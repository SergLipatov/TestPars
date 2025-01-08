from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import pandas as pd
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("detach", True)
browser = webdriver.Chrome(options=chrome_options)
browser.get('https://www.tolgas.ru/services/raspisanie/?id=0')

try:
    element = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[2]/form/div/div/button'))
    )
finally:
    kuki = browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/button')
    kuki.click()
rows = []
for i in range(271):
    select = Select(browser.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/form/div/label[1]/select'))
    select.select_by_index(i)
    #select.select_by_visible_text("БОЗИоз23")
    share = browser.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/form/div/div/input')
    share.click()

    time.sleep(5)
    source_data = browser.page_source
    soup = bs(source_data, 'html.parser')

    

    # Поиск всех блоков расписания
    schedule_blocks = soup.find_all('div', class_='timetable-frame__row')

    current_date = None

    for block in schedule_blocks:
        # Проверяем, есть ли в блоке дата
        date_div = block.find('div', class_='timetable-frame-current-date__text timetable-frame-current-date__text--2 text-lead')
        if date_div:
            current_date = date_div.get_text(strip=True)

        # Находим элементы расписания
        lessons = block.find_all('li', class_='timetable-frame__item timetable-frame-item')
        
        for lesson in lessons:
            subject = lesson.find('h3', class_='timetable-frame-item__title text-black').get_text(strip=True)
            
            times = lesson.find('div', class_='timetable-frame-item__time').find_all('span')
            time_range = f"{times[0].get_text(strip=True)} - {times[1].get_text(strip=True)}"
            
            audience = lesson.find('div', class_='timetable-frame-item__text--1').find('p').get_text(strip=True)
            
            teacher = lesson.find_all('div', class_='timetable-frame-item__text--1')[1].find('p').get_text(strip=True)
            
            lesson_type = lesson.find('div', class_='timetable-frame-item__type').get_text(strip=True)
            
            # Получаем информацию о группе (при необходимости обрабатывать исключения)
            try:
                group_info = lesson.find('div', class_='timetable-frame-item__text--2').find('p').get_text(strip=True)
                group = group_info.replace("Для групп: ", "")
            except AttributeError:
                group = ""

            rows.append({
                "Дата": current_date,
                "Время занятия": time_range,
                "Предмет": subject,
                "Аудитория": audience.replace("Аудитория: ", ""),
                "Преподаватель": teacher.replace("Преподаватель: ", ""),
                "Тип занятия": lesson_type.strip(),
                "Группа": group
            })
    browser.back()
    #time.sleep(5)
# Создать DataFrame
df = pd.DataFrame(rows)
df.to_excel('данные.xlsx', index=False)
#print(df)
