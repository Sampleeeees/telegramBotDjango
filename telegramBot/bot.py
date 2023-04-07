import secrets
import asyncpg
import io
from io import BytesIO
from PIL import Image
from typing import List
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from telegramBotDjango.settings import BOT_KEY, DATABASES

bot = Bot(token=BOT_KEY)
dp = Dispatcher(bot)


async def connect_to_db():
    db_config = DATABASES['default']
    conn = await asyncpg.connect(
        user=db_config['USER'],
        password=db_config['PASSWORD'],
        host=db_config['HOST'],
        database=db_config['NAME']
    )
    return conn


async def save_user_data(user_data):
    conn = await connect_to_db()

    try:
        await conn.execute(
            'INSERT INTO tgbot_manage_telegramuser (id, username, first_name, last_name, password, photo) '
            'VALUES ($1, $2, $3, $4, $5, $6)',
            user_data['id'],
            user_data['username'],
            user_data['first_name'],
            user_data['last_name'],
            user_data['password'],
            memoryview(user_data['photo'])
        )
    finally:
        await conn.close()



@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(
        f"Вітаю, {message.from_user.full_name}, я створений для реєстрації користувачів сайту\n"
        "\nОбери команду в menu👇",)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer(
        "Щоб зараєструватись обери кнопку '/registration'\n"
        "\nТакож якщо ти зареєстрований то можеш себе видалити з бази командою '/delete_me'"
    )


@dp.message_handler(commands=['registration'])
async def process_registration_command(msg: types.Message):
    conn = await connect_to_db()

    try:
        result = await conn.fetchrow(
            'SELECT id FROM tgbot_manage_telegramuser WHERE id = $1',
            msg.from_user.id
        )
        if result:
            await msg.answer("Ви вже зареєстровані.")
            return

        profile_photos = await msg.from_user.get_profile_photos()

        if not profile_photos.photos:
            # Якщо у користувача немає фото, то виходимо
            await msg.answer('У вас немає фото')
            return

        last_photo = profile_photos.photos[-1][-1]

        photo_bytes = BytesIO()
        await last_photo.download(destination_file=photo_bytes)
        photo_bytes.seek(0)

        password = secrets.token_urlsafe(8)

        user_data = {
            'id': msg.from_user.id,
            'username': msg.from_user.username,
            'first_name': msg.from_user.first_name,
            'last_name': msg.from_user.last_name,
            'password': password,
            'photo': photo_bytes.getvalue()
        }


        await save_user_data(user_data)

        registration_message = (
            f"Вітаємо, {msg.from_user.first_name}!\n"
            f"Ви успішно зареєстровані на нашому сервісі.\n"
            f"Ваш логін: {msg.from_user.username}\n"
            f"Ваш пароль: {password}"
        )

        await msg.answer(registration_message)
    finally:
        await conn.close()

@dp.message_handler(commands=['delete_me'])
async def delete_user_from_db(msg: types.Message):
    conn = await connect_to_db()

    try:
        user_id = msg.from_user.id
        # перевіряємо, чи існує користувач з вказаним id
        res = await conn.fetch('SELECT * FROM tgbot_manage_telegramuser WHERE id = $1', user_id)
        if res:
            # якщо користувач існує, то видаляємо його з бази даних
            await conn.execute('DELETE FROM tgbot_manage_telegramuser WHERE id = $1', user_id)
            await msg.answer('Ти успішно видалений')
        else:
            # якщо користувач не існує, повідомляємо про це
            await msg.answer('Користувач з таким id не існує в базі даних')
    finally:
        await conn.close()






