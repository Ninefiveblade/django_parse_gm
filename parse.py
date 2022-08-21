import os
import json
from time import sleep

from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

storage = {}
storage1 = {}


def zoomout(driver) -> None:
    """Метод необходим для активации кнопки на карте
    'Искать здесь'."""

    zoom_out = driver.find_element(
        By.XPATH, '//*[@id="widget-zoom-out"]/div'
    )
    zoom_out.click()
    find_farmacy = driver.find_element(
        By.XPATH, '//*[@id="search-this-area"]/div/button/span'
    )
    sleep(1)
    find_farmacy.click()
    sleep(4)
    parse_farmacy(driver)


def parse_farmacy(driver) -> None:
    """Парсинг всех аптек на выбранной карте."""

    soup = BeautifulSoup(driver.page_source, "html.parser")
    div1 = soup.find("div", class_="XltNde tTVLSc")
    first_last = div1.find_all("div", class_="Nv2PK Q2HXcd THOPZb")
    middle = div1.find_all("div", class_="Nv2PK THOPZb tH5CWc")
    if first_last:
        for row in first_last:
            name = row["aria-label"]
            card_link = row.find("a")["href"]
            storage[name] = card_link
    if middle:
        for row in middle:
            name = row["aria-label"]
            card_link = row.find("a")["href"]
            storage[name] = card_link


def parse_card(storage: dict, driver) -> None:
    """Парсинг карточки каждой аптеки."""

    for name, link in storage.items():
        driver.get(link)
        sleep(1)
        try:
            farm_stars = driver.find_element(
                By.CSS_SELECTOR, (
                    '#QA0Szd > div > div > div.w6VYqd > '
                    'div.bJzME.tTVLSc > div > '
                    'div.e07Vkf.kA9KIf > div > div > '
                    'div.TIHn2 > div.tAiQdd > div.lMbq3e > '
                    'div.LBgpqf > div > div.fontBodyMedium.dmRWX > '
                    'div.F7nice.mmu3tf > span > span > span.ceNzKf'
                )
            ).get_attribute("aria-label")
        except NoSuchElementException:
            farm_stars = "Нет звезд"
        try:
            overall_reviews = driver.find_element(
                By.CSS_SELECTOR, (
                    '#QA0Szd > div > div > div.w6VYqd > '
                    'div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > '
                    'div > div > div.TIHn2 > div.tAiQdd > '
                    'div.lMbq3e > div.LBgpqf > div > '
                    'div.fontBodyMedium.dmRWX > span:nth-child(3) > '
                    'span > span > span.F7nice.mmu3tf > '
                    'span:nth-child(1) > button'
                )
            ).text
        except NoSuchElementException:
            overall_reviews = "Нет отзывов"
        try:
            source = driver.find_element(
                By.CSS_SELECTOR, (
                    '#QA0Szd > div > div > div.w6VYqd > '
                    'div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > '
                    'div > div > div:nth-child(9) > div:nth-child(5) > '
                    'a > div.AeaXub > div.rogA2c.ITvuef > '
                    'div.Io6YTe.fontBodyMedium'
                )
            ).text
        except NoSuchElementException:
            source = "Нет ресурса"
        storage1[name] = [link, farm_stars, overall_reviews, source]


