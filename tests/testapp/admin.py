from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from specifications.admin import ModelAdminWithSpecification

from . import models


@admin.register(models.Stuff)
class StuffAdmin(ModelAdminWithSpecification):
    def get_fieldsets_with_specification(self, request, obj, fieldsets):
        if obj is not None and obj.specification:
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
