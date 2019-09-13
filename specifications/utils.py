from collections import OrderedDict, defaultdict


def specification_values_dict(instance):
    """
    Returns a dictionary suitable for outputting the specification field
    values.
    """
    groups = OrderedDict()
    for field in instance.fields.select_related("field__group"):
        groups.setdefault(field.group, []).append(
            (field.name, field.get_value_display())
        )
    return groups


def specification_values_comparison(*instances):
    """
    Returns a data structure most useful to display a comparison between
    different instances with the same specification.
    """
    ValueField = instances[0].fields.model
    indices = dict((instance.pk, idx) for idx, instance in enumerate(instances))
    groups = defaultdict(lambda: defaultdict(lambda: [None] * len(instances)))

    for field in ValueField._default_manager.filter(
        parent__in=instances
    ).select_related("field__group"):
        groups[field.field.group][field.field][
            indices[field.parent_id]
        ] = field.get_value_display()

    group_list = []
    for group, fields in sorted(groups.items()):
        group_list.append(
            (group, sorted(fields.items(), key=lambda item: item[0].ordering))
        )

    return {"instances": instances, "group_list": group_list}
