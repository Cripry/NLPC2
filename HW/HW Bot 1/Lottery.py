import telebot


bot = telebot.TeleBot('5114637735:AAHpf9C0Lp6-0EgmTM7H8vevO4hxHiDURJ4')
types = telebot.types
import random

def get_global_data():

    global markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    
    global lucky_number
    lucky_number = str(random.randint(0,100))
    non_lucky_numbers = [str(random.randint(0,100)) for _ in range(3)]

    while True:
        if lucky_number in non_lucky_numbers:
            lucky_number = str(random.randint(0,100))
        else:
            break

    global joined_numbers
    joined_numbers = non_lucky_numbers + [lucky_number]

    random.shuffle(joined_numbers)

    buttons_list = []
    for number in joined_numbers:
        buttons_list.append(types.KeyboardButton(number))
        
    btn1, btn2, btn3, btn4 = buttons_list

    markup.row(btn1, btn2)
    markup.row(btn3, btn4)



@bot.message_handler(commands=['fortuna'])
def fortuna(message):
    
    get_global_data()
    bot.send_message(message.chat.id, 'Alegeti un numar', reply_markup=markup)
    

@bot.message_handler(func=lambda m: m.text in joined_numbers)
def go_to(message):
    if message.text == lucky_number:
        bot.reply_to(message, 'Felicitări, ați ales numărul corect ! Sunteți norocos !')
    else:
        bot.reply_to(message, f'Ehh.. păcat, nu ați ales numărul corect. Trebuia {lucky_number}')


bot.infinity_polling()