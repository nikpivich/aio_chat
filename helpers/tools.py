
from aiohttp import web


def redirect(request, router_name,permanent=False ,**kwargs):
    print(router_name)
    url = request.app.router[router_name].url_for(**kwargs)
    print(url)
    if permanent:
        raise web.HTTPPermanentRedirect(url)
    raise web.HTTPFound(url)

