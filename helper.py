from dotenv import load_dotenv
import os
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import Firefox
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from seleniumwire import webdriver

load_dotenv(dotenv_path=".env", override=True)
def check_env_variables():
    username, password = os.getenv('USERNAME'), os.getenv('PASSWORD')
    if username == 'your_instagram_username_here' or password == 'your_instagram_password_here':
        return False
    else:
        print('env set correctly')
        return True
        
        
def setup_driver(browser):        
    if browser == 'chrome':
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--log-level=3")  
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument('--lang=en-US')
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, chrome_options=chrome_options)
    elif browser == 'firefox':
        firefox_options = FirefoxOptions()
        firefox_options.set_preference('intl.accept_languages', 'en-US, en')
        service = FirefoxService(GeckoDriverManager().install())
        driver = Firefox(service=service, options=firefox_options)
    
    return driver
