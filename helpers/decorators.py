from .tools import redirect


def login_required(func):
    async def wrapped(self, *args, **kwargs):
        if self.request.user is None:
            redirect(self.request, 'register')
        return await func(self, *args, **kwargs)
    return wrapped


def anonymous_required(func):
    async def wrapped(self, *args, **kwargs):
        if self.request.user is not None:
            redirect(self.request, 'index')
        return await func(self, *args, **kwargs)
    return wrapped