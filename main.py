import requests
from pprint import pprint

from config import TOKEN, ADMINS



class Bot:
    
    def __init__(self, token: str):
        self.token = token
        self.BASE_URL = F'https://api.telegram.org/bot{token}'
        self.offset = int
        self.limit = 5
    
     
    def get_updates(self) -> list[dict] | bool:
        get_url = f'{self.BASE_URL}/getUpdates'
        
        params = {
        "offset": self.offset,
        "limit": self.limit 
        }
        response = requests.get(get_url, params=params)

        if response.status_code == 200:
            return response.json()["result"]
        return False
    
    
    def copy_message(self, chat_id: int | str,  from_chat_id: int | str, message_id: int, ) -> bool:
        get_url = f'{self.BASE_URL}/copyMessage'
        
        params = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_id": message_id
        }
        response = requests.get(get_url, params=params)

        return True if response.status_code == 200 else False
    
    
    def send_message(self, chat_id: int | str, text: str) -> None:
        get_url = f'{self.BASE_URL}/sendMessage'
        
        params = {
            "chat_id": chat_id,
            "text": text
        }
        requests.get(get_url, params=params)
    
    
    def main(self) -> None:
        
        while True:
            updates = self.get_updates()
            
            if updates:
                for update in updates:
                    chat_id = update["message"]["chat"]["id"]
                    message_id = update["message"]["message_id"]
                    
                    copy_status = self.copy_message(chat_id=chat_id, from_chat_id=chat_id, message_id=message_id)
                    if not copy_status:
                        self.send_message(chat_id=chat_id, text="yaxshi")
                        
                self.offset = updates[-1]["update_id"] + 1
                    
                

def notify(admins: list, bot: Bot):
    try:
        for admin in admins:
            bot.send_message(admin, "Bot ishga tushdi")
    
    except Exception as e:
        print("ERROR   \n {e}")
    
              

def main() -> None:
    bot = Bot(TOKEN)
    
    bot.main()
    notify(ADMINS, bot)
    
    
main()