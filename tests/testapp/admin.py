from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from specifications.forms import FormWithSpecification

from . import models


@admin.register(models.Stuff)
class StuffAdmin(admin.ModelAdmin):
    form = FormWithSpecification

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(StuffAdmin, self).get_fieldsets(request, obj=obj)

        # Only add specification fields to adminform when we are creating the
        # adminform helper, not when creating the modelform (because obviously
        # the model and its form will not know about additional fields)
        import inspect
        creating_adminform = "to_field" in inspect.currentframe().f_back.f_locals

        if creating_adminform and obj is not None and obj.specification:
            obj.specification.update_fields(obj)  # TODO redundant?
            # TODO groups!
            fieldsets.append(
                (
                    _("Specification"),
                    {
                        "fields": [
                            field.formfield_name()
                            for field in obj.fields.select_related("field__group")
                        ]
                    },
                )
            )

        return fieldsets
