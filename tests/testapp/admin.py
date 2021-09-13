from django.contrib import admin

from specifications.admin import ModelAdminWithSpecification

from . import models


@admin.register(models.Stuff)
class StuffAdmin(ModelAdminWithSpecification):
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if self.can_add_specification_fields(request, obj):
            obj.specification.update_fields(obj)
            fieldsets.extend(self.grouped_specification_fieldsets(obj))

        return fieldsets
