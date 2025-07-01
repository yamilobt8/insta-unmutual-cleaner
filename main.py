from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from collections import Counter
import os
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv

def get_followers_followings_count():
    spans = driver.find_elements(By.TAG_NAME, "span")
    followings_count = 0
    followers_count = 0
    
    for i in range(len(spans) - 1):
        if 'following' in spans[i].text:
            followings_count = spans[i+1].text.strip()
            followers_count = spans[i-1].text.strip()
            break
                
    if 'K' in followers_count:
        followers_count = int(followers_count.replace('K', '')) * 1000
        
    elif 'K' in followings_count:
        followings_count = int(followings_count.replace('K', '')) * 1000
        
    elif 'M' in followers_count:
        followers_count = float(followers_count.replace('M', '')) * 1000000
        
    elif 'M' in followings_count:
        followings_count = float(followings_count.replace('M', '')) * 1000000
        
            
    return [int(followings_count), int(followers_count)]


def scroll(followers_followings_count):
    ans = followers_followings_count // 12
    times_to_scorll =  ans + 3 if followers_followings_count > 60 else ans + 1
    scrollable_div = driver.execute_script("""return document.querySelector('[style="height: auto; overflow: hidden auto;"]').parentElement;""")
        
    for i in range(times_to_scorll):
        print(f'{i}/{times_to_scorll}')
        driver.execute_script("""arguments[0].scrollTop = arguments[0].scrollHeight;""", scrollable_div)
        sleep(1.5)
    driver.execute_script("""arguments[0].scrollTo({top: 0,behavior: 'smooth'})""", scrollable_div)

def get(followers_followings_count):

    scroll(followers_followings_count)

    followings_div = driver.execute_script("""return document.querySelector('[style="display: flex; flex-direction: column; padding-bottom: 0px; padding-top: 0px; position: relative;"]');""")
    followings_users = followings_div.find_elements(By.XPATH, './*')
    
    followings_links = []
    for user in followings_users:
        user_href = user.find_element(By.TAG_NAME, 'a').get_attribute('href')
        followings_links.append(user_href)        
            
    return followings_links

def unfollow_unmutuals(followers_followgins_count, unmutuals):
    scroll(followers_followgins_count)
    followings_div = driver.execute_script("""return document.querySelector('[style="display: flex; flex-direction: column; padding-bottom: 0px; padding-top: 0px; position: relative;"]');""")
    followings_users = followings_div.find_elements(By.XPATH, './*')
    
    for user in followings_users:
        user_href = user.find_element(By.TAG_NAME, 'a').get_attribute('href')
        if user_href in unmutuals:
            user.find_element(By.TAG_NAME, 'button').click()
            unfollow_btn = driver.find_element(By.XPATH, ".//button[normalize-space(text())='Unfollow']")
            unfollow_btn.click()
            print(f'{user_href[26:-1]} has been unfollowed')
            sleep(1.5)

def close():
    close_button = driver.find_elements(By.TAG_NAME, 'button')[1]
    close_button.click()
    
    
def login():
    username = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Phone number, username, or email"]')
    username.send_keys(os.getenv('USERNAME'))

    password = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Password"]')
    password.send_keys(os.getenv("PASSWORD"))

    log_in = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    log_in.click()

load_dotenv()

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.instagram.com/")

sleep(5)

login()

sleep(9)

try:
    back_up_codes = driver.find_element(By.XPATH, '//button[.//div[text()="backup codes"]]')
    back_up_codes.click()
    sleep(1)
    verification_code = driver.find_element(By.TAG_NAME, 'input')
    verification_code.send_keys(os.getenv("BACKUP_CODE"))
    confirm = driver.find_element(By.XPATH, '//button[contains(., "Confirm")]')
    confirm.click()
except NoSuchElementException:
    print("No 2FA detected")



def confirm_error(spans):
    for span in spans:
        if span.text == 'This code doesn’t work. Check it’s correct or try a new one.':
            return True
    return False

def clear_input(input):
    input.send_keys(Keys.CONTROL + "a")
    input.send_keys(Keys.BACKSPACE)
    
    
def confirm_login(spans, error=False):
    message = 'This code doesn’t work. Check it’s correct or try a new one: ' if error else 'Enter the code sented to your email: '
    code = input(message)
    code_input = driver.find_element(By.TAG_NAME, 'input')
    while len(code) != 6 or not code.isdigit():
        code = input('THE confirmation code should contain 6 digits: ')
    clear_input(code_input)
    code_input.send_keys(code)
    continue_btn = driver.find_element(By.XPATH, '//span[text()="Continue"]')
    continue_btn.click()
    sleep(2)
    spans = driver.find_elements(By.TAG_NAME, 'span')
    if confirm_error(spans):
        confirm_login(spans, error=True)
    else:
        print('logged_in succesfully')
    

spans = driver.find_elements(By.TAG_NAME, 'span')
label = driver.find_element(By.TAG_NAME, 'label').text == 'Code'
confiramtion_needed = ['Check your email' in span.text for span in spans]
if any(confiramtion_needed) and label:
    confirm_login(spans)
    
        
        
sleep(19)
try:
    not_now = driver.find_element(By.XPATH, "//div[text()='Not now']")
    not_now.click()
except NoSuchElementException:
    pass

account_username = os.getenv('USERNAME')
if account_username:
    account_url = f'https://instagram.com/{account_username}'
    driver.execute_script(f"window.open('{account_url}', '_blank');")
else:
    print('USERNAME env variable is not set')


tabs = driver.window_handles
driver.switch_to.window(tabs[-1])



data = get_followers_followings_count()
followings_count = data[0]
followers_count = data[1]

print(f'your followers number is {followers_count}')        
print(f'your followings number is {followings_count}')        

followings = driver.find_element(By.XPATH, "//a[contains(@href, '/following/')]")
followings.click()
sleep(2)
followings_list = get(followings_count)

close()

followers = driver.find_element(By.XPATH, "//a[contains(@href, '/followers/')]")
followers.click()
sleep(2)
followers_list = get(followers_count)

close()
        
unmutuals = [user_link for user_link in followings_list if user_link not in followers_list]


followings.click()
unfollow_unmutuals(followings_count, unmutuals)

