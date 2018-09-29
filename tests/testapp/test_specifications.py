from django.contrib.auth.models import User
from django.test import Client, TestCase

from specifications.models import Specification, SpecificationField
from specifications.utils import specification_values_dict

from testapp.models import Stuff


class SpecificationsTest(TestCase):
    def login(self):
        client = Client()
        self.user = User.objects.create(
            username="test", is_staff=True, is_superuser=True
        )
        client.force_login(self.user)
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

        return spec

    def test_models(self):
        spec = self.create_specification()
        stuff = Stuff.objects.create(specification=spec)

        self.assertEqual(dict(specification_values_dict(stuff)), {})

        spec.update_fields(stuff)

        print(specification_values_dict(stuff))

    def test_admin(self):
        spec = self.create_specification()
        stuff = Stuff.objects.create(specification=spec)

        client = self.login()
        response = client.get("/admin/testapp/stuff/{}/change/".format(stuff.pk))
        print(response.content.decode("utf-8"))

        response = client.get("/admin/testapp/stuff/{}/change/".format(stuff.pk))
        self.assertEqual(response.status_code, 200)

        response = client.get("/admin/testapp/stuff/add/")
        self.assertEqual(response.status_code, 200)
