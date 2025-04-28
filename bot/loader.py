import os
import sys
import time
from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2

BASE_DIR = Path(__file__).parent.resolve()

import logging.config



# Создаем папки для логов
log_err_dir = BASE_DIR / "logs" / "err"
log_out_dir = BASE_DIR / "logs" / "out"

log_err_dir.mkdir(parents=True, exist_ok=True)
log_out_dir.mkdir(parents=True, exist_ok=True)

# Конфигурация логгера
logging.config.fileConfig(
    BASE_DIR / "logging.conf",
    defaults={
        "err_log_file": (log_err_dir / "err.log").as_posix(),
        "out_log_file": (log_out_dir / "out.log").as_posix()
    },
    disable_existing_loggers=False
)

logger = logging.getLogger(f"root.{__name__}")

BOT_TOKEN = os.getenv("BOT_TOKEN")

if BOT_TOKEN is None:
    logger.error("Can't find BOT_TOKEN env variable")
    sys.exit()

bot = Bot(BOT_TOKEN, parse_mode="HTML")
try:
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = 6379
    redis_db = 1
    storage = RedisStorage2(host=redis_host, port=redis_port, db=redis_db, prefix='fsm', data_ttl=1800, state_ttl=1800,
                            pool_size=100)
    dp = Dispatcher(bot=bot, storage=storage)
    logger.info("Redis connected. Dispatcher initialized successfully.")
except Exception as e:
    logger.error(f"No connection to redis. Error: {e}")



ADMINS_IDS = os.getenv("ADMINS_IDS")
admins = []
if ADMINS_IDS is not None:
    logger.info("Admins found. Parse admins IDs")
    admins = ADMINS_IDS.split(",")
    admins = [admin for admin in admins if admin != ""]

django_start = False

from login import get_token


while django_start is False:
    try:
        token = get_token()
        django_start = True
        logger.info("Successfully connected to Django and received token.")
    except Exception as e:
        logger.warning(f"Waiting for Django to start... Error: {e}")
        time.sleep(3)
