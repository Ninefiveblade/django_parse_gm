"""Парсинг комментариев ватиканской Аптеки."""
import os
import time
import json

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

def parse(driver, url):
    """Парсинг.
    ActionChains - мотаем до конца страницы, пока не
    найдем последний элемент.
    Цикл прерываем, если последний динамический элемент найден.
    Парсим все необходимые данные и записываем в json.
    time.sleep - 10 секунд для подгрузки времени,
    Это нужно для подгрузки всех комментариев на страницу.
    inplicity_wait не удовлетворяет результат в данной задаче.
    div1 - Тег в котором будем искать комментарии (rows).
    div2 - Тег с перечнем комментариев."""

    time.sleep(10)
    iframe = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]')
    scroll_origin = ScrollOrigin.from_element(iframe)
    while True:
        ActionChains(driver)\
            .scroll_from_origin(scroll_origin, 0, 200)\
            .perform()
        try:
            driver.find_element(By.CSS_SELECTOR, (
                "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > "
                "div > div.e07Vkf.kA9KIf > div > div > "
                "div.m6QErb.DxyBCb.kA9KIf.dS8AEf > "
                "div:nth-child(10) > div:nth-child(1357)"
            ))
            break
        except Exception:
            continue

    soup = BeautifulSoup(driver.page_source, "html.parser")
    div1 = soup.find("div", class_="m6QErb DxyBCb kA9KIf dS8AEf")
    div2 = div1.find_all("div", class_="jftiEf fontBodyMedium")
    with open("dump.json", encoding='utf-8') as f:
        data = json.load(f)  # Загружаем файл json.

    reviews_overall = 0  # Считаем количество комментариев.
    for row in div2:
        name = row.find('div', class_="d4r55").text
        date = row.find('div', class_="DU9Pgb").find("span", class_="rsqaWe").text
        stars = row.find('div', class_="DU9Pgb").find("span", class_="kvMYJc")["aria-label"]
        comment = row.find('div', class_="MyEned").text
        new_data = {
            "name": name.strip(),
            "date": date.strip(),
            "stars": stars.strip(),
            "comment": comment.strip()
        }
        data["reviews"].append(new_data)
        reviews_overall +=1
    data["pharmacy"].append(soup.find("title").text)
    data["reviews_overall"].append(reviews_overall)
    data["pharmacy_url"].append(url)
    with open("dump.json", 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2)
    driver.close()

def main():
    """path - определяем путь до драйвера.
    chrome_options - открываем опции драйвера,
    включаем javascript.
    driver - запускаем браузер,
    получаем url и передаем в функцию parse.
    """
    path = os.path.abspath("chromedriver")
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--enable-javascript")
    driver = webdriver.Chrome(path, chrome_options=chrome_options)
    with open("urls.txt", "r") as f:
        url = f.readline()
    driver.get(url)
    parse(driver, url)

if __name__ == "__main__":
    main()

