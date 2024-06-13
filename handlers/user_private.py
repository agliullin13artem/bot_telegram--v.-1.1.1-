
from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.formatting import as_list, as_marked_section, Bold


from filters.chat_types import ChatTypeFilter

from kbds import reply


# создаем роутер
user_private_router = Router()
# фильр для приватного чата
user_private_router.message.filter(ChatTypeFilter(['private']))


# ответ на /start и кнопки "меню", "о нас", "варианты оплаты", "варианты доставки" передаю кнопки в клавиатуру
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привет! Я бот. Напиши мне что-нибудь и я тебе отвечу!', reply_markup=reply.start_kb3.as_markup(
        resize_keyboard=True, input_field_placeholder='Что вас интересует?'
    )) 


# команда /menu
# @user_private_router.message(F.text.lower() == 'меню')
@user_private_router.message(or_f(Command('menu'), (F.text.lower() == 'меню')))
async def menu_cmd(message: types.Message):
    await message.answer('Вот меню:', reply_markup=reply.del_kbd) # если пользователь выберет /menu то удаляем клавиатуру
    # await message.reply(message.text) # ответ эхом но именно по имени к пользователю


# команда /about
@user_private_router.message(F.text.lower() == 'о магазине')
@user_private_router.message(Command('about'))
async def abount_cmd(message: types.Message):
    await message.answer('О нас:')


# команда /payment
@user_private_router.message(F.text.lower() == 'варианты оплаты')
@user_private_router.message(Command('payment'))
async def payment_cmd(message: types.Message):

    # формируем разметку с помощью функции as_marked_section варианты 
    text = as_marked_section(
        Bold('Варианты оплаты:'),
        'Картой в боте', 
        'При получении карта/кеш',
        'В заведении',
        marker='✅ ')

    await message.answer(text.as_html())



# команда /shipping варианты доставки
@user_private_router.message((F.text.lower().contains('доставк')) | (F.text.lower() == ('варианты доставки'))) # сравниваем с текстом сообщения
@user_private_router.message(Command('shipping'))
async def shipping_cmd(message: types.Message):

    text = as_list(
        as_marked_section(
        Bold('Варианты доставки/заказа:'),
        'Курьером',
        'Самовывоз',
        'Покушаю у вас',
        marker='✅ '
        ),
        as_marked_section(
        Bold('Нельзя:'),
        'Почта',
        'Голуби',
        marker='❌ '
        ),
        sep='\n-----------------------------------------\n')
    
    
    await message.answer(text.as_html())


#  команда /echo
# @user_private_router.message(F.text)
# async def echo_cmd(message: types.Message):
#     await message.answer(message.text)


# получаем номер телефона 
@user_private_router.message(F.contact)
async def get_contact(message: types.Message):
    await message.answer(f'Ваш телефон: {message.contact.phone_number}')
    await message.answer(str(message.contact))

# тут получаю локацию
@user_private_router.message(F.location)
async def get_location(message: types.Message):
    await message.answer(f'Ваше местоположение: {message.location.latitude}, {message.location.longitude}')
    await message.answer(str(message.location))



@user_private_router.message((F.text.lower().contains('данны')) | (F.text.lower() == ('Мои данные')))
@user_private_router.message(Command('data'))
async def abount_cmd(message: types.Message):
    await message.answer('Ваши данные:', reply_markup=reply.test_kb
    )