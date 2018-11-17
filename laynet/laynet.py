from selenium import webdriver
import time
import logger
import utility
from selenium.webdriver.support import expected_conditions as EC
import db
import stock

lg = logger.Logger()

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
#options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")

driver = webdriver.Chrome('chromedriver.exe', options=options, service_log_path='result.log')

stock.scrape_kospi_top200(driver)
stock.scrape_kospi_top200_stock_trade(driver)
stock.update_kospi_top200_big_players_data()
stock.update_today_recommendation_stock()
stock.update_past_recommendation_results()
    
driver.quit()