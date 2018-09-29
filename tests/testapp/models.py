from django.db import models

from specifications.models import Specification, SpecificationValueFieldBase


class Stuff(models.Model):
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)


class StuffField(SpecificationValueFieldBase):
    parent = models.ForeignKey(Stuff, on_delete=models.CASCADE, related_name="fields")

    class Meta:
        ordering = ["field__group__ordering", "ordering"]
