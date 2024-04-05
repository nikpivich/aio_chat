import jinja2
from aiohttp import web
import aiohttp_jinja2
from settings import BASE_DIR, HOST, PORT
from accounts.urls import routes as acc_routes
from chat.urls import routes as chat_routes
from helpers.middlewares import middlewares


if __name__ == '__main__':
    app = web.Application(
        middlewares=middlewares
    )

    jinja_env = aiohttp_jinja2.setup(
        app,
        loader = jinja2.FileSystemLoader(BASE_DIR / 'templates'),
        context_processors=[aiohttp_jinja2.request_processor]
    )

    # все userы
    app.users = {}

   # Все rooms
    app.chats = {}

    #     'room_name': {
    #         'usernmae1': {
    #             'status': True,
    #             'ws': 'WebSocketClass'
    #         },
    #         'username2':{
    #             'status': True,
    #             'ws': 'WebSocketClass'
    #         }
    #     }
    # }



    app.router.add_routes(acc_routes)
    app.router.add_routes(chat_routes)

    app.router.add_static('/static/', BASE_DIR / 'static', name='static')

    web.run_app(app, host=HOST, port=PORT)





