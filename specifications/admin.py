from django import forms
from django.contrib import admin
from django.utils.translation import ugettext as _

from specifications import models


class SpecificationFieldGroupInline(admin.TabularInline):
    model = models.SpecificationFieldGroup
    extra = 0


class SpecificationFieldForm(forms.ModelForm):
    class Meta:
        model = models.SpecificationField

    def __init__(self, *args, **kwargs):
        super(SpecificationFieldForm, self).__init__(*args, **kwargs)

        try:
            # DON'T LOOK! WAAAH
            import inspect
            instance = inspect.currentframe().f_back.f_locals['self'].instance
        except KeyError:
            instance = None

        if instance:
            self.fields['group'].queryset = instance.groups.all()

    def clean(self):
        data = super(SpecificationFieldForm, self).clean()

        if data.get('choices') and '_set_' not in data.get('type'):
            raise forms.ValidationError(_('Cannot set choices when not using a set type.'))

        if 'closed_set' in data.get('type') and not data.get('choices'):
            raise forms.ValidationError(
                _('Please provide at least one choice when using a closed set.'))

        return data


class SpecificationFieldInline(admin.TabularInline):
    model = models.SpecificationField
    form = SpecificationFieldForm
    extra = 0
    # All fields, but different ordering:
    fields = ('group', 'name', 'key', 'type', 'choices', 'help_text', 'required', 'ordering')


admin.site.register(models.Specification,
    inlines=[SpecificationFieldGroupInline, SpecificationFieldInline],
    )
