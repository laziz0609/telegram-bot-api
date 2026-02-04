import asyncio
import aiohttp

from config import TOKEN, ADMINS



class Bot:
    
    def __init__(self, token: str):
        self.token = token
        self.session = aiohttp.ClientSession()
        self.BASE_URL = F'https://api.telegram.org/bot{token}'
        self.offset = 0
        self.limit = 5
    
     
    async def get_updates(self) -> list[dict] | bool:
        get_updates_url = f'{self.BASE_URL}/getUpdates'
        
        params = {
        "offset": self.offset,
        "limit": self.limit 
        }
        async with self.session.get(get_updates_url, params=params) as response: 
            if response.status == 200:
                data = await response.json()
                return data["result"]
            return False
    
    
    async def copy_message(self, chat_id: int | str,  from_chat_id: int | str, message_id: int, ) -> bool:
        copy_message_url = f'{self.BASE_URL}/copyMessage'
        
        params = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_id": message_id
        }
        async with self.session.post(copy_message_url, params=params) as response: 
            return True if response.status == 200 else False
    
    
    
    async def send_message(self, chat_id: int | str, text: str) -> bool:
        send_message_url = f'{self.BASE_URL}/sendMessage'
        
        params = {
            "chat_id": chat_id,
            "text": text
        }
        async with self.session.post(send_message_url, params=params) as res: 
            return True if res.status == 200 else False
    
    
    
    async def main(self) -> None:
        
        while True:
            updates = await self.get_updates()
            
            if updates:
                for update in updates:
                    chat_id = update["message"]["chat"]["id"]
                    message_id = update["message"]["message_id"]
                    
                    copy_status = await self.copy_message(chat_id=chat_id, from_chat_id=chat_id, message_id=message_id)
                    if not copy_status:
                        await self.send_message(chat_id=chat_id, text="yaxshi")
                        
                self.offset = updates[-1]["update_id"] + 1
                    
                

async def notify(admins: list, bot: Bot):
    try:
        for admin in admins:
            status = await bot.send_message(admin, "Bot ishga tushdi")
            if not status:
                print("xabar adminga jo'natilmadi")
    except Exception as e:
        print("ERROR   \n {e}")
    
              

async def main() -> None:
    bot = Bot(TOKEN)
    
    await notify(ADMINS, bot)
    await bot.main()
    
    
    
asyncio.run(main())