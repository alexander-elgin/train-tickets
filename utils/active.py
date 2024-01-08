def check_active(id, Model, model_name):
    obj = Model.objects.get(pk=id)

    if not obj.active:
        raise Exception(f'The {model_name} is inactive')
