def get_or_none(classmodel, *args, **kwargs):
    try:
        return classmodel.objects.get(*args, **kwargs)
    except classmodel.DoesNotExist:
        return None
