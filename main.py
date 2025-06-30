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
    times_to_scorll = int(followers_followings_count) // 12 + 3

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
    
def unfollow():
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    buttons[-2].click()

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
        
unmutuals = [user_link for user_link in followings_list if user_link not in followers_list]

# for unmutual in unmutuals[:5]:
#     driver.get(unmutual)
    
        

followings.click()
# i need to add the scroll
followings_div = driver.execute_script("""return document.querySelector('[style="display: flex; flex-direction: column; padding-bottom: 0px; padding-top: 0px; position: relative;"]');""")

child_elements = followings_div.find_elements(By.XPATH, './/*')

buttons_count = 0
unfollow_buttons = []


for child in child_elements:
    tag_name = child.tag_name
    if tag_name == 'button':
        buttons_count += 1
        unfollow_buttons.append(child)
        
for i, following in enumerate(followings_list):
    if following in unmutuals:
        unfollow_buttons[i].click()
        sleep(1)
        unfollow()
        
    
      
def unfollow():
    try:
        confirm_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="Unfollow"]'))
        )
        confirm_button.click()
    except Exception:
        print('button not found')  
    sleep(2)

buttons = driver.find_elements(By.TAG_NAME, 'button')
print(len(buttons))



print(len(unfollow_buttons))
print(buttons_count)


buttons = driver.find_elements(By.TAG_NAME, 'button')
unfollowing_buttons = []
for button in buttons:
    if button.text == 'Following':
        unfollowing_buttons.append(button)
        
print(len(unfollowing_buttons))

for i, following in enumerate(followings_list):
    if following in unmutuals:
        unfollowing_buttons[i].click()
        unfollow()