def parse_reviews(storage1: dict, driver, farm_data) -> None:
    """Парсинг отзывов каждой аптеки."""

    for name, array in storage1.items():
        link = array[0]
        driver.get(link)
        if array[2] == "Нет отзывов":
            pass
        else:
            try:
                more_reviews = driver.find_element(
                    By.CSS_SELECTOR, (
                        '#QA0Szd > div > div > div.w6VYqd > '
                        'div.bJzME.tTVLSc > div > '
                        'div.e07Vkf.kA9KIf > div > div > '
                        'div.TIHn2 > div.tAiQdd > div.lMbq3e > '
                        'div.LBgpqf > div > div.fontBodyMedium.dmRWX > '
                        'span:nth-child(3) > span > span > '
                        'span.F7nice.mmu3tf > span:nth-child(1) > button'
                    )
                )
                more_reviews.click()
                sleep(1)
                element = driver.find_element(
                        By.CSS_SELECTOR,
                        (
                            '#QA0Szd > '
                            'div > div > '
                            'div.w6VYqd > '
                            'div.bJzME.tTVLSc > div'
                        )
                    )
                scroll_origin = ScrollOrigin.from_element(element)
                number_reviews = array[2].replace(
                    ' отзывов', ''
                ).replace(' отзыва', '').replace(' отзыв', '')
                last_review = int(number_reviews)*9
                for i in range(last_review):
                    ActionChains(driver)\
                        .scroll_from_origin(scroll_origin, 0, 200)\
                        .perform()
                sleep(1)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                div1 = soup.find("div", class_="m6QErb DxyBCb kA9KIf dS8AEf")
                div2 = div1.find_all("div", class_="jftiEf fontBodyMedium")
                for row in tqdm(div2):
                    author = row.find('div', class_="d4r55").text
                    date = row.find('div', class_="DU9Pgb").find(
                         "span", class_="rsqaWe"
                    ).text
                    stars = row.find('div', class_="DU9Pgb").find(
                         "span", class_="kvMYJc"
                    )["aria-label"]
                    comment = row.find('div', class_="MyEned").text
                    farm_data["farmacy"].append([
                        {"name": name.strip()},
                        {"link": link},
                        {"farm_stars": array[1].strip()},
                        {"overall_reviews": array[2].strip()},
                        {"source": array[3]},
                        {"author": author.strip()},
                        {"date": date.strip()},
                        {"stars": stars.strip()},
                        {"comment": comment.strip()}
                    ])
            except Exception as er:
                print(er)


def find_coordinates(data, driver, zoom: str) -> None:
    """Поиск элементов карты по координатам."""

    for coordinates in data['coordinates']:
        lat = coordinates['lat']
        lon = coordinates['lon']
        url = f"https://www.google.com/maps/search/аптека/@{lat},{lon},{zoom}"
        driver.get(url)
        try:
            zoomout(driver)
        except Exception:
            continue


def main() -> None:
    """path - определяем путь до драйвера.
    chrome_options - открываем опции драйвера,
    включаем javascript.
    path_coor_data - получаем заготовленные
    координаты,
    path_farm_data - подготавливаем к записи
    файл json.
    driver - запускаем браузер,
    logging решил не исользовать.
    find_coordinates - Поиск по частям карты,
    zoomout - поиск аптек на элементах карты,
    parse_farmacy - парсинг аптек,
    parse_card - парсинг карточек каждой аптеки,
    parse_reviews - парсинг отзывов каждой аптеки.
    storage  - хранилище аптек и карточек
    storage1 - хранилище дополнительных данных
    для передачи в parse_reviews.
    """

    path = os.path.abspath("backend/data/chromedriver")
    path_farm_data = os.path.abspath("backend/data/famacy.json")
    path_coor_data = os.path.abspath("backend/data/coordinates.json")
    with open(path_farm_data, encoding='utf-8') as f:
        farm_data = json.load(f)
    with open(path_coor_data, encoding='utf-8') as f:
        data = json.load(f)
    zoom = "14.9z"
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--enable-javascript")
    driver = webdriver.Chrome(path, chrome_options=chrome_options)
    driver.implicitly_wait(10)
    find_coordinates(data, driver, zoom)
    if storage:
        parse_card(storage, driver)
    if storage1:
        parse_reviews(storage1, driver, farm_data)
    with open(path_farm_data, 'w', encoding='utf-8') as outfile:
        json.dump(farm_data, outfile, ensure_ascii=False, indent=2)
    driver.close()
    print("All Done!")


if __name__ == '__main__':
    main()
