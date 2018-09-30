from __future__ import unicode_literals

import inspect
import itertools

from django import forms
from django.contrib import admin
from django.utils.translation import ugettext as _

from specifications.forms import FormWithSpecification
from specifications import models


class SpecificationFieldGroupInline(admin.TabularInline):
    model = models.SpecificationFieldGroup
    extra = 0


class SpecificationFieldForm(forms.ModelForm):
    class Meta:
        model = models.SpecificationField
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SpecificationFieldForm, self).__init__(*args, **kwargs)

        try:
            # DON'T LOOK! WAAAH
            instance = inspect.currentframe().f_back.f_locals["self"].instance
        except KeyError:
            instance = None

        # When adding new specifications ``instance`` is set but does not have
        # a ``pk`` attribute yet. Still, instance.groups.all() works and
        # returns an empty queryset (which is what we want -- no groups from
        # other specifications)
        if instance:
            self.fields["group"].queryset = instance.groups.all()

    def clean(self):
        data = super(SpecificationFieldForm, self).clean()

        if data.get("choices") and "_set_" not in data.get("type"):
            raise forms.ValidationError(
                _("Cannot set choices when not using a set type.")
            )

        if "closed_set" in data.get("type", "") and not data.get("choices"):
            raise forms.ValidationError(
                _("Please provide at least one choice when using a closed set.")
            )

        return data


class SpecificationFieldInline(admin.TabularInline):
    model = models.SpecificationField
    form = SpecificationFieldForm
    extra = 0
    # All fields, but different ordering:
    fields = ("group", "name", "type", "choices", "help_text", "required", "ordering")


admin.site.register(
    models.Specification,
    inlines=[SpecificationFieldGroupInline, SpecificationFieldInline],
)


class ModelAdminWithSpecification(admin.ModelAdmin):
    form = FormWithSpecification

    def can_add_specification_fields(self, request, obj):
        if obj is None:
            return False
        # Is the ModelForm already defined? Then we are currently creating
        # the adminform helper. In this case, return a fieldset including
        # the specifications' fields. (If we did this for creating the initial
        # ModelForm the creation would fail because of unknown model fields.)
        frame = inspect.currentframe()
        try:
            while frame:
                ModelForm = frame.f_locals.get("ModelForm")
                if ModelForm is not None and obj.specification:
                    return True
                frame = frame.f_back
        finally:
            del frame
        return False

    def grouped_specification_fieldsets(self, obj):
        fieldsets = []
        for group, fields in itertools.groupby(
            obj.fields.order_by("field__group__ordering", "ordering").select_related(
                "field__group"
            ),
            key=lambda field: field.field.group,
        ):
            fieldsets.append(
                (
                    _("Specification") if group is None else group.name,
                    {"fields": [field.formfield_name() for field in fields]},
                )
            )
        return fieldsets
