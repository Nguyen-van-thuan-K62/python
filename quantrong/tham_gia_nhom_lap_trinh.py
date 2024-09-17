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

# Cài đặt chromedriver
chromedriver_autoinstaller.install()

# Thông tin đăng nhập

email = "61556243280796"
password = "12112002"

# Khởi tạo trình duyệt
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")  # Mở trình duyệt ở chế độ toàn màn hình
options.add_argument("--disable-popup-blocking")

#login
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
#khai bao deiver
driver = webdriver.Chrome(options=options)

#thuc hien login
login(driver, email, password)

#truy cap vao cac nhom
driver.get('https://www.facebook.com/groups/?category=membership')
time.sleep(3)

#tu khoa tim kiem
content_search = "IT"

#click vao tim kiem va thuc hien chuc nang tim kiem nhom
box_search = driver.find_element(By.XPATH, "//input[@aria-label='Tìm kiếm nhóm']")
box_search.click()
box_search.send_keys(content_search)
box_search.send_keys(Keys.RETURN)  # Nhấn phím Enter
time.sleep(2)

# Khởi tạo biến đếm số lượt cuộn
scroll_count = 0
max_scroll_count = 5

#auto keo luot cac nhom
last_height = driver.execute_script("return document.body.scrollHeight")
while scroll_count < max_scroll_count:
    # Cuộn xuống cuối trang
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2.5)  # Chờ trang tải thêm nội dung

    # Lấy chiều cao mới của trang sau khi tải thêm
    new_height = driver.execute_script("return document.body.scrollHeight")
        
    # Nếu không có thêm nội dung được tải, dừng lại
    if new_height == last_height:
        break
    # Tăng biến đếm số lượt cuộn
    scroll_count += 1
        
    last_height = new_height
    
#khai bao mot list        
group_links = set()  # Sử dụng set để tránh trùng lặp
#lay cac the a trong trang do
links = driver.find_elements(By.TAG_NAME, 'a')

#lam sach link
for link in links:
    href = link.get_attribute('href')
    if '/groups/' in href and 32 < len(href) < 100 :
        # xoa "?__tn__=" ra khoi link
        cleaned_href = href.split("?__tn__=")[0]
        group_links.add(cleaned_href)
        
print(len(group_links))
print("Nhóm :")
#in ra link
for link in group_links:
    print(link)

def add_group(driver,group_link):
    driver.get(group_link)
    time.sleep(5)
    try:
        add_button = driver.find_element(By.XPATH, "//div[@aria-label='Tham gia nhóm']")
        add_button.click()
        time.sleep(5)        
        print("tham gia thanh cong group_link: " + group_link)
    except Exception as e:
        print(f"Failed to post in group {group_link}: {e}")
        
for group_link in group_links:
    add_group(driver,group_link)
    current_window_handle = driver.current_window_handle
    driver.execute_script("window.open('{group_link}');")
    driver.switch_to.window(current_window_handle)
    driver.close()  # Đóng tab trước đó
    driver.switch_to.window(driver.window_handles[-1])
