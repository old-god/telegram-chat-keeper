import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not API_TOKEN:
    logging.error("TELEGRAM_BOT_TOKEN is not set.")
    exit(1)

class ChatKeeperBot:
    def __init__(self, token):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()

        # Регистрация хэндлеров
        self.register_handlers()

    def register_handlers(self):
        self.dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=(None, 'member', 'left')))(self.on_chat_member_update)
        self.dp.message()(self.handle_message)
        self.dp.update()(self.handle_unhandled_updates)
    
    async def delete_message(self, chat_id: int, message_id: int):
        try:
            await self.bot.delete_message(chat_id, message_id)
            logging.debug(f"Message {message_id} deleted in chat {chat_id}")
        except Exception as e:
            logging.error(f"Не удалось удалить сообщение {message_id}: {e}")

    async def ban_user(self, chat_id: int, user_id: int):
        try:
            await self.bot.ban_chat_member(chat_id, user_id)
            logging.debug(f"User {user_id} banned in chat {chat_id}")
        except Exception as e:
            logging.error(f"User {user_id} was not banned in chat {chat_id}: {e}")

    async def on_chat_member_update(self, event: ChatMemberUpdated):
        logging.debug(f"User {event.from_user.id} changed status to {event.new_chat_member.status}")
        
        if event.new_chat_member.status == 'member' and event.old_chat_member.status != 'member':
            await self.delete_system_message(event)

        elif event.new_chat_member.status == 'left' and event.old_chat_member.status == 'member':
            await self.delete_system_message(event)

    async def delete_system_message(self, event: ChatMemberUpdated):
        logging.debug(f"Attempting to remove system message")
        if event.message and hasattr(event.message, 'message_id'):
            await self.delete_message(event.chat.id, event.message.message_id)
            logging.info(f"Removed system message ID {event.message.message_id}")

    async def handle_message(self, message: types.Message):
        logging.debug(f"Received message: {message.text}")
        
        if message.new_chat_members:
            for member in message.new_chat_members:
                logging.info(f"User {member.id} joined the chat")
                await self.delete_message(message.chat.id, message.message_id)

        if message.left_chat_member:
            logging.info(f"User {message.left_chat_member.id} left the chat")
            await self.delete_message(message.chat.id, message.message_id)

        if hasattr(message, 'text') and message.text and message.text != '':
            await self.handle_stop_words(message)

    async def handle_stop_words(self, message: types.Message):
        STOP_WORDS = ['@OrOpremkabot']
        if any(stop_word.lower() in message.text.lower() for stop_word in STOP_WORDS):
            logging.info(f"Message contains stop word, user will be banned: {message.from_user.id}")
            
            await self.delete_message(message.chat.id, message.message_id)
            logging.info(f"Message {message.message_id} deleted")
            
            await self.ban_user(message.chat.id, message.from_user.id)
            logging.info(f"User {message.from_user.id} banned")

    async def handle_unhandled_updates(self, update: types.Update):
        logging.info(f"Unhandled update: {update}")

    async def start(self):
        try:
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logging.error(f"An error occurred during polling: {e}")

if __name__ == '__main__':
    chat_keeper_bot = ChatKeeperBot(API_TOKEN)
    asyncio.run(chat_keeper_bot.start())
