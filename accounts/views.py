import datetime
import time

from aiohttp import web
import aiohttp_jinja2
from helpers.decorators import anonymous_required, login_required
from helpers.tools import redirect

class LogIn(web.View):
    pass

    # @aiohttp_jinja2.template("users/login.html")
    # async def get(self):
    #     return {}
    #
    # async def post(self):
    #     data = await self.request.post()
    #     username = data.get('username', '').lower()
    #
    #     try:
    #         user = await User.get(username=username)
    #     except Exception as error:
    #         print(error)
    #         redirect(self.request, "login")
    #         return
    #
    #     else:
    #         self.login(user)
    #     return web.json_response({"user": user.id})
    #
    # def login(self, user: User):
    #
    #     self.request.session["user_id"] = user.id
    #     self.request.session["time"] = str(datetime.datetime.now())
    #
    #     redirect(self.request, "home")

class Register(web.View):

    @anonymous_required
    @aiohttp_jinja2.template('accounts/register.html')
    def get(self):
        ''' Отдаем шаблон для ввода имени'''
        pass

    @anonymous_required
    async def post(self):
        username = await self.is_valid()
        if not username or self.request.app.users.get(username, None):
            redirect(self.request, 'register')

        self.request.app.users[username] = {
            'active': True
        }

        self.login(username)

    async def is_valid(self):
        '''Проверяем имя пользователя'''

        data = await self.request.post()
        username = data.get('username', '').lower()
        if 4 < len(username) < 10:
            return False
        return username

    def login(self, username):
        """Создаем на основе имени пользователя запись сессии в Redis"""

        self.request.session['user'] = username # Добавляем поле имени
        self.request.session['time'] = time.time() # Добавляем поле временн
        redirect(self.request, 'index') # Перенаправляем на главную


class Logout(web.View):

    @login_required
    async def get(self):
        self.request.app.users.pop(
            self.request.session.pop('user', None),
            None
        )
        redirect(self.request, 'index')























