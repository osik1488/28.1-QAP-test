from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest
from time import sleep
from pages.base_page import BaseForm
from pages.base_page import AuthForm
from pages.base_page import CodeForm
from pages.settings import *
@pytest.fixture(autouse=True)
def testing(selenium):
   selenium.get("https://b2c.passport.rt.ru")
   # Переходим на страницу авторизации
   yield

   selenium.quit()
   # лицевой счет
def test_postive_tabs (selenium):
    sleep(5)
    form = AuthForm(selenium)
    form.ls_tab.click()
    activ_ls_tab = selenium.find_element(By.CSS_SELECTOR,"div#t-btn-tab-ls")
    assert activ_ls_tab


def test_postive_login_tab(selenium):
    sleep(5)
    form = AuthForm(selenium)
    form.login_tab.click()
    activ_login_tab = selenium.find_element(By.CSS_SELECTOR,"div#t-btn-tab-login")
    assert activ_login_tab

# почта
def test_postive_mail_tab(selenium):
    sleep(5)
    form = AuthForm(selenium)
    form.mail_tab.click()
    activ_mail_tab = selenium.find_element(By.ID,"t-btn-tab-mail")
    assert activ_mail_tab


# телефон
def test_postive_phone_tab(selenium):
    sleep(5)
    form = AuthForm(selenium)
    form.phone_tab.click()
    activ_phone_tab = selenium.find_element(By.ID,"t-btn-tab-phone")
    assert activ_phone_tab



#  проверка, что по-умолчанию выбрана форма авторизации по телефону
def test_005_by_phone(selenium):

    form = AuthForm(selenium)
    sleep(5)
    assert form.placeholder.text == 'Мобильный телефон'


#проверка автосмены "ввода"
def test_006_change_placeholder(selenium):
    form = AuthForm(selenium)
    sleep(5)
    # ввод телефона
    form.username.send_keys('+79998887766')
    form.password.send_keys('_')


    assert form.placeholder.text == 'Мобильный телефон'

def test_change_placeholder_login(selenium):
    form = AuthForm(selenium)
    # очистка поля логина
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)

    # ввод почты
    form.username.send_keys('mail@mail.ru')
    form.password.send_keys('_')
    sleep(5)

    assert form.placeholder.text == 'Электронная почта'

    # очистка поля логина
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)

    # ввод логина
    form.username.send_keys(valid_email)
    form.password.send_keys('_'),
    sleep(5)

    assert form.placeholder.text == 'Электронная почта'


#проверка позитивного сценария авторизации по телефону
def test_007_positive_by_phone(selenium):
    sleep(5)
    form = AuthForm(selenium)

    # ввод телефона
    form.username.send_keys(valid_phone)
    form.password.send_keys(valid_pass)
    sleep(5)
    form.btn_click()

    assert form.find_element(By.XPATH,'//*[@id="app"]/main[1]/div[1]/div[2]/div[3]/h3[1]')

# проверка негативного сценария авторизации по телефону
def test_007_negative_by_phone(selenium):
    form = AuthForm(selenium)

    # ввод телефона
    form.username.send_keys('+1234567890')
    form.password.send_keys('any_password')
    sleep(5)
    form.btn_click()

    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


#проверка негативного сценария авторизации по почте
def test_010_negative_by_email(selenium):
    form = AuthForm(selenium)

    # ввод почты
    form.username.send_keys('aa@aa.aa')
    form.password.send_keys('any_password')
    sleep(5)
    form.btn_click()

    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'

# проверка позитивного сценария авторизации по почте
def test_009_positive_by_email(selenium):
    form = AuthForm(selenium)

    # ввод почты
    form.username.send_keys(valid_email)
    form.password.send_keys(valid_pass)
    sleep(5)
    form.btn_click()

    assert form.find_element(By.XPATH,'//*[@id="app"]/main[1]/div[1]/div[2]/div[3]/h3[1]')

#проверка получения временного кода на телефон и открытия формы для ввода кода
def test_get_code(selenium):
    sleep(5)
    form = CodeForm(selenium)

    # ввод телефона
    form.address.send_keys(valid_phone)

    form.code_btn_click()

    rt_code = form.find_element(By.XPATH,'//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/div[1]/div[1]/div[1]')
    assert rt_code


#проверка перехода в форму восстановления пароля и её открытия
def test_forgot_pass(selenium):
    form = AuthForm(selenium)

    # клик по надписи "Забыл пароль"
    form.forgot.click()
    sleep(5)

    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Восстановление пароля'


# проверка перехода в форму регистрации и её открытия
def test_register(selenium):
    form = AuthForm(selenium)

    # клик по надписи "Зарегистрироваться"
    form.register.click()
    sleep(5)

    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Регистрация'


