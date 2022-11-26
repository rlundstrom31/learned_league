import os
import time

import pandas
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    # debugging help
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=service)
    user = os.environ['user']  # must set these using environmental variables
    pwd = os.environ['pwd']
    driver.get('https://www.learnedleague.com/ucp.php?mode=login')
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/form/div[2]/div/div[2]/input').send_keys(user)
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/form/div[3]/div/div[2]/input').send_keys(pwd)
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/form/div[5]/input').click()
    # logging in complete - can start scraping games
    driver.get('https://www.learnedleague.com')
    driver.maximize_window()
    opponentName = "LundstromR"
    driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/section/form').click()
    driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/section/form/input').send_keys(opponentName)
    time.sleep(3)
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div/section/form/div/a[1]')))
    element.click()
    # We have gotten to a profile
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div[2]/button[9]').click() #to the question history page!
    time.sleep(1)
    df = pd.DataFrame()
    for i in range(1,19):
        basePath = '/html/body/div[2]/div[1]/div/div[11]/div/ul[' + str(i) + ']/li'
        wait.until(EC.element_to_be_clickable((By.XPATH, (basePath + '/span[1]')))).click()
        topic = driver.find_element(By.XPATH, basePath + '/span[2]').text
        rows = driver.find_elements(By.XPATH, basePath + '/ul/table/tbody/tr')
        for j in range(1, len(rows)+1):
            questionPage = wait.until(EC.element_to_be_clickable((By.XPATH, (basePath + '/ul/table/tbody/tr[' + str(j) + ']/td[1]/a[3]'))))
            correctIdentifier = wait.until(EC.element_to_be_clickable((By.XPATH, (basePath + '/ul/table/tbody/tr[' + str(j) + ']/td[3]')))).get_attribute("class")
            correct = (correctIdentifier == "c g")
            questionPage.click()
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[1])
            correctPct = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div[1]/div/div[3]/div[1]/div[1]/span').text[0:-1]
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            df2 = pd.DataFrame({'Subject': [topic], 'Correct': [correct], "percentCorrect": [correctPct]})
            df = pd.concat([df, df2])
    df = df.reset_index()
    print(df)