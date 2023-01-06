from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections: dict[str, WebSocket] = {}
        self.generator = self.get_notification_generator()

    async def get_notification_generator(self):
        while True:
            message = yield
            await self._notify(message)

    async def push(self, message):
        print(message)
        await self.generator.asend(message)

    async def connect(self, websocket: WebSocket, user_id: str):
        if user_id in self.connections.keys():
            await self.push("User already registered")

        await websocket.accept()
        self.connections[user_id] = websocket
        await self.push("User connected")

    async def remove(self, websocket: WebSocket, user_id: str):
        if user_id in self.connections:
            self.connections.pop(user_id)

    async def _notify(self, message):  # Response
        living_connections = {}
        keys = list(self.connections.keys())

        for user in keys:
            websocket = self.connections.pop(user)
            await websocket.send_text(message)
            living_connections[user] = websocket

        self.connections = living_connections

    async def broadcast(self, message: str):
        await self.push(message)
