import cv2
from aiogram import Bot, Dispatcher, executor, types
from config import token

bot = Bot(token)
dp = Dispatcher(bot)

start_text = '''<em>Здравствуй, этот бот ищет лица на фотографии
👦👳🏻‍♂️👶🏻🧔🏿‍♂️👧🏽👩🏼‍🦰
Как это работает?:)
Ты отправляешь нам изображение, мы выделяем в нем лица, все просто😊</em>'''

start_markup = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton('Начать' , callback_data='старт')
start_markup.add(button1)


@dp.message_handler(commands=['start'])
async def hello(message: types.Message):
   await bot.send_message(message.chat.id, start_text ,parse_mode='HTML', reply_markup=start_markup)


@dp.message_handler(content_types='photo')
async def face(message: types.Message):

   face = cv2.CascadeClassifier('face_detector.xml')

   await message.photo[-1].download(destination_file='smile.jpg')
   img = cv2.imread('smile.jpg')
   gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   result = face.detectMultiScale(gray_img, scaleFactor=1.75, minNeighbors=1)

   num = 0
   smile = cv2.imread('smile.png')
   for (x , y ,w , h) in result:
      res_smile = cv2.resize(smile , (w,h))
      img[y:y+h , x:x+w] = res_smile
      num+=1

   cv2.imwrite('./new_img.jpg', img)

   photo = open('new_img.jpg' , 'rb')
   await message.answer_photo(photo)
   await message.answer(f'Количество обнаруженных на фото лиц: {num}')


@dp.callback_query_handler()
async def callback(callback:types.CallbackQuery):
   if callback.data == 'старт':
      await callback.bot.send_message(callback.message.chat.id , '<em>Отправь нам фото, в котором отчетливо видны лица</em>', parse_mode='HTML')
      await callback.answer('ждем фоток')
executor.start_polling(dp)