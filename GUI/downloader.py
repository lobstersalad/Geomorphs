# Sources: https://selenium-python.readthedocs.io/
#          https://stackoverflow.com/questions/45631715/downloading-with-chrome-headless-and-selenium

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

def download(download_path, dungeon_name, random_seed, dungeon_layout, dungeon_size, peripheral_egress, add_stairs, room_layout, room_size, door_set,
             corridor_layout, remove_deadends):
    def text_select(option, value):
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, option)), message = 'Unable to Locate Text Box')
        element.clear()
        element.send_keys(value)

    def dd_select(option, value):
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, option)), message = 'Unable to Locate Dropdown')
        select = Select(element)
        select.select_by_visible_text(value)

    def button_press(option, wait):
        element = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.XPATH, option)), message = 'Unable to Locate Button')
        element.click()

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options = options)
    driver.command_executor._commands['send_command'] = ('POST', '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_path}}
    driver.execute('send_command', params)
    print ('Connecting to donjon...')
    driver.get('https://donjon.bin.sh/d20/dungeon/')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'dungeon_form')), message = 'Connection Failed')

    # Don't really care about level, motif
    # Need defaults for style, grid
    print ('Selecting Map Options...')
    text_select('name', dungeon_name)
    dd_select('level', '1')
    dd_select('motif', 'None')
    text_select('seed', random_seed)
    dd_select('map_style', 'Standard')
    dd_select('grid', 'Square')
    dd_select('dungeon_layout', dungeon_layout)
    dd_select('dungeon_size', dungeon_size)
    dd_select('peripheral_egress', peripheral_egress)
    dd_select('add_stairs', add_stairs)
    dd_select('room_layout', room_layout)
    dd_select('room_size', room_size)
    dd_select('door_set', door_set)
    dd_select('corridor_layout', corridor_layout)
    dd_select('remove_deadends', remove_deadends)

    button_press("//input[@value = 'Construct']", 10)
    print ('Constructing Map...')

    button_press("//input[@value = 'Print Map']", 600)
    print ('Downloading Map!')

if __name__ == '__download__':
    download()
