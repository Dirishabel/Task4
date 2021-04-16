import sqlite3

import telebot
from newsapi import NewsApiClient
from telebot import types

from db_connector import sql
from messages import MESSAGES

list_hello = ("Привет", "Здравствуй", "Hello")
bot = telebot.TeleBot("1772232476:AAG-4CkgpaYp8gH49OoemonnyreJerzFkDI")
newsapi = NewsApiClient(api_key='bf8f4d7bff7346729ec5bd55856a1591')


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('Ключевые слова')
    btn2 = types.KeyboardButton('Подписки')
    btn3 = types.KeyboardButton('Новости по ключевым словам')
    btn4 = types.KeyboardButton('Новости по подпискам')
    markup.add(btn1, btn2, btn3, btn4)
    if not sql('select_one', 'select_user', (message.from_user.id,)):
        sql('insert', 'insert_user', (
            message.from_user.id,
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.username,
            message.from_user.language_code,
        )
        )
    bot.send_message(message.from_user.id, MESSAGES['hello_msg'].format(
        message.from_user.first_name), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'key_add':
        key_name = bot.send_message(
            call.message.chat.id, 'Введите ключевое слово:')
        bot.register_next_step_handler(key_name, add_key)
    elif call.data == 'key_delete':
        key_name = bot.send_message(
            call.message.chat.id, 'Введите ключевое слово, которое подлежит удалению:')
        bot.register_next_step_handler(key_name, del_key)
    elif call.data == 'subs_add':
        sources = newsapi.get_sources()
        for source in sources['sources'][:10]:
            if source['language'] in ('en', 'ru',):
                subscribe_div = types.InlineKeyboardMarkup()
                callback_string = 'sbc#' + source['name'] + '#' + source['id']
                sub_btn = types.InlineKeyboardButton(
                    text='Подписаться', callback_data=callback_string)
                subscribe_div.add(sub_btn)
                bot.send_message(
                    call.message.chat.id,
                    source['description'],
                    reply_markup=subscribe_div
                )
    elif ((call.data).split('#'))[0] == 'sbc':
        if not sql('select_one', 'is_user_subscribe', (call.message.chat.id, ((call.data).split('#'))[1],)):
            sql('insert', 'add_subscribe',
                (call.message.chat.id, ((call.data).split('#'))[1], ((call.data).split('#'))[2],))
            message_sub = 'Подписка на {0} успешно оформлена'.format(
                ((call.data).split('#'))[1])
        else:
            message_sub = 'Вы уже подписаны на эту рассылку.'
        bot.send_message(
            call.message.chat.id,
            message_sub,
        )
    elif call.data == 'subs_delete':
        sub_list = sql('select_all', 'get_user_subscribes',
                       (call.message.chat.id,))
        sub_delete_keyboard = types.InlineKeyboardMarkup()
        for sub in sub_list:
            sub_delete = types.InlineKeyboardButton(
                text=sub[0], callback_data='subdelete#'+sub[0])
            sub_delete_keyboard.add(sub_delete)
        bot.send_message(
            call.message.chat.id,
            'Выберите подписку, которую хотите удалить:',
            reply_markup=sub_delete_keyboard
        )
    elif ((call.data).split('#'))[0] == 'subdelete':
        response = sql('delete', 'delete_subscribe', (
            call.message.chat.id,
            ((call.data).split('#'))[1],
        ))
        if response is not None:
            msg_text = 'Удаление прошло успешно!'
        else:
            msg_text = 'Удалить подписку не удалось, попробуйте позже'
        bot.send_message(
            call.message.chat.id,
            msg_text,
        )


def add_key(message):
    if not sql('select_one', 'is_user_keyword', (message.from_user.id, message.text,)):
        response = sql('insert', 'insert_keyword',
                       (message.from_user.id, message.text,))
        if response:
            msg_response = 'Ключевое слово {0} добавлено в список.'.format(
                message.text)
        else:
            msg_response = 'Не удалось добавить слово в список.'
    else:
        msg_response = 'У вас уже есть это ключевое слово.'
    bot.send_message(message.from_user.id, msg_response)


def del_key(message):
    response = sql('delete', 'delete_keyword',
                   (message.from_user.id, message.text,))
    if response is not None:
        msg_response = 'Ключевое слово {0} удалено из списка.'.format(
            message.text)
    else:
        msg_response = 'Не удалось удалить слово {0}, т.к. его не существует у текущего пользователя.'.format(
            message.text)
    bot.send_message(message.from_user.id, msg_response)


@bot.message_handler(content_types=['text'])
def handle_button(message):
    if message.text == 'Ключевые слова':
        key_keyboard = types.InlineKeyboardMarkup()
        key_add = types.InlineKeyboardButton(
            text='Добавить', callback_data='key_add')
        key_delete = types.InlineKeyboardButton(
            text='Удалить', callback_data='key_delete')
        key_keyboard.add(key_add)
        key_keyboard.add(key_delete)
        user_keywords = sql('select_all', 'get_user_keywords',
                            (message.from_user.id,))
        keywords_list = ''
        for add_word in user_keywords:
            keywords_list += '- '+add_word[0]+'\n'
        bot.send_message(
            message.from_user.id,
            'На данный момент вы отслеживаете данные ключевые слова:\n'+keywords_list,
            reply_markup=key_keyboard
        )

    elif message.text == 'Подписки':
        subs_keyboard = types.InlineKeyboardMarkup()
        subs_add = types.InlineKeyboardButton(
            text='Добавить', callback_data='subs_add')
        subs_delete = types.InlineKeyboardButton(
            text='Удалить', callback_data='subs_delete')
        subs_keyboard.add(subs_add)
        subs_keyboard.add(subs_delete)
        user_subscribes = sql('select_all', 'get_user_subscribes',
                              (message.from_user.id,))
        subscribes_list = ''
        for add_word in user_subscribes:
            subscribes_list += '- '+add_word[0]+'\n'
        bot.send_message(
            message.from_user.id,
            'На данный момент вы подписаны на:\n'+subscribes_list,
            reply_markup=subs_keyboard
        )

    elif message.text == 'Новости по ключевым словам':
        key_list = sql('select_all', 'get_user_keywords',
                       (message.from_user.id,))
        q_string = ''
        for key in key_list:
            q_string += key[0]+' OR '
        if q_string:
            top_headlines = newsapi.get_top_headlines(q=q_string)
            if len(top_headlines['articles']) != 0:
                for top_new in top_headlines['articles'][:10]:
                    new_text = top_new['title']+'\n'+top_new['description']
                    if top_new['urlToImage']:
                        bot.send_photo(message.from_user.id,
                                       top_new['urlToImage'], caption=new_text)
                    else:
                        bot.send_message(
                            message.from_user.id,
                            new_text,
                        )
            else:
                bot.send_message(
                    message.from_user.id,
                    'На данный момент нет новых новостей',
                )
        else:
            bot.send_message(
                message.from_user.id,
                'На данный момент у вас еще нет ключевых слов',
            )

    elif message.text == 'Новости по подпискам':
        tag_list = sql('select_all', 'get_user_subscribe_id',
                       (message.from_user.id,))
        sources_string = ''
        for tag in tag_list:
            sources_string += tag[0]+','
        if sources_string:
            top_headlines = newsapi.get_top_headlines(sources=sources_string)
            if len(top_headlines['articles']) != 0:
                for top_new in top_headlines['articles'][:10]:
                    new_text = top_new['title']+'\n'+top_new['description']
                    if top_new['urlToImage']:
                        bot.send_photo(message.from_user.id,
                                       top_new['urlToImage'], caption=new_text)
                    else:
                        bot.send_message(
                            message.from_user.id,
                            new_text,
                        )
            else:
                bot.send_message(
                    message.from_user.id,
                    'На данный момент нет новых новостей',
                )

        else:
            bot.send_message(
                message.from_user.id,
                'На данный момент у вас еще нет подписок',
            )
    else:
        bot.send_message(message.from_user.id, MESSAGES['err_msg'])


bot.polling()
