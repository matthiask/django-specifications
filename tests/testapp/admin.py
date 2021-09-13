from django.contrib import admin

from specifications.admin import ModelAdminWithSpecification

from . import models


@admin.register(models.Stuff)
class StuffAdmin(ModelAdminWithSpecification):
    pass
