from prisma import Prisma


class DataService:
    db: Prisma

    def __init__(self) -> None:
        self.db = Prisma()

    async def connect(self) -> None:
        if not self.db.is_connected():
            await self.db.connect()

    async def disconnect(self) -> None:
        if self.db.is_connected():
            await self.db.disconnect()

    def get_db(self) -> Prisma:
        return self.db
