import asyncio
from telethon import TelegramClient
import random
import time
import logging

# Логи, чтобы видеть каждый шаг, сука
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Твои данные, перепроверь, епта
API_ID = ''  # С my.telegram.org
API_HASH = ''  # Оттуда же
PHONE = '+777777777'  # Например, +79991234567
TEXT_TO_SPAM = "сюда текст"  # Твой текст
DELAY_MIN = 1 #раставь промежуток по секундам между спамами в чат
DELAY_MAX = 2

# Список каналов, кидай сюда все свои, блять
TARGET_CHATS = [

    '@сюда чат',
    '@сюда тоже',
    '@и сюда',
    '@', #Можете подобным образом накопировать и добавить ещё больше чатов
]

# Клиент с устройством и системой
client = TelegramClient(
    'spammer_session',
    API_ID,
    API_HASH,
    device_model="iPhone 15 Pro", #не трогай!
    system_version="IOS 10.1",
)


async def get_entity(chat):
    """Проверяем, можем ли достать чат"""
    try:
        entity = await client.get_entity(chat)
        logger.info(f"Чат {chat} найден!")
        return entity
    except Exception as e:
        logger.error(f"Не могу найти или получить доступ к {chat}: {e}")
        return None


async def get_last_message(chat_entity):
    """Достаём последнее сообщение в чате"""
    try:
        messages = await client.get_messages(chat_entity, limit=1)
        if messages and len(messages) > 0:
            last_message = messages[0]
            logger.info(f"Последнее сообщение в {chat_entity} найдено, ID: {last_message.id}")
            return last_message
        else:
            logger.info(f"В {chat_entity} нет сообщений")
            return None
    except Exception as e:
        logger.error(f"Ошибка при получении последнего сообщения в {chat_entity}: {e}")
        return None


async def spam_the_fuck_out_of_chats():
    logger.info("Бот поехал")
    while True:
        for chat in TARGET_CHATS:
            logger.info(f"Пробую отправить в {chat}")
            entity = await get_entity(chat)
            if entity:
                try:
                    # Достаём последнее сообщение
                    last_message = await get_last_message(entity)

                    delay = random.uniform(DELAY_MIN, DELAY_MAX)
                    logger.info(f"Жду {delay:.2f} сек перед отправкой в {chat}")
                    await asyncio.sleep(delay)

                    # Если есть последнее сообщение, отвечаем на него
                    if last_message:
                        await client.send_message(
                            entity,
                            TEXT_TO_SPAM,
                            reply_to=last_message.id
                        )
                        logger.info(f"Ответил на сообщение ID {last_message.id} в {chat}")
                    else:
                        # Если нет сообщений, просто отправляем
                        await client.send_message(entity, TEXT_TO_SPAM)
                        logger.info(f"Отправил в {chat} без ответа")
                except Exception as e:
                    logger.error(f"Ошибка при отправке в {chat}: {e}")
            else:
                logger.warning(f"Пропускаю {chat}, нет доступа или не найден!")
        logger.info("Прошёл круг по чатам, жду перед следующим, блять!")
        await asyncio.sleep(random.uniform(30, 60))


async def main():
    # Проверяем, залогинены ли
    if not await client.is_user_authorized():
        logger.info("Не залогинен")
        await client.start(phone=PHONE)
        logger.info("Залогинился")
    else:
        logger.info("Уже залогинен")

    me = await client.get_me()
    logger.info(f"Ты {me.username or me.first_name}, всё заебись!")

    # Сразу спам
    await spam_the_fuck_out_of_chats()


if __name__ == '__main__':
    try:
        with client:
            client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Ты вырубил, сессия цела, епта!")
    except Exception as e:
        logger.error(f"Сломалось: {e}")