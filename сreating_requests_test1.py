from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import os
from selenium.common.exceptions import TimeoutException
import traceback  # Импортируем модуль traceback для обработки ошибок



class TestCreating():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}
        self.driver.maximize_window()


    def teardown_method(self, method):
        sleep(10)
        self.driver.quit()

    def test_CreatingAnApplication(self):
        try:
            # Авторизация
            self.driver.get("https://xxxxx.me/auth/login")
            self.driver.find_element(By.XPATH,"//input[@name=\"password\"]").send_keys("XXXXXXXXXXXX")
            self.driver.find_element(By.XPATH, "//input[@name=\"username\"]").send_keys("1231232")

           # Меню
            self.driver.find_element(By.XPATH,"//button[@class=\"buttonstyled__StyledButton-sc-1c5l3e8-0 fWrIer\"]").click()
            WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.LINK_TEXT, "Журнал заявок")))
            self.driver.find_element(By.LINK_TEXT, "Журнал заявок").click()
            self.driver.find_element(By.XPATH, "//button[contains(@class, 'main-buttonstyled__StyledButton')]//div[text()='Создать заявку']").click()

           # Заявитель
            self.driver.find_element(By.CSS_SELECTOR, ".phonestyled__StyledInput-sc-121dg7b-8").clear()
            self.driver.find_element(By.CSS_SELECTOR, ".phonestyled__StyledInput-sc-121dg7b-8").send_keys("(111) 111-11-11")
            WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable((By.XPATH, "//button[.//div[text()='Далее']]"))).click()

            try:
                # Если элемент с состоянием 'Все начисления по объекту' найден, пропускаем шаг
                WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH,"//div[contains(@class, 'statusstyled__BottomBlock')]//span[text()='Все начисления по объекту']")))
                # Если элемент не найден, выполняем шаг
                self.driver.find_element(By.XPATH, "//button[.//div[text()='Далее']]").click()
                self.driver.find_element(By.XPATH, "//div[contains(@class, 'descriptionstyled__SelectionGroupWrapper')]//div[text()='Ремонт строения/дома']").click()
            except TimeoutException:
               # Описание
                self.driver.find_element(By.XPATH,"//div[contains(@class, 'descriptionstyled__SelectionGroupWrapper')]//div[text()='Ремонт строения/дома']").click()

            self.driver.find_element(By.XPATH,"//div[contains(@class, 'descriptionstyled__SelectionGroupWrapper')]//div[text()='Общее имущество']").click()
            self.driver.find_element(By.XPATH, "//textarea[@class ='request-descriptionstyled__DescriptionTextArea-sc-4rka9i-2 dVhSyn common-v4-scrollbar']").send_keys("test_test")
            scrollable_element = self.driver.find_element(By.XPATH, "//div[@class = 'stepsstyled__ScrollWrapper-sc-1du8ujb-5 IUAlc common-v4-scrollbar']")
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scrollable_element)
            self.driver.find_element(By.XPATH,"//div[contains(@class, 'request-datestyled__Wrapper')]//button[text()='До обеда']").click()
            self.driver.find_element(By.XPATH, "//button[.//div[text()='Далее']]").click()

            # Дополнительно
            self.driver.find_element(By.XPATH,"//div[contains(@class,'additionallystyled__SelectionGroupWrapper')]//div[text()='Срочная']").click()
            self.driver.find_element(By.XPATH, "//div[contains(@class,'additionallystyled__SelectionGroupWrapper-sc-d7zh0-4')]//div[text()='004']").click()
            file_input = self.driver.find_element(By.XPATH,"//input[@type = 'file']")
            image_path = os.path.join("images.jpeg")
            absolute_image_path = os.path.abspath(image_path)
            file_input.send_keys(absolute_image_path)
            self.driver.find_element(By.XPATH, "//button[.//div[text()='Сохранить и создать новую']]").click()

            # Проверка создания заявки
            try:
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),\"Создана заявка\")]")))
                print("Заявка успешно создана.")
            except TimeoutException:
                print("Заявка не создана.")
                raise AssertionError("Тест провален: заявка не была создана.")  # Завершаем тест, если заявка не была создана

            time.sleep(1)

            # Сохраняем номер созданной заявки без символа "№"
            self.vars["x"] = self.driver.find_element(By.CSS_SELECTOR, ".toaststyled__ToastSubtitle-sc-1a980md-3").text
            self.vars["x"] = self.vars["x"].replace("№", "").strip()  # Убираем "№" и лишние пробелы
            print("Номер заявки:", self.vars["x"])

            # Сохраняем текущее окно
            current_window = self.driver.current_window_handle

            # Кликаем по элементу, который открывает новую вкладку
            self.driver.find_element(By.CSS_SELECTOR, ".toaststyled__ToastSubtitle-sc-1a980md-3").click()

            # Ждем, пока новая вкладка откроется
            WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)

            #Переключаемся на новую вкладку
            for window in self.driver.window_handles:
                if window != current_window:
                    self.driver.switch_to.window(window)
                    break


                # Ожидание, пока элемент станет видимым
            try:
                WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, f"//span[contains(.,'{self.vars['x']}')]")))
                print("Заявка найдена в журнале.")
            except TimeoutException:
                print("Заявка не найдена в журнале.")
                raise AssertionError("Тест провален: заявка не была найдена в журнале.")  

            #Проверка наличия прикрепленного файла
            try:
               WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@src,'static/media/attach_staple')]")))
               print("Файл к заявке прикреплен")
            except TimeoutException:
                print("Файл не прикреплен к заявке")
                raise AssertionError("Тест провален: файл не был прикреплен к заявке.")

        except Exception as e:
            # Выводим информацию об ошибке
            print("Произошла ошибка:")
            print(traceback.format_exc())
            raise e  
