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
import pyautogui

# Cài đặt chromedriver
chromedriver_autoinstaller.install()

# Thông tin đăng nhập
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

# Khởi tạo trình duyệt cho mỗi tài khoản
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")
options.add_argument("--disable-popup-blocking")

# Hàm để đăng nhập và thực hiện các thao tác trên Facebook
def perform_actions(email, password):
    try:
        # Khởi tạo trình duyệt
        driver = webdriver.Chrome(options=options)

        # Hàm đăng nhập
        def login(driver, email, password):
            driver.get("https://www.facebook.com/")
            time.sleep(2)
            email_field = driver.find_element(By.ID, "email")
            password_field = driver.find_element(By.ID, "pass")
            login_button = driver.find_element(By.NAME, "login")

            email_field.send_keys(email)
            password_field.send_keys(password)
            login_button.click()
            time.sleep(2)

        # Thực hiện đăng nhập
        login(driver, email, password)

        # Truy cập vào trang Nhóm trên Facebook
        driver.get('https://www.facebook.com/groups/?category=membership')
        time.sleep(3)

        #truy cap vao cac nhom da tham gia
        all_button = driver.find_element(By.XPATH, "//a[@aria-label='Xem tất cả']")
        all_button.click()
        time.sleep(2)

        #auto keo luot cac nhom
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
        # Cuộn xuống cuối trang
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2.5)  # Chờ trang tải thêm nội dung

            # Lấy chiều cao mới của trang sau khi tải thêm
            new_height = driver.execute_script("return document.body.scrollHeight")
        
            # Nếu không có thêm nội dung được tải, dừng lại
            if new_height == last_height:
                break
        
            last_height = new_height
    

        # Lấy các liên kết nhóm
        group_links = set()
        links = driver.find_elements(By.TAG_NAME, 'a')
        for link in links:
            href = link.get_attribute('href')
            if '/groups/' in href and 32 < len(href) < 100:
                cleaned_href = href.split("?__tn__=")[0]
                group_links.add(cleaned_href)

        print(f"Logged in and found {len(group_links)} groups with account: {email}")

        
        def delete_post_group(driver,group_link):
            driver.get(group_link)
            time.sleep(5)
            try:
                #click quan ly bai viet
                QLBV_button = driver.find_element(By.XPATH, "//a[@aria-label='Quản lý bài viết']")
                QLBV_button.click()
                time.sleep(2)

                #auto keo luot cac nhom
                last_height = driver.execute_script("return document.body.scrollHeight")
                while True:
                    # Cuộn xuống cuối trang
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2.5)  # Chờ trang tải thêm nội dung
                    # Lấy chiều cao mới của trang sau khi tải thêm
                    new_height = driver.execute_script("return document.body.scrollHeight")        
                    # Nếu không có thêm nội dung được tải, dừng lại
                    if new_height == last_height:
                        break
                    last_height = new_height
    
                group_post_links = set()
                links = driver.find_elements(By.TAG_NAME, 'a')
                for link in links:
                    href = link.get_attribute('href')
                    #if '/groups/' in href and 100 < len(href):
                    #cleaned_href = href.split("?__tn__=")[0]
                    if '/photo/' in href:
                        group_post_links.add(href)
                print(len(group_post_links))
                print("so bai viet cho trong nhom :")
                #in ra link'''
                for post_link in group_post_links:
                    print(post_link)
            
                    driver.get(post_link)
                    time.sleep(2)
                    try:
                        group_post_menu_button = driver.find_element(By.XPATH, "//div[@aria-label='Hành động với bài viết này']")
                        group_post_menu_button.click()
                        time.sleep(2)

                        group_post_clear_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Xóa ảnh')]")
                        group_post_clear_button.click()
                        time.sleep(2)

                        #group_post_clear_alert_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Xóa')]")
                        group_post_clear_alert_button = driver.find_element(By.XPATH, "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f xtk6v10']")
                        group_post_clear_alert_button.click()
                        time.sleep(3)

                        if driver.find_element(By.XPATH, "//div[contains(text(), 'Có vẻ như bạn đang dùng nhầm tính năng này do sử dụng quá nhanh. Bạn tạm thời đã bị chặn sử dụng nó.')]").is_displayed():
                            print("Phần tử mong muốn hiển thị, dừng lại!")
                            driver.quit()
                    
                    except Exception as e:
                        print(f"Failed to post in group {post_link}: {e}")

                print("xoa bai viet cho thanh cong group_link: " + group_link)
            except Exception as e:
                print(f"Failed to post in group {group_link}: {e}")

        # Đăng bài vào từng nhóm đã tìm thấy
        for group_link in group_links:
            delete_post_group(driver,group_link)
            current_window_handle = driver.current_window_handle
            driver.execute_script("window.open('{group_link}');")
            driver.switch_to.window(current_window_handle)
            driver.close()  # Đóng tab trước đó
            driver.switch_to.window(driver.window_handles[-1])

    except Exception as e:
        print(f"Error with account {email}: {e}")

    finally:
        driver.quit()

# Sử dụng threading để thực hiện đồng thời trên các tài khoản
threads = []
for idx, account in enumerate(accounts):
    thread = threading.Thread(target=perform_actions, args=(account["email"], account["password"]))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
