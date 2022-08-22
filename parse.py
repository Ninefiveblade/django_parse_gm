import os
import sys
import json
import logging
from time import sleep

from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup


logging.basicConfig(
    level=logging.INFO,
    filename='program.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s'
)
handler.setFormatter(formatter)

storage = {}
storage1 = {}


def zoomout(driver) -> None:
    """Метод необходим для активации кнопки на карте
    'Искать здесь'."""

    zoom_out = driver.find_element(
        By.XPATH, '//*[@id="widget-zoom-out"]'
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
    element = driver.find_element(
        By.CSS_SELECTOR,
        (
            '#QA0Szd > div > div > div.w6VYqd > '
            'div.bJzME.tTVLSc > div > '
            'div.e07Vkf.kA9KIf > div > div > '
            'div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd'
        )
    )
    scroll_origin = ScrollOrigin.from_element(element)
    while True:
        ActionChains(driver)\
            .scroll_from_origin(scroll_origin, 0, 600)\
            .perform()
        soup = BeautifulSoup(driver.page_source, "html.parser")
        if soup.find("div", class_="PbZDve") is not None:
            logger.info('Тег PbZDve найден, цикл остановлен')
            break
        if soup.find("div", class_="njRcn") is not None:
            logger.info('Тег njRcn найден, цикл остановлен')
            break

    soup = BeautifulSoup(driver.page_source, "html.parser")
    div1 = soup.find("div", class_="XltNde tTVLSc")
    first_last = div1.find_all("div", class_="Nv2PK Q2HXcd THOPZb")
    middle = div1.find_all("div", class_="Nv2PK THOPZb tH5CWc")
    count = 0
    if first_last:
        for row in first_last:
            name = row["aria-label"]
            card_link = row.find("a")["href"]
            if name in storage.keys():
                count += 1
                name += f" Номер {count}"
            storage[name] = card_link
        logger.info("Успешно выполнено first_last")
    if middle:
        for row in middle:
            name = row["aria-label"]
            card_link = row.find("a")["href"]
            if name in storage.keys():
                count += 1
                name += f" Номер {count}"
            logger.info("Успешно выполнено middle")
            storage[name] = card_link


def parse_card(storage: dict, driver) -> None:
    """Парсинг карточки каждой аптеки."""

    for name, link in storage.items():
        driver.get(link)
        sleep(0.5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        if soup.find("div", "fontBodyMedium dmRWX") is not None:
            farm_stars = soup.find(
                "div", "fontBodyMedium dmRWX"
            ).find("div", class_="F7nice mmu3tf")
            if farm_stars is not None:
                farm_stars = farm_stars.find("span", class_="ceNzKf")
                if farm_stars is not None:
                    farm_stars = farm_stars["aria-label"]
        else:
            farm_stars = "-"
        if soup.find("span", class_="mgr77e") is not None:
            overall_reviews = soup.find("span", class_="mgr77e").find(
                "button", class_="DkEaL"
            )
            if overall_reviews is not None:
                overall_reviews = overall_reviews.text
            else:
                overall_reviews = "-"
        else:
            overall_reviews = "-"
        if soup.find("div", "rogA2c ITvuef") is not None:
            source = soup.find(
                "div", "rogA2c ITvuef"
            ).find("div", class_="Io6YTe fontBodyMedium").text
        else:
            source = "-"
        logger.info(
            f"Данные успешно парсятся\n"
            f"{[link, farm_stars, overall_reviews, source]}"
        )
        storage1[name] = [link, farm_stars, overall_reviews, source]


def parse_reviews(storage1: dict, driver, farm_data) -> None:
    """Парсинг отзывов каждой аптеки."""

    for name, array in storage1.items():
        link = array[0]
        driver.get(link)
        if array[2] == "-":
            continue
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
                logger.error(f'Произошла ошибка {er}')
                continue


def find_coordinates(data, driver, zoom: str) -> None:
    """Поиск элементов карты по координатам."""

    for coordinates in data['coordinates']:
        lat = coordinates['lat']
        lon = coordinates['lon']
        url = (
            f"https://www.google.com/maps/search/"
            f"farmàcia/@{lat},{lon},{zoom}"
        )
        driver.get(url)
        try:
            zoomout(driver)
        except Exception as er:
            logger.error(f'Произошла ошибка {er}')
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
    find_coordinates - Поиск по частям карты,
    zoomout - поиск аптек на элементах карты,
    parse_farmacy - парсинг аптек,
    parse_card - парсинг карточек каждой аптеки,
    parse_reviews - парсинг отзывов каждой аптеки.
    storage  - хранилище аптек и карточек
    storage1 - хранилище дополнительных данных
    для передачи в parse_reviews.
    """

    TIME_OUT = 180
    RETRY_TIME = 600
    RETRY_COUNT = 2
    path = os.path.abspath("backend/data/chromedriver")
    path_farm_data = os.path.abspath("backend/data/famacy.json")
    path_coor_data = os.path.abspath("backend/data/coordinates.json")
    with open(path_farm_data, encoding='utf-8') as f:
        farm_data = json.load(f)
    with open(path_coor_data, encoding='utf-8') as f:
        data = json.load(f)
    zoom = "15z"
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--enable-javascript")
    driver = webdriver.Chrome(path, chrome_options=chrome_options)
    driver.implicitly_wait(TIME_OUT)
    find_coordinates(data, driver, zoom)
    if storage:
        parse_card(storage, driver)
    for _ in range(RETRY_COUNT):
        try:
            if storage1:
                parse_reviews(storage1, driver, farm_data)
            break
        except Exception as er:
            logger.error(
                f"Произошла ошибка {er}"
            )
            logger.info(f"Сон на {RETRY_TIME} секунд")
            sleep(RETRY_TIME)
    with open(path_farm_data, 'w', encoding='utf-8') as outfile:
        json.dump(farm_data, outfile, ensure_ascii=False, indent=2)
    driver.close()
    logger.info("Программа успешно выолнена")
    print("All Done!")


if __name__ == '__main__':
    main()
