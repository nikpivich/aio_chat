from aiohttp import web
from . import views


routes = [
    web.route("*", "/login", views.LogIn, name="login"),
    web.route('*', '/register', views.Register, name='register'),
    web.route('*', '/logout', views.Logout, name='logout')
]