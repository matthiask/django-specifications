import re

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from specifications.models import Specification, SpecificationField
from specifications.utils import specification_values_dict

from testapp.models import Stuff


class SpecificationsTest(TestCase):
    def login(self):
        client = Client()
        self.user = User.objects.create_superuser("test", "test@example.com", "test")
        client.login(username="test", password="test")
        return client

    def create_specification(self):
        spec = Specification.objects.create(name="specs")
        display = spec.groups.create(name="monitor", ordering=1)
        computer = spec.groups.create(name="computer", ordering=2)

        SpecificationField.objects.create(
            name="screen size",
            type=SpecificationField.TEXT,
            ordering=1,
            group=display,
            specification=spec,
        )
        SpecificationField.objects.create(
            name="true color",
            type=SpecificationField.BOOLEAN,
            ordering=2,
            group=display,
            specification=spec,
        )

        SpecificationField.objects.create(
            name="CPU family",
            type=SpecificationField.CLOSED_SET_SINGLE,
            ordering=1,
            choices="i7\ni5\ni3",
            group=computer,
            specification=spec,
        )
        SpecificationField.objects.create(
            name="RAM",
            type=SpecificationField.CLOSED_SET_SINGLE,
            ordering=2,
            choices="32 GB\n16 GB\n8 GB",
            group=computer,
            specification=spec,
        )

        SpecificationField.objects.create(
            name="Name",
            type=SpecificationField.TEXT,
            ordering=1,
            group=None,  # Free-floating.
            specification=spec,
        )

        return spec

    def test_models(self):
        spec = self.create_specification()
        stuff = Stuff.objects.create(specification=spec)

        self.assertEqual(dict(specification_values_dict(stuff)), {})

        spec.update_fields(stuff)

        self.assertNotEqual(dict(specification_values_dict(stuff)), {})

    def test_specification_admin(self):
        self.create_specification()
        spec = self.create_specification()  # Create it twice.
        client = self.login()

        response = client.get(
            reverse("admin:specifications_specification_change", args=(spec.pk,))
        )

        # Test that the fields group dropdown only contains groups from the
        # specification we are editing.
        self.assertContains(
            response,
            """
<select name="fields-__prefix__-group" id="id_fields-__prefix__-group">
<option value="" selected>---------</option>
<option value="{}">monitor</option>
<option value="{}">computer</option>
</select>
            """.format(
                *[group.id for group in spec.groups.all()]
            ),
            html=True,
        )

        # No groups selectable even though groups exist in other specifications.
        response = client.get(reverse("admin:specifications_specification_add"))
        # print(response.content.decode("utf-8"))
        self.assertContains(
            response,
            """
<select name="fields-__prefix__-group" id="id_fields-__prefix__-group">
<option value="" selected>---------</option>
</select>
            """,
            html=True,
        )

    def test_admin_with_specification(self):
        spec = self.create_specification()
        stuff = Stuff.objects.create(specification=spec)

        client = self.login()

        response = client.get("/admin/testapp/stuff/add/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "8 GB")

        response = client.get(reverse("admin:testapp_stuff_change", args=(stuff.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "8 GB")

        h2 = re.findall(r"<h2>(.+?)</h2>", response.content.decode("utf-8"))
        self.assertEqual(h2, ["Specification", "monitor", "computer"])

        field_ids = set(field.field_id for field in stuff.fields.all())
        self.assertEqual(stuff.fields.count(), 5)

        # Delete several fields at once to test the Specification.update_fields code
        sf1 = SpecificationField.objects.get(name="RAM")
        sf2 = SpecificationField.objects.get(name="CPU family")
        sf3 = SpecificationField.objects.get(name="true color")

        new_field_ids = field_ids - {sf1.id, sf2.id, sf3.id}

        sf1.delete()
        sf2.delete()
        sf3.delete()

        self.assertEqual(
            set(field.field_id for field in stuff.fields.all()), new_field_ids | {None}
        )

        response = client.get(reverse("admin:testapp_stuff_change", args=(stuff.pk,)))
        self.assertEqual(stuff.fields.count(), 2)
        # print(response, response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "8 GB")