#проверка открытия пользовательского соглашения
def test_agreement(selenium):
    form = AuthForm(selenium)

    original_window = form.driver.current_window_handle
    # клик по надписи "Пользовательским соглашением" в подвале страницы
    form.agree.click()
    sleep(5)
    WebDriverWait(form.driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in form.driver.window_handles:
        if window_handle != original_window:
            form.driver.switch_to.window(window_handle)
            break
    win_title = form.driver.execute_script("return window.document.title")

    assert win_title == 'User agreement'

#проверка перехода по ссылке авторизации пользователя через вконтакте
def test_uth_vk(selenium):
    form = AuthForm(selenium)
    sleep(5)
    form.vk_btn.click()
    sleep(5)

    assert form.get_base_url(
        'https://oauth.vk.com/authorize?scope=login:email&state=NzZVyYZRa8fB39qt0A9VTWpF8o8iWI-35obrF03k4Qk.-txhZTWGBVM.lk_smarthome&response_type=code&client_id=6771961&redirect_uri=https://b2c.passport.rt.ru/social/adapter/vk/auth&nonce=m3VUK9iTLzidn597pZY1zg') == 'oauth.vk.com'


#проверка перехода по ссылке авторизации пользователя через одноклассники
def test_auth_ok(selenium):
    form = AuthForm(selenium)
    form.ok_btn.click()
    sleep(5)

    assert form.get_base_url(
        'https://connect.ok.ru/dk?st.cmd=OAuth2Login&st.redirect=%252Fdk%253Fst.cmd%253DOAuth2Permissions%2526amp%253Bst.scope%253Dlogin%25253Aemail%2526amp%253Bst.response_type%253Dcode%2526amp%253Bst.show_permissions%253Doff%2526amp%253Bst.redirect_uri%253Dhttps%25253A%25252F%25252Fb2c.passport.rt.ru%25252Fsocial%25252Fadapter%25252Fok%25252Fauth%2526amp%253Bst.state%253DVtqCLUK2tH2skET6EU7UZCY_gKrx1Vcl-67oyOgXJoA.xXT7N4_4KSQ.lk_smarthome%2526amp%253Bst.client_id%253D1272957184&st.client_id=1272957184') == 'connect.ok.ru'


# проверка перехода по ссылке авторизации пользователя через майлру
def test_uth_mailru(selenium):
    form = AuthForm(selenium)
    form.mailru_btn.click()
    sleep(5)

    assert form.get_base_url(
        'https://connect.mail.ru/oauth/authorize?scope=login%3Aemail&state=ndKs0z8PIrS6n0INcTa1c6e8Bc1Gn555tP3kbwKs_bw.ODA-cijRHis.lk_smarthome&response_type=code&client_id=762573&redirect_uri=https://b2c.passport.rt.ru/social/adapter/mail/auth&nonce=NJFswKfOGqdlwi1sPlEMyg') == 'connect.mail.ru'


# проверка перехода по ссылке авторизации пользователя через google
def test_auth_google(selenium):
    form = AuthForm(selenium)
    form.google_btn.click()
    sleep(5)

    assert form.get_base_url(
        'https://accounts.google.com/o/oauth2/auth/identifier?scope=openid&state=6U6PficG8ZDRlxCg7J3cjk7QMCgeBHEik3SfmpVPUVU.MF1cKQkTJSs.lk_smarthome&response_type=code&client_id=121868035218-rd8lrg4eb24p25g6vo6qnoerkln4b2lp.apps.googleusercontent.com&redirect_uri=https%3A%2F%2Fb2c.passport.rt.ru%2Fsocial%2Fadapter%2Fgoogle%2Fauth&nonce=KbXxryrTfaZ9DOTOx3SHxA&service=lso&o2v=1&flowName=GeneralOAuthFlow') == 'accounts.google.com'


#проверка перехода по ссылке авторизации пользователя через яндекс
def test_auth_yandex(selenium):
    form = AuthForm(selenium)
    sleep(5)
    form.ya_btn.click()
    sleep(5)

    assert form.get_base_url(
        'https://passport.yandex.ru/auth?retpath=https%3A%2F%2Foauth.yandex.ru%2Fauthorize%3Fscope%3Dlogin%253Aemail%26state%3Dl2rCdYq3uz3Sl5gCrFtQqYD8y7H5Q5Srgq98Y0T3hPw.ZY0GS1WxcSY.lk_smarthome%26response_type%3Dcode%26client_id%3Dcca955e781554be08e4007813ddd578e%26redirect_uri%3Dhttps%3A%2F%2Fb2c.passport.rt.ru%2Fsocial%2Fadapter%2Fya%2Fauth%26nonce%3DuHdvWm6v8ALPI4jCVj4x1Q&noreturn=1&origin=oauth') == 'passport.yandex.ru'
