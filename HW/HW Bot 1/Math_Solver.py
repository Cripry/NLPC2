import telebot
from operator import pow, truediv, mul, add, sub  



bot = telebot.TeleBot('5114637735:AAHpf9C0Lp6-0EgmTM7H8vevO4hxHiDURJ4')


@bot.message_handler(regexp='.+')
def response(message):
    
    operators = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv
    }

    def calculate(s):
        if s.isdigit():
            return float(s)
        
        for c in operators.keys():
            left, operator, right = s.partition(c)
            if operator in operators:
                return operators[operator](calculate(left), calculate(right))


    if "+" in message.text or '-' in message.text or '/' in message.text or '*' in message.text:
    
        try:
            answer = calculate(message.text)
        except (SyntaxError, TypeError):
            answer = 'Your string is invalid, please check it again'
            
        if not answer:
            answer = 'Your string is invalid, please check it again'
    else:
        answer = 'Your string is invalid, please check it again'
            
    bot.reply_to(message, answer)
    
bot.infinity_polling()



