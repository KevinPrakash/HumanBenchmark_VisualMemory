from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re

value = []
done = True

# Wait for the html element to load
def waitforload(XPATH):
    timeout = 10
    try:
        element_present = EC.presence_of_element_located((By.XPATH, XPATH))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("restart the program")

# Find substrings in a string
def find_all(string, sub_string):
    start = 0
    while True:
        start = string.find(sub_string, start)
        if start == -1: return
        yield start
        start += len(sub_string)
        
# Open chrome and start the challenge

driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.get("https://www.humanbenchmark.com/tests/memory")
waitforload("//button[@class='hero-button']")
driver.find_element_by_xpath("//button[@class='hero-button']").click()

# Do this for every level
while(1):
    
    if done:
        # Detect the coloured squares
        waitforload("//div[@class='square active']")
        # Copy the entire html under the table on detecting the squares
        text = driver.find_element_by_xpath("//div[@class='squares']").get_attribute('innerHTML')
        # Remove extra text to improve speed for higher levels
        text = re.sub(r"[0-9:;,.<>dbdfghjklmnopwxyz// ]", "", text)
        # Create a list of the squares to click
        active_square = list(find_all(text,"squareactive"))
        value =  sorted(list(find_all(text,"\"square\"")) + active_square)
        done = False
        
    else:
        # Wait for the test to start
        test_squares = driver.find_elements_by_xpath("//div[@class='square']")
        if len(test_squares) == len(value):
            time.sleep(1)
            for i in range(len(value)):
                # Click with delay so the browser doesnt hang
                if value[i] in active_square:
                    time.sleep(0.1)
                    test_squares[i].click()
            done = True
        # This delay is required to prevent the clicked squares from being recognised as
        # the next level squares
        time.sleep(1)

                
        
        
