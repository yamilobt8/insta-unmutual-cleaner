from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, time
import os
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
import sys
from helper import check_env_variables, setup_driver


if not check_env_variables:
    print('error: set the env variables first')
    sys.exit(1)

def get_followers_followings_count():
    spans = driver.find_elements(By.TAG_NAME, "span")
    followings_count = ""
    followers_count = ""
    
    for i in range(len(spans) - 1):
        if 'following' in spans[i].text:
            followings_count = spans[i+1].text.strip()
            followers_count = spans[i-1].text.strip()
            break
                
    def parse_count(count_str):
        if not count_str:
            return count_str
        if 'K' in count_str:
            return int(float(count_str.replace('K', '')) * 1000)
        elif 'M' in count_str:
            return int(float(count_str.replace('M', '')) * 1000000)
        return int(count_str)
        
            
    return [parse_count(followings_count),parse_count(followers_count)]


def scroll(followers_followings_count):
    ans = followers_followings_count // 12
    times_to_scorll =  ans + 4 if followers_followings_count > 24 else ans + 2
    try:
        scrollable_div = driver.execute_script("""return document.querySelector('[style="height: auto; overflow: hidden auto;"]').parentElement;""")
            
        for i in range(times_to_scorll):
            print(f'{i}/{times_to_scorll}')
            driver.execute_script("""arguments[0].scrollTop = arguments[0].scrollHeight;""", scrollable_div)
            sleep(1.5)
        driver.execute_script("""arguments[0].scrollTo({top: 0,behavior: 'smooth'})""", scrollable_div)
        sleep(1.5)
    except Exception as e:
        print("You have no followings or the scrollable div was not found.")
        print('--------------------Error--------------------')
        print(e)
        print('---------------------------------------------')
        sys.exit(1)
    
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
    username_input = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Phone number, username, or email"]'))
    )
    username_input.send_keys(os.getenv('USERNAME'))

    password_input = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Password"]'))
    )
    
    password_input.send_keys(os.getenv("PASSWORD"))

    log_in = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    log_in.click()

load_dotenv(dotenv_path=".env", override=True)

browser = input("Which browser do you use?\n1) Firefox\n2) Chrome\nEnter 1 or 2: ").strip()
if browser == '1':
    print("Loading Firefox ....")
    driver = setup_driver('firefox')
else:
    print("Loading Chrome ....")
    driver = setup_driver('chrome')


driver.get("https://www.instagram.com/")

wait = WebDriverWait(driver, 15)

sleep(5)

login()

sleep(10)

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



def confirm_error():
    spans = driver.find_elements(By.TAG_NAME, 'span')
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
    if confirm_error():
        confirm_login(spans, error=True)
    else:
        print('logged_in succesfully')
    
try:
    spans = driver.find_elements(By.TAG_NAME, 'span')
    label = driver.find_element(By.TAG_NAME, 'label').text == 'Code'
    confiramtion_needed = ['Check your email' in span.text for span in spans]
    if any(confiramtion_needed) and label:
        confirm_login(spans)
except NoSuchElementException:
    print('No Confirmation detected')
        

try:
    not_now = driver.find_element(By.XPATH, "//div[text()='Not now']")
    not_now.click()
except NoSuchElementException:
    pass

account_username = os.getenv('USERNAME')
if account_username:
    account_url = f'https://instagram.com/{account_username}'
    driver.get(account_url)
else:
    print('USERNAME env variable is not set')

timeout = 30
start_time = time()


while True:
    h2_elements = driver.find_elements(By.TAG_NAME, 'h2')
    contents = [h2_element.text for h2_element in h2_elements]
    print(f'content: {contents}')
    if h2_elements and h2_elements[0].text == account_username:
        print("Profile loaded!")
        break
    
    if time() - start_time > timeout:
        print("Timeout: Profile not loaded.")
        break
    
    contents = [h2_element.text for h2_element in h2_elements]
    
    print(f'h2_elements: {contents}')
    sleep(3)


data = get_followers_followings_count()
followings_count = data[0]
followers_count = data[1]

print(f'your followers number is {followers_count}')        
print(f'your followings number is {followings_count}')        

def click_followers_followings(target):
    followers_followings_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f'//a[contains(@href, "/{account_username}/{target}/")]'))
    )
    try:
        followers_followings_button.click()
    except:
        driver.execute_script("arguments[0].click();", followers_followings_button)

followings = click_followers_followings('following')
sleep(3)
followings_list = get(followings_count)
print(f'followings_list len = {len(followings_list)}')

close()

followings = click_followers_followings('followers')
sleep(3)

followers_list = get(followers_count)
print(f'followers_list len = {len(followers_list)}')

close()
        
unmutuals = [user_link for user_link in followings_list if user_link not in followers_list]
print(f'unmutuals: {unmutuals}')

if not unmutuals:
    print('No unmutuals')
    sys.exit()

print('starting unfollowing process')
followings = click_followers_followings('following')
sleep(3)
unfollow_unmutuals(followings_count, unmutuals)
close()