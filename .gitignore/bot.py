import telebot
from telebot import types

bot = telebot.TeleBot('1650807306:AAGx6OJGgQm889ZETa4GgS6svdCfUATyg_M')
my_list = dict()
my_description_list = dict()


@bot.message_handler(commands=['start'])
def start(message):
    global my_list
    if message.from_user.first_name not in my_list:
        my_list[message.from_user.first_name] = []
        my_description_list[message.from_user.first_name] = []
    if len(my_list[message.from_user.first_name]) == 0:
        send_mess = 'Your to-do list is empty for today. Click on the button below to add a new task!'
    else:
        send_mess = '\n'.join(my_list[message.from_user.first_name])
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton('add')
    btn2 = types.KeyboardButton('delete')
    btn3 = types.KeyboardButton('show')
    btn4 = types.KeyboardButton('clean')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def mess(message):
    global my_list
    global my_description_list
    get_message_bot = message.text.strip().lower()
    if get_message_bot == "add":
        bot.send_message(message.from_user.id, "Write your task!")
        bot.register_next_step_handler(message, get_li)
    elif get_message_bot == "clean":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('yes')
        btn2 = types.KeyboardButton('no')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Are you sure you want to clear your to-do list?', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, clear_list)
    elif get_message_bot == "delete":
        if len(my_list[message.from_user.first_name]) == 0:
            bot.send_message(message.from_user.id, 'Your list is empty!')
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=False, row_width=3)
            for i in my_list[message.from_user.first_name]:
                markup.add(types.KeyboardButton(i))
            final_message = "Click on the task you want to delete!"
            bot.send_message(message.chat.id, final_message, parse_mode='html', reply_markup=markup)
            bot.register_next_step_handler(message, del_task)
    elif get_message_bot == "show":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        for i in my_list[message.from_user.first_name]:
            markup.add(types.KeyboardButton(i))
        bot.send_message(message.chat.id, 'Click on the button below!', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, show_de)
    else:
        bot.send_message(message.from_user.id, 'I do not understand you')


def get_li(message):
    global my_list
    li = str(len(my_list[message.from_user.first_name]) + 1) + '. ' + message.text
    my_list[message.from_user.first_name].append(li)
    bot.send_message(message.from_user.id, 'Write a description of your task!')
    bot.register_next_step_handler(message, get_de)


def get_de(message):
    global my_list
    global my_description_list
    de = message.text
    my_description_list[message.from_user.first_name].append(de)
    bot.send_message(message.from_user.id, "\n".join(my_list[message.from_user.first_name]))


def del_task(message):
    global my_list
    global my_description_list
    li = message.text.strip().lower()
    for i in range(my_list[message.from_user.first_name].index(li) + 1, len(my_list[message.from_user.first_name])):
        x = my_list[message.from_user.first_name][i]
        j = 0
        num = ''
        while x[j] != '.':
            num += x[j]
            j += 1
        my_list[message.from_user.first_name][i] = str(int(num) - 1) + x[j:]
    my_description_list[message.from_user.first_name].pop(my_list[message.from_user.first_name].index(li))
    my_list[message.from_user.first_name].remove(li)
    if len(my_list[message.from_user.first_name]) > 0:
        bot.send_message(message.from_user.id, 'Your to-do list for today')
        bot.send_message(message.from_user.id, '\n'.join(my_list[message.from_user.first_name]))
    else:
        bot.send_message(message.from_user.id, 'Your to-do list is empty for today)')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton('add')
    btn2 = types.KeyboardButton('delete')
    btn3 = types.KeyboardButton('show')
    btn4 = types.KeyboardButton('clean')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, 'Click on the button below!', parse_mode='html', reply_markup=markup)


def show_de(message):
    global my_list
    global my_description_list
    s = message.text.strip().lower()
    ind = my_list[message.from_user.first_name].index(s)
    bot.send_message(message.from_user.id, my_description_list[message.from_user.first_name][ind])
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton('add')
    btn2 = types.KeyboardButton('delete')
    btn3 = types.KeyboardButton('show')
    btn4 = types.KeyboardButton('clean')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, 'Click on the button below!', parse_mode='html', reply_markup=markup)


def clear_list(message):
    global my_list
    global my_description_list
    ans = message.text.strip().lower()
    if ans == 'yes':
        my_list[message.from_user.first_name] = []
        my_description_list[message.from_user.first_name] = []
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('add')
        btn2 = types.KeyboardButton('delete')
        btn3 = types.KeyboardButton('show')
        btn4 = types.KeyboardButton('clean')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Your to-do list is empty again. Click on the button below to add a new task.', parse_mode='html', reply_markup=markup)
    elif ans == 'no':
        bot.send_message(message.from_user.id, 'ok, your list for today:' + '\n' + '\n'.join(my_list[message.from_user.first_name]))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('add')
        btn2 = types.KeyboardButton('delete')
        btn3 = types.KeyboardButton('show')
        btn4 = types.KeyboardButton('clean')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Click on the button below!', parse_mode='html', reply_markup=markup)


bot.polling(none_stop=True)
