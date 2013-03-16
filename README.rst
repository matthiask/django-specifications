=====================
django-specifications
=====================

This module offers an easy way to attach auxiliary information to Django
models. It allows configuring custom forms through the administration
interface.

Usage
=====

1. Add ``'specifications'`` to ``INSTALLED_APPS``.
2. Create a ``specification = ForeignKey('specifications.Specification')`` 
   on the model you want to use specifications with. The foreign key can 
   be nullable or required, as you wish.
3. Create the place where the specification field data is actually stored::

       from specifications.models import SpecificationValueFieldBase

       class MyObjectField(SpecificationValueFieldBase):
           parent = models.ForeignKey(MyObject, related_name='fields')

           class Meta:
               ordering = ['field__group__ordering', 'ordering']

4. Inherit from ``FormWithSpecification`` when creating your ``ModelForm``::

       from specifications.forms import FormWithSpecification

       class MyObjectForm(FormWithSpecification):
           class Meta:
               model = MyObject

5. There is no fifth step.

The fields are available after saving a specification. The specification can
be changed, but you risk losing data if you do this.
