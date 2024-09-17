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

# Thông tin đăng nhập100076418080581

'''email = "61559321912990"
password = "12112002"'''

'''email = "61559127609312"
password = "12112002"'''

email = "61559489194458"
password = "12112002"

'''email = "100025990569347"
password = "0326243170ttt"'''

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
time.sleep(5)
#group_button = driver.find_element(By.XPATH, "//a[@aria-label='Nhóm']")
#group_button.click()
#time.sleep(2)

#tu khoa tim kiem
content_search = "Lập trình"

#click vao tim kiem va thuc hien chuc nang tim kiem nhom
box_search = driver.find_element(By.XPATH, "//input[@aria-label='Tìm kiếm nhóm']")
box_search.click()
box_search.send_keys(content_search)
box_search.send_keys(Keys.RETURN)  # Nhấn phím Enter
time.sleep(2)

#click vao nhom vua tim kiem
url = "https://www.facebook.com/groups/search/groups/?q=" + content_search + "&__tsid__=0.6966745255588549&__epa__=SERP_TAB&__eps__=GROUPS_HOME_SERP_ALL_TAB"
driver.get(url)
time.sleep(2)

#truy cap vao  nhom cua toi
group_search_output = driver.find_element(By.XPATH, "//input[@aria-label='Nhóm của tôi']")
group_search_output .click()
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
    
#khai bao mot list        
group_links = set()  # Sử dụng set để tránh trùng lặp
#lay cac the a trong trang do
links = driver.find_elements(By.TAG_NAME, 'a')

#do dai toi da cua link
max_url_length = 100
min_url_length = 32

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

#noi dung can post
#post_content = "Mình đang có full bộ khóa học(gồm video và tài liệu) kiếm tiền trên nền tảng tiktok,youtube,shoppe đầy đủ từ A-Z có cả tus đi kèm ...Bác nào cần thì inbox mình nhé dỡ mất nhiều tiền cho các thầy lùa"
post_content = """Bác nào cần các khóa này ib mk nhé :
1. LẬP TRÌNH JAVA (4 tuần, cơ bản, nâng cao, WEB, SPRING MVC, SPRING BOOT)
LẬP TRÌNH ANDROID - từ cơ bản đến nâng cao
LẬP TRÌNH PYTHON - 4 tuần, từ zero -hero, ứng dụng thực tế
LẬP TRÌNH C++, c#
LẬP TRÌNH PHP
18 KHÓA LẬP TRÌNH FRONTEN nhe """
#image
image_path = "D:/KHLT.jpg"

#truy cap vao nhom va post bai
def post_to_group(driver, group_link, post_content, image_path):
    driver.get(group_link)
    time.sleep(3)

    try:
        create_post_button = driver.find_element(By.XPATH, "//div[@class='xi81zsa x1lkfr7t xkjl1po x1mzt3pk xh8yej3 x13faqbe']")
        create_post_button.click()
        time.sleep(2)

        photo_video_button = driver.find_element(By.XPATH, "//div[@aria-label='Ảnh/video']")
        photo_video_button.click()
        time.sleep(2)

        for _ in range(2):
            upload_input = driver.find_element(By.XPATH, "//input[@type='file']")
            upload_input.send_keys(image_path)
            time.sleep(2)
        
        post_box = driver.find_element(By.XPATH, "//div[contains(@aria-label,'Bạn viết gì đi...') or contains(@aria-label, 'Tạo bài viết công khai...')]")
        post_box.click()
        for char in post_content:
            post_box.send_keys(char)
            time.sleep(0.000001)  
        time.sleep(2)
                                
        post_button = driver.find_element(By.XPATH, "//div[@aria-label='Đăng']")
        post_button.click()
        time.sleep(3)

        #element = driver.find_element(By.XPATH, "//div[@class='xu06os2 x1ok221b']")
        #element = driver.find_element(By.XPATH, "//div[contains(text(), 'Để bảo vệ cộng đồng khỏi spam, chúng tôi giới hạn tần suất bạn đăng bài, bình luận hoặc làm các việc khác trong khoảng thời gian nhất định. Bạn có thể thử lại sau.')]")
        if driver.find_element(By.XPATH, "//div[contains(text(), 'Để bảo vệ cộng đồng khỏi spam, chúng tôi giới hạn tần suất bạn đăng bài, bình luận hoặc làm các việc khác trong khoảng thời gian nhất định. Bạn có thể thử lại sau.')]").is_displayed():
            print("Phần tử mong muốn hiển thị, dừng lại!")
            driver.quit()
        else:
            print("thuc hien thanh cong group_link: " + group_link)
    
    except Exception as e:
        print(f"Failed to post in group {group_link}: {e}")

for group_link in group_links:
    post_to_group(driver, group_link, post_content, image_path)
    current_window_handle = driver.current_window_handle
    driver.execute_script("window.open('{group_link}');")
    driver.switch_to.window(current_window_handle)
    driver.close()  # Đóng tab trước đó
    driver.switch_to.window(driver.window_handles[-1])

