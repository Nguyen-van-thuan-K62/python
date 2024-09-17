import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time
import threading
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

chromedriver_autoinstaller.install()

accounts = [
   {"email": "61559321912990", "password": "12112002"},
   {"email": "61559127609312", "password": "12112002"},
   {"email": "61559489194458", "password": "12112002"},
   {"email": "100087635589100", "password": "Nguyenthuan12112002"},
   {"email": "100090923691791", "password": "12112002"},
   {"email": "61556148554968", "pasword": "12112002"},
   {"email": "100025990569347", "password": "0326243170ttt"},
   {"email": "61556825842010", "password": "Nguyenthuan1211@"},
   {"email": "100076418080581", "password": "Nguyenthuan1211"},
]

options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")  # Mở trình duyệt ở chế độ toàn màn hình
options.add_argument("--disable-popup-blocking")

def delete_post_group(driver,group_link):
    driver.get(group_link)
    time.sleep(5)
    try:
        driver.find_element(By.XPATH, "//a[@aria-label='Quản lý bài viết']").click()
        time.sleep(2)

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2.5) 
            
            new_height = driver.execute_script("return document.body.scrollHeight")        
        
            if new_height == last_height:
                break
            last_height = new_height

        group_post_links = set()
        links = driver.find_elements(By.TAG_NAME, 'a')
        for link in links:
            href = link.get_attribute('href')
            if '/photo/' in href:
                group_post_links.add(href)
        print(len(group_post_links))
        print("so bai viet cho trong nhom :")
        
        for post_link in group_post_links:
            print(post_link)
            
            driver.get(post_link)
            time.sleep(2)
            try:
                driver.find_element(By.XPATH, "//div[@aria-label='Hành động với bài viết này']").click()
                time.sleep(2)

                driver.find_element(By.XPATH, "//span[contains(text(), 'Xóa ảnh')]").click()
                time.sleep(2)

                driver.find_element(By.XPATH, "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f xtk6v10']").click()
                time.sleep(3)

                if "Có vẻ như bạn đang dùng nhầm tính năng này do sử dụng quá nhanh. Bạn tạm thời đã bị chặn sử dụng nó." in driver.page_source:
                    print("Bị chặn, dừng lại!")
                    driver.quit()
                    
            except Exception as e:
                print(f"Failed to post in group {post_link}: {e}")

        print("xoa bai viet cho thanh cong group_link: " + group_link)

    except Exception as e:
        print(f"Failed to post in group {group_link}: {e}")

def login_and_delete(email,password):
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://www.facebook.com/")
        time.sleep(2)

        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "pass").send_keys(password)
        driver.find_element(By.NAME, "login").click()
        time.sleep(2)

        driver.get('https://www.facebook.com/groups/?category=membership')
        time.sleep(5)

        #driver.find_element(By.XPATH, "//a[@aria-label='Xem tất cả']").click()
        #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Xem tất cả']"))).click()
        driver.get('https://www.facebook.com/groups/joins/?nav_source=tab')
        time.sleep(2)

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2.5)  

            new_height = driver.execute_script("return document.body.scrollHeight")
                
            if new_height == last_height:
                break
                
            last_height = new_height
                 
        group_links = set()  
    
        links = driver.find_elements(By.TAG_NAME, 'a')

        for link in links:
            href = link.get_attribute('href')
            if '/groups/' in href and 32 < len(href) < 100 :
                cleaned_href = href.split("?__tn__=")[0]
                group_links.add(cleaned_href)
                
        print(len(group_links))
        print("Nhóm :")

        for link in group_links:
            print(link)

        for group_link in group_links:
            delete_post_group(driver,group_link)
            current_window_handle = driver.current_window_handle
            driver.execute_script("window.open('{group_link}');")
            driver.switch_to.window(current_window_handle)
            driver.close()  # Đóng tab trước đó
            driver.switch_to.window(driver.window_handles[-1])

    except Exception as e:
        print(f"Error: {str(e)}")

for account in accounts:
    email = account["email"]
    password = account["password"]

    print(f"Processing account: {email}")
    login_and_delete(email, password)

print("All accounts processed successfully")







