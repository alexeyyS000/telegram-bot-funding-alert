def check_admin(func):
    async def inner(*args, **kwargs):
        if kwargs["user"] is None or not kwargs["user"].admin:
            return 1
        await func(*args)

    return inner


def check_unregistrated_user(func):
    async def inner(*args, **kwargs):
        if kwargs["user"] is not None:
            return 1
        await func(*args)

    return inner


def check_not_banned_subscriber_user(func):
    async def inner(*args, **kwargs):
        if kwargs["user"] is None or kwargs["user"].pending or kwargs["user"].banned:
            return 1
        await func(*args)

    return inner
