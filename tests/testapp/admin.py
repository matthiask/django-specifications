from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from specifications.admin import ModelAdminWithSpecification

from . import models


@admin.register(models.Stuff)
class StuffAdmin(ModelAdminWithSpecification):
    def get_fieldsets(self, request, obj=None):
        fieldsets = super(StuffAdmin, self).get_fieldsets(request, obj)
        if self.can_add_specification_fields(request, obj):
            obj.specification.update_fields(obj)
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
