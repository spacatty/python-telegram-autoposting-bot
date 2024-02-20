from telethon.sync import TelegramClient
from dotenv import load_dotenv
from db import DBController
import time, asyncio, os
from logger import logger
from telethon.tl import functions, types
import json
import jsonpickle

from apscheduler.schedulers.asyncio import AsyncIOScheduler

class CustomMessageType:
    def __init__(self, message, media, id) -> None:
        self.message = message
        self.media = media
        self.id = id


async def poll_messages():
    for channel in channel_list:
        for message in await client.get_messages(channel):
            if  DBC.is_unique_message(message, channel):
                    if message.message and any(x in message.message for x in FILTER):
                        return
                    else:
                        DBC.add_message(CustomMessageType(id=message.id, message=message.message, media=jsonpickle.encode(message.media)), channel)
                        logger.custom(f"Found and registered message from channel @{channel}")

async def send_messages():
    unsent_messages = DBC.get_unsent_messagess()
    if len(unsent_messages) > 0:
        for id, message, channel, _, object in unsent_messages:
            try:
                decoded = jsonpickle.decode(object)
                decoded.media = jsonpickle.decode(decoded.media)
                if decoded.message or decoded.media:
                    await client.send_message(HOST_CHANNEL, types.Message(id=decoded.id, media=decoded.media, message=decoded.message))
                    logger.custom(f"Sent message {message} from {channel} (ID {id})")
                    DBC.update_message_status(id)
            except Exception as e:
                print(e)
                logger.error(e)
                logger.custom(f"FAILED to send message {message} from {channel} (ID {id})")


if __name__ == "__main__":
    jsonpickle.set_decoder_options('simplejson', encoding='utf8')
    jsonpickle.set_encoder_options('simplejson', encoding='utf8')


    load_dotenv()
    DBC = DBController()
    DBC.init_table()

    APP_ID = os.getenv('APP_ID')
    API_HASH = os.getenv('API_HASH')
    HOST_CHANNEL = os.getenv("HOST_CHANNEL")
    CHANNELS = os.getenv("CHANNELS")
    channel_list = CHANNELS.replace(", ", ",").split(",")
    FILTER = ["реклама", "://", "t.me/", "@"]

    client = TelegramClient("myAppSession", APP_ID, API_HASH, system_version="4.16.30-vxCUSTOM", flood_sleep_threshold=0)

    client.start()

    poll_scheduler = AsyncIOScheduler()
    poll_scheduler.add_job(poll_messages, 'interval', seconds=10)
    poll_scheduler.add_job(send_messages, 'interval', seconds=5)

    poll_scheduler.start()
    logger.custom(f"Scheduler started, found {len(channel_list)} channels")

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        DBC.close_connection()