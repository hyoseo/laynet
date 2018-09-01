from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

def get_my_headers(driver) -> list:
    WHAT_IS_MY_BROWSER_URL = 'https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending'
    
    driver.get(WHAT_IS_MY_BROWSER_URL)

    trs = driver.find_elements_by_xpath('//*[@id="main"]/section/article/div/table/tbody/tr')
    headers = []
    for tr in trs:
        headers.append(tr.text)

    return headers