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
        
            
    return [followings_count, followers_count]

def get(followers_followings_count):
    times_to_scorll = int(followers_followings_count) // 12 + 2

    def followings_scroll(times_to_scroll):
        scrollable_div = driver.execute_script("""return document.querySelector('[style="height: auto; overflow: hidden auto;"]').parentElement;""")

        for i in range(times_to_scorll):
            print(f'{i}/{times_to_scorll}')
            driver.execute_script("""arguments[0].scrollTop = arguments[0].scrollHeight;""", scrollable_div)
            sleep(1.5)

    followings_scroll(times_to_scorll)

    a_s = driver.find_elements(By.TAG_NAME, 'a')
    links = []
    seen = set()
                
    for a in a_s:
        href = a.get_attribute('href')
        if href:
            if href not in seen:
                seen.add(href)
                links.append(href)
                
    non_profile_links_number = len(links) - int(followers_followings_count)
    print(non_profile_links_number)
    return links[non_profile_links_number:]

def close():
    close_button = driver.find_elements(By.TAG_NAME, 'button')[1]
    close_button.click()

load_dotenv()

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.instagram.com/")

sleep(5)

username = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Phone number, username, or email"]')
username.send_keys(os.getenv('USERNAME'))

password = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Password"]')
password.send_keys(os.getenv("PASSWORD"))

log_in = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
log_in.click()

sleep(9)

back_up_codes = driver.find_element(By.XPATH, '//button[.//div[text()="backup codes"]]')
back_up_codes.click()

sleep(1)

verification_code = driver.find_element(By.TAG_NAME, 'input')
verification_code.send_keys(os.getenv("BACKUP_CODE"))

confirm = driver.find_element(By.XPATH, '//button[contains(., "Confirm")]')
confirm.click()

sleep(19)

not_now = driver.find_element(By.XPATH, "//div[text()='Not now']")
not_now.click()

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
        
unmutual = [user_link for user_link in followings_list if user_link not in followers_list]

print(len(unmutual))
print(unmutual)

        