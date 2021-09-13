import inspect
import itertools

from django import forms
from django.contrib import admin
from django.utils.translation import gettext as _

from specifications import models
from specifications.forms import FormWithSpecification


class SpecificationFieldGroupInline(admin.TabularInline):
    model = models.SpecificationFieldGroup
    extra = 0


class SpecificationFieldForm(forms.ModelForm):
    class Meta:
        model = models.SpecificationField
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        data = super().clean()

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
    def get_form(self, request, obj=None, **kwargs):
        if not hasattr(request, "_form_with_specification_class"):
            form_class = super().get_form(request, obj, **kwargs)
            request._form_with_specification_class = type(
                self.form.__name__,
                (FormWithSpecification, form_class),
                {},
            )
        return request._form_with_specification_class

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            obj.specification.update_fields(obj)  # XXX Maybe once too often
            fieldsets.extend(self.grouped_specification_fieldsets(obj))
        return fieldsets

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
