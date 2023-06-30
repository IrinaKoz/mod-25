import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from settings import email, password


@pytest.fixture(autouse=True)
def browser_opening():
    driver = Service("Selenium_edukation/chromedriver/")
    pytest.driver = webdriver.Chrome(service=driver)
    # Переходим на страницу авторизации
    pytest.driver.get('https://petfriends.skillfactory.ru/login')
    pytest.driver.implicitly_wait(10)
    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))).send_keys(email)

    # Вводим пароль
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'pass'))).send_keys(password)

    # Нажимаем на кнопку входа в аккаунт
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))).click()

    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Нажимаем на кнопку Мои питомцы
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'nav-link'))).click()

    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h2').text == "NataliaB"

    images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0
