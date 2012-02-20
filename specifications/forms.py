from django import forms
from django.utils.datastructures import SortedDict


class FormWithSpecification(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormWithSpecification, self).__init__(*args, **kwargs)

        self.specification_fields = SortedDict()
        if self.instance and self.instance.pk and self.instance.specification:
            self.instance.specification.update_fields(self.instance)
            for field in self.instance.fields.select_related('field__group'):
                self.specification_fields.setdefault(field.group, []).append(
                    field.add_formfield(self))

    def save(self, *args, **kwargs):
        instance = super(FormWithSpecification, self).save(*args, **kwargs)

        if self.specification_fields:
            for field in instance.fields.all():
                field.update_value(self)

        return instance

    def specification_field_values(self):
        if not (self.instance and self.instance.pk and self.instance.specification):
            return {}

        values = {}
        for field in self.instance.fields.all():
            values[field.key] = field.get_value(self)
        return values
