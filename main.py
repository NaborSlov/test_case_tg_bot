import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

from utils import convert_mp3_to_wav, search_face

load_dotenv()

API_TOKEN = os.environ.get('API_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=["start"])
async def send_start_message(message: types.Message):
    await message.reply("Привет!\nЭтот бот умеет сохранять аудио сообщения\nи фотографии с людьми.")


@dp.message_handler(content_types=[types.ContentType.VOICE])
async def audio(message: types.Message):
    file = await bot.get_file(file_id=message.voice.file_id)
    file_path = f"data/{message.from_id}/audio/audio_message_{message.message_id}.wav"
    await bot.download_file(file_path=file.file_path, destination=file_path, make_dirs=True)
    convert_mp3_to_wav(file_path)
    await message.answer("Файл загружен и конвертирован")


@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def photo(message: types.Message):
    photo_id = message.photo[-1].file_id
    file_path = f"data/{message.from_id}/photo/photo_{photo_id}.jpeg"
    file = await bot.get_file(file_id=photo_id)
    await bot.download_file(file_path=file.file_path,
                            destination=file_path,
                            make_dirs=True)

    if not search_face(file_path):
        os.remove(file_path)
        await message.answer("Не удалось сохранить фото")
    else:
        await message.answer("Фото сохранено")


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)
