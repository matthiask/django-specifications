from functools import partial

from django import forms
from django.core.cache import cache
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


class Specification(models.Model):
    name = models.CharField(_("name"), max_length=100)
    notes = models.TextField(_("notes"), blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("specification")
        verbose_name_plural = _("specifications")

    def __str__(self):
        return self.name

    def update_fields(self, instance):
        """
        Updates the fields on the passed instance from the specification
        """

        valuefields = instance.fields.all()
        existing = {f.field_id: f for f in valuefields if f.field_id}
        instance_field_model = instance.fields.model

        for spec in self.fields.all():
            try:
                valuefield = existing.pop(spec.pk)
            except KeyError:
                valuefield = instance_field_model(parent=instance, field=spec)

            spec.update_fields_on(valuefield)
            valuefield.save()

        for valuefield in existing.values():
            valuefield.delete()
        for valuefield in valuefields:
            if not valuefield.field_id:
                valuefield.delete()


class SpecificationFieldGroup(models.Model):
    specification = models.ForeignKey(
        Specification,
        on_delete=models.CASCADE,
        verbose_name=_("specification"),
        related_name="groups",
    )
    name = models.CharField(_("name"), max_length=100)
    ordering = models.IntegerField(_("ordering"), default=0)

    class Meta:
        ordering = ["ordering"]
        verbose_name = _("specification field group")
        verbose_name_plural = _("specification field groups")

    def __str__(self):
        return self.name


def open_set_formfield(**kwargs):
    choices = kwargs.pop("choices", ())
    kwargs["widget"] = forms.Select(choices=choices, attrs={"class": "combo"})
    return forms.CharField(**kwargs)


class SpecificationFieldBase(models.Model):
    TEXT = "text"
    LONGTEXT = "longtext"
    BOOLEAN = "boolean"
    INTEGER = "integer"
    CLOSED_SET_SINGLE = "closed_set_single"
    CLOSED_SET_MULTIPLE = "closed_set_multiple"
    OPEN_SET_SINGLE = "open_set_single"
    OPEN_SET_SINGLE_EXTENSIBLE = "open_set_single_extensible"
    # OPEN_SET_MULTIPLE = 'open_set_multiple'
    # Currently disabled, let's hope nobody ever needs this :-)
    # Otherwise, look into towel's multiple autocompletion widget

    TYPES = (
        (TEXT, _("text"), forms.CharField),
        (LONGTEXT, _("long text"), partial(forms.CharField, widget=forms.Textarea)),
        (BOOLEAN, _("boolean"), forms.BooleanField),
        (INTEGER, _("integer"), forms.IntegerField),
        (
            CLOSED_SET_SINGLE,
            _("closed set"),
            partial(forms.ChoiceField, widget=forms.RadioSelect),
        ),
        (
            CLOSED_SET_MULTIPLE,
            _("closed set (multiple)"),
            partial(forms.MultipleChoiceField, widget=forms.CheckboxSelectMultiple),
        ),
        (OPEN_SET_SINGLE, _("open set"), open_set_formfield),
        (OPEN_SET_SINGLE_EXTENSIBLE, ("open set (extensible)"), open_set_formfield),
        # (OPEN_SET_MULTIPLE, _('Open set (multiple)'),
        #     partial(forms.MultipleChoiceField,
        #           widget=forms.CheckboxSelectMultiple)),
    )

    TYPE_CHOICES = [r[0:2] for r in TYPES]

    name = models.CharField(_("name"), max_length=100)
    type = models.CharField(_("type"), max_length=30, choices=TYPE_CHOICES)
    choices = models.TextField(
        _("choices"), blank=True, help_text=_("One choice per line (if applicable).")
    )
    help_text = models.CharField(_("help text"), max_length=100, blank=True, default="")
    required = models.BooleanField(_("required"), default=True)

    ordering = models.IntegerField(_("ordering"), default=0)

    class Meta:
        abstract = True
        ordering = ["ordering"]

    def __str__(self):
        return self.name

    def get_type(self, **kwargs):
        types = dict((r[0], r[2]) for r in self.TYPES)
        return types[self.type](**kwargs)

    @property
    def fullname(self):
        return self.name

    def update_fields_on(self, instance):
        instance.name = self.name
        instance.type = self.type
        instance.choices = self.choices
        instance.help_text = self.help_text
        instance.required = self.required
        instance.ordering = self.ordering


class SpecificationField(SpecificationFieldBase):
    specification = models.ForeignKey(
        Specification,
        on_delete=models.CASCADE,
        verbose_name=_("specification"),
        related_name="fields",
    )
    group = models.ForeignKey(
        SpecificationFieldGroup,
        on_delete=models.SET_NULL,
        verbose_name=_("group"),
        related_name="fields",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["group__ordering", "ordering"]
        verbose_name = _("specification field")
        verbose_name_plural = _("specification fields")

    def __str__(self):
        return self.fullname

    @property
    def fullname(self):
        if self.group:
            return "%s - %s" % (self.group, self.name)
        return self.name


class SpecificationValueFieldBase(SpecificationFieldBase):
    field = models.ForeignKey(
        SpecificationField,
        on_delete=models.SET_NULL,
        verbose_name=_("specification field"),
        related_name="+",
        blank=True,
        null=True,
    )
    value = models.TextField(_("value"), default="")

    class Meta:
        abstract = True
        ordering = ["field__group__ordering", "ordering"]

    def __str__(self):
        return self.fullname

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.clobber_choices_cache()

    save.alters_data = True

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.clobber_choices_cache()

    save.alters_data = True

    @property
    def choices_cache_key(self):
        return "svfb_choices_%s" % self.field_id

    def clobber_choices_cache(self):
        cache.delete(self.choices_cache_key)

    @property
    def group(self):
        if self.field:
            return self.field.group
        return None

    @property
    def fullname(self):
        if self.field:
            return self.field.fullname
        return self.name

    def get_choices(self):
        choices = [value.strip() for value in self.choices.splitlines()]
        choices = [(slugify(value), value) for value in choices if value]

        if not self.required and self.type in (
            "open_set_single",
            "open_set_single_extensible",
        ):
            choices = BLANK_CHOICE_DASH + choices
        if "extensible" in self.type:
            values = cache.get(self.choices_cache_key)
            if not values:
                # Cannot use self.field.values... because of related_name
                # clashes when several subclasses of
                # SpecificationValueFieldBase exist
                values = (
                    self.__class__.objects.filter(field=self.field)
                    .values_list("value", flat=True)
                    .order_by("value")
                    .distinct()
                )
                cache.set(self.choices_cache_key, values)

            existing = dict(choices)
            for v in values:
                if v in existing:
                    continue
                choices.append((v, v))

        return list(choices)

    def formfield(self, form=None):
        kwargs = dict(label=self.name, required=self.required, help_text=self.help_text)

        if self.value:
            if "multiple" in self.type:
                kwargs["initial"] = self.value.split("|")
            else:
                kwargs["initial"] = self.value
        if self.choices or "open_set" in self.type:
            choices = self.get_choices()
            if self.type == "open_set_single":
                # Ensure the current value is available too

                if (
                    form
                    and form.instance
                    and kwargs.get("initial")
                    and kwargs["initial"] not in dict(choices)
                ):
                    choices = [(kwargs["initial"], kwargs["initial"])] + choices
            kwargs["choices"] = choices

        return self.get_type(**kwargs)

    def formfield_name(self):
        return "field_%s" % (self.field.pk if self.field else self.pk)

    def add_formfield(self, form):
        """
        Adds the specification field to the form and returns the corresponding
        ``BoundField`` instance.
        """
        field_name = self.formfield_name()
        form.fields[field_name] = self.formfield(form=form)
        return form[field_name]

    def get_value(self, form):
        newvalue = form.cleaned_data.get(self.formfield_name())
        if newvalue is None:
            return ""
        if "multiple" in self.type:
            newvalue = "|".join(sorted(newvalue))
        return newvalue

    def update_value(self, form):
        newvalue = self.get_value(form)
        if newvalue != self.value:
            self.value = newvalue or ""
            self.save()

    def get_value_display(self):
        if self.value and (self.choices or "open_set" in self.type):
            choices = dict(self.get_choices())
            if "multiple" in self.type:
                return ", ".join(choices.get(v, v) for v in self.value.split("|"))
            else:
                return choices.get(self.value, self.value)
        return self.value

    def create_copy(self):
        """
        Returns an unsaved copy containing all of the values of this abstract
        base class. It is your responsability to copy additional fields and
        save the return value if you want to persist the copy.
        """
        return self.__class__(
            name=self.name,
            type=self.type,
            choices=self.choices,
            help_text=self.help_text,
            required=self.required,
            ordering=self.ordering,
            field=self.field,
            value=self.value,
        )
