'''
ToDo
- Rename downloaded file
'''

import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(chrome_options = options)
driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': '/home/lobstersalad/Documents/490/Geomorphs/Texture Laying'}}
driver.execute("send_command", params)
driver.get("https://donjon.bin.sh/d20/dungeon/")

def text_select(option, value):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, option)))
    element.clear()
    element.send_keys(value)

def dd_select(option, value):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, option)))
    select = Select(element)
    select.select_by_visible_text(value)

def button_press(option, wait):
    element = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.XPATH, option)))
    element.click()

text_select("name", "Testing")
dd_select("level", "2")
dd_select("motif", "None")
text_select("seed", "2000")
dd_select("map_style", "Standard")
dd_select("grid", "Square")
dd_select("dungeon_layout", "Cavernous")
dd_select("dungeon_size", "Small")
dd_select("peripheral_egress", "No")
dd_select("add_stairs", "No")
dd_select("room_layout", "Dense")
dd_select("room_size", "Medium")
dd_select("door_set", "Standard")
dd_select("corridor_layout", "Errant")
dd_select("remove_deadends", "Some")

button_press("//input[@value = 'Construct']", 10)
button_press("//input[@value = 'Print Map']", 600)
