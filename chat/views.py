import datetime

import aiohttp
from aiohttp import web
import aiohttp_jinja2
from helpers.decorators import anonymous_required, login_required
from helpers.tools import redirect

class CreateRoom(web.View):

    @login_required
    @aiohttp_jinja2.template('chat/rooms.html')
    async def get(self):
        pass

    @login_required
    async def post(self):
        self.roomname = await self.is_valid()

        if not self.roomname:
            redirect(self.request, 'create_room')

        chats = self.request.app.chats

        # Комната занята
        if chats.get(self.roomname) and len(chats[self.roomname]) >=2:
            redirect(self.request, 'create_room')

        # Первое подключение
        elif not chats.get(self.roomname):
            chats[self.roomname] = {
                self.request.user: {
                    'active': True
                }
            }

        #Второе и последующие
        else:
            message = {
                'text': '<Подключился>',
                'user': self.request.user,
                'created_at': datetime.datetime.now().isoformat()

            }
            await self.broadcast(message)

            chats[self.roomname][self.request.user] = {
                'active': True
            }

        redirect(self.request, 'room', slug=self.roomname)

    async def is_valid(self):
        data = await self.request.post()
        roomname = data.get('roomname', '').lower()
        if len(roomname)< 4:
            return False
        return roomname

    # для всех
    async def broadcast(self, message):
        cliets_data = self.request.app.chats[self.roomname].values()
        print(cliets_data)
        for client in cliets_data:
            await client['ws'].send_json(message)


class ChatRoom(web.View):
    @login_required
    @aiohttp_jinja2.template('chat/chat.html')
    async def get(self):
        roomname = self.request.match_info['slug'].lower() # = roomname
        return {
            'room': {'name': roomname}
        }



class WebSocket(web.View):
    async def get(self):
        self.room = self.request.match_info['slug'].lower()
        username : str = self.request.user
        app = self.request.app
        ws = web.WebSocketResponse()

        await ws.prepare(self.request)

        if not app.chats.get(self.room) or not app.chats[self.room].get(username):
            redirect(self.request, 'create_room')

        app.chats[self.room][username]['ws'] = ws # Указываем текущему пользователю сокет

        async for msg in ws:  # Цикл приема сообщения
            if msg.type == aiohttp.WSMsgType.text:
                if msg.data == '/close':
                    await ws.close()

                else: # Обработка сообщений от пользователя
                    text = msg.data.strip() #получаем сообщения от текущкго пользователя
                    message = {
                        'text': text,
                        'user': username,
                        'created_at': datetime.datetime.now().isoformat()
                    }
                    await self.broadcast(message) # Отправкавсем пользоввателям в комнате

            elif msg.type == web.WSMsgType.error:
                print('errror')
                break
                # await ws.close()

        await self.dissconect(username, ws)

    async def broadcast(self, message):
        cliets_data = self.request.app.chats[self.room].values()
        print(cliets_data)
        for client in cliets_data:
            await client['ws'].send_json(message)

    async def dissconect(self, username, socket):
        self.request.app.chats[self.room].pop(username, None)
        if not socket.closed:
            await socket.close()

        if not self.request.app.chats[self.room]:
            self.request.app.chats.pop(self.room)


class Index(web.View):


    @aiohttp_jinja2.template('index.html')
    async def get(self):
        pass
