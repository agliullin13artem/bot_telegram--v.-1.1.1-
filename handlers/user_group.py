from string import punctuation


from aiogram import Router, types
from filters.chat_types import ChatTypeFilter

user_group_router = Router()

# фильтр для чатов в группе и супергруппе
user_group_router.message.filter(ChatTypeFilter(['group', 'supergroup']))


# запрещенные слова
restricted_words = {'лох', 'хуй', 'пидор', 'гондон', 'гандон', 'пизда','еблан', 'иди на хуй', 'пошел на хуй', 'блять', 'сука'}


# метод чистки текс что бы не было запрещенных слов например ло!х что бы не замаскировали
def clean_text(text: str) -> str:
    return text.translate(str.maketrans('', '', punctuation))


# выявлеие запрещенных слов в групповом чате
@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f'{message.from_user.first_name}, соблюдайте правила в чате не материтесь!')
        await message.delete()
        # await message.chat.ban(message.from_user.id) # блокировка пользователя
