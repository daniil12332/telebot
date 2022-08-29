from re import T
import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types

bot = telebot.TeleBot("5467348981:AAGukG6UAvcSfyRAGNDfD8_jhKOJThtayNE")
url = "https://habr.com/ru/news/"
url2 = "https://habr.com/ru/all/"

response = requests.get(url)
response.raise_for_status()

response2 = requests.get(url2)
response2.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")
tag2 = soup.find_all("article", class_="tm-articles-list__item")

soup2 = BeautifulSoup(response2.text, "lxml")
tag = soup2.find_all("article", class_="tm-articles-list__item")

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, "Bot is started.")

page = 0
pages = []

def markUP(pages, page):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_url = types.InlineKeyboardButton(text="Go to habr.", url=pages[page][1])
    btn_next = types.InlineKeyboardButton(text="Next page.", callback_data="habr_next")
    btn_back = types.InlineKeyboardButton(text="Back page.", callback_data="habr_back")
    markup.add(btn_back, btn_next, btn_url)
    return markup

@bot.callback_query_handler(func=lambda call:True)
def call_repley(call):
    global page
    global pages
    if call.message and call.data == "habr_back":
        page -= 1
        try:
            markup = markUP(pages=pages, page=page)
            bot.edit_message_text(pages[page][0], reply_markup = markup, chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            bot.answer_callback_query(call.id, show_alert=True, text="Такой статьи нету.")
            page += 1
    if call.message and call.data == "habr_next":
        page += 1
        try:
            markup = markUP(pages=pages, page=page)
            bot.edit_message_text(pages[page][0], reply_markup = markup, chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            bot.answer_callback_query(call.id, show_alert=True, text="Такой статьи нету.")
            page -= 1

@bot.message_handler(commands=["habr"])
def habr(message):
    global page
    global pages
    page = 0
    pages = []
    response = requests.get(url2)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    tag2 = soup.find_all("article", class_="tm-articles-list__item")
    for i in range(0, 10):
        out = tag2[i].find("h2").find("span").text
        urlOut = "https://habr.com" + tag2[i].find("h2").find("a").get("href")
        pages.append([out, urlOut])
    markup = markUP(pages=pages, page=page)
    bot.send_message(message.chat.id, pages[page][0], reply_markup=markup)

@bot.message_handler(commands=["news"])
def habrNews(message):
    global page
    global pages
    page = 0
    pages = []
    response2 = requests.get(url)
    response2.raise_for_status()
    soup2 = BeautifulSoup(response2.text, "lxml")
    tag = soup2.find_all("article", class_="tm-articles-list__item")
    for i in range(0, 10):
        out = tag[i].find("h2").find("span").text
        urlOut = "https://habr.com" + tag[i].find("h2").find("a").get("href")
        pages.append([out, urlOut])
    markup = markUP(pages=pages, page=page)
    bot.send_message(message.chat.id, pages[page][0], reply_markup=markup)

bot.polling(none_stop=True, interval=0)