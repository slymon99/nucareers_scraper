from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import secrets
import sqlite3


driver = webdriver.Edge()
driver.get("https://nucareers.northeastern.edu/Shibboleth.sso/Login?target=https://nucareers.northeastern.edu/secure/neuLogin.htm?action=login#login")
time.sleep(1)
driver.find_element_by_id("username").send_keys("clark.si")
driver.find_element_by_id("password").send_keys(secrets.password)
driver.find_element_by_name("submit").click()
time.sleep(3)

driver.get("https://nucareers.northeastern.edu/myAccount/co-op/jobs.htm")
Select(driver.find_element_by_id("savedSearchId")).select_by_visible_text("cs")
time.sleep(5)
# driver.find_element_by_xpath("//*[contains(text(), 'For My Program')]").click()

conn = sqlite3.connect('application.db')
c = conn.cursor()
c.execute('DELETE FROM Jobs')

time.sleep(2)

for i in range(1, 6):
    if i != 1:
        time.sleep(3)
        driver.execute_script("loadPostingTable('', '',  'Forward', '{}','myProgramPostingsCount','', null)".format(i))
        print("moved forward")
        time.sleep(7)
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(7)
    for row in driver.find_elements_by_tag_name("tr")[1:]:

        main_window = driver.current_window_handle
        col = row.find_element_by_class_name('orgDivTitleMaxWidth')
        span = col.find_elements_by_tag_name('span')[-1]
        span.click()
        driver.switch_to_window(driver.window_handles[-1])
        time.sleep(2)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, ("panel-body"))))

        titles = driver.find_elements_by_tag_name('h5')
        if titles:
            title = titles[0].text.strip()
            body = driver.find_element_by_class_name('panel-body')
            
            salary = -1
            max_salary = -1
            for subrow in body.find_elements_by_tag_name('tr'):
                groups = subrow.find_elements_by_tag_name('td')
                if groups:
                    label = groups[0].text
                    if ('Minimum' in label):
                        salary = groups[1].text
                    elif ('Maximum' in label):
                        max_salary = groups[1].text
                        
            

            c.execute('INSERT INTO Jobs VALUES (?, ?, ?)', (title, salary, max_salary,))
            conn.commit()
        driver.close()
        driver.switch_to_window(driver.window_handles[0])


    