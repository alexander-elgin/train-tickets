def is_authenticated(info) -> bool:
    return info.context.user.is_authenticated


def check_authentication(info):
    if not is_authenticated(info):
        raise Exception('Unauthorized')
