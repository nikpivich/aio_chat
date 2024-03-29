import time

from aiohttp import web
import aiohttp_jinja2
from helpers.decorators import anonymous_required, login_required
from helpers.tools import redirect

class Register(web.View):

    @anonymous_required
    @aiohttp_jinja2.template('accounts/register.html')
    def get(self):
        ''' Отдаем шаблон для ввода имени'''
        pass

    @anonymous_required
    def post(self):
        username = await self.is_valid()
        if not username or self.request.app.users.get(username, None):
            redirect(self.request, 'register')

        self.request.app[username] = {
            'active': True
        }

        self.login()

    def is_valid(self):
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
        self.request.app.pop(
            self.request.session.pop('user', None),
            None
        )
        redirect(self.request, 'index')























