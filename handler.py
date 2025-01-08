import pandas as pd
from datetime import datetime as dt
from datetime import timedelta as td
import telebot
from tabulate import tabulate
#import aspose.words as aw
from config import token
current_date = dt.now()
ten_days = td(10)
next_date = current_date + ten_days
df = pd.read_excel('данные.xlsx')
#print(df.columns)
#print(df.dtypes)
df['Дата'] = pd.to_datetime(df['Дата'])
#print(df.dtypes)
#print(df.sample)
df_filtered = df[df['Дата'] >= current_date] #next_date >= 
df_filtered = df_filtered[df_filtered['Дата'] <= next_date]
#print(df_filtered.sample)
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.reply_to(message, "Привет! Я бот. Для получения расписания пришлите название группы.")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    grupp_name = message.text.strip()

    # Загружаем данные из Excel-таблицы

    # Ищем статус заказа по номеру
    df_raspisanie = df_filtered[df_filtered['Группа'] == grupp_name]

    if len(df_raspisanie) > 0:
        bot.reply_to(message, f"Расписание для группы {grupp_name} на ближайшие 10 дней: ")
        stroka = tabulate(df_raspisanie, headers='keys', tablefmt='html', maxcolwidths=[None, 15])
        with open('rasp.html', 'w') as file_output:
            file_output.write(stroka)
        bot.send_document(message.chat.id, open(r'rasp.html', 'rb'))
    else:
        bot.reply_to(message, f"Группа: {grupp_name} не найдена.")







# Запускаем бота
bot.polling()