import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Cài đặt Chromedriver
chromedriver_autoinstaller.install()

# Danh sách các tài khoản Facebook
accounts = [
   {"email": "100087635589100", "password": "Nguyenthuan12112002"},
   {"email": "100090923691791", "password": "12112002"}
]
# Tùy chọn cho trình duyệt Chrome
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")
options.add_argument("--disable-popup-blocking")

# Hàm đăng nhập và xóa bài viết trong nhóm
def login_and_delete_posts(email, password):
    driver = webdriver.Chrome(options=options)
    try:
        # Đăng nhập vào Facebook
        driver.get("https://www.facebook.com/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "pass").send_keys(password)
        driver.find_element(By.NAME, "login").click()

        # Chờ đến khi đăng nhập thành công
        WebDriverWait(driver, 10).until(EC.url_contains("facebook.com"))

        # Truy cập vào trang Nhóm
        driver.get("https://www.facebook.com/groups/?category=membership")
        time.sleep(5)

        # Click để xem tất cả nhóm đã tham gia
        driver.find_element(By.XPATH, "//a[@aria-label='Xem tất cả']").click()
        time.sleep(2)

        # Lấy danh sách các nhóm
        group_links = set()
        links = driver.find_elements(By.TAG_NAME, 'a')
        for link in links:
            href = link.get_attribute('href')
            if '/groups/' in href and 32 < len(href) < 100:
                cleaned_href = href.split("?__tn__=")[0]
                group_links.add(cleaned_href)

        print(f"Found {len(group_links)} groups")

        # Xóa bài viết trong từng nhóm
        for group_link in group_links:
            delete_posts_in_group(driver, group_link)

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        driver.quit()

# Hàm xóa bài viết trong nhóm
def delete_posts_in_group(driver, group_link):
    try:
        driver.get(group_link)
        time.sleep(5)

        # Click vào "Quản lý bài viết"
        driver.find_element(By.XPATH, "//a[@aria-label='Quản lý bài viết']").click()
        time.sleep(2)

        # Cuộn xuống để tải tất cả bài viết
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2.5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Lấy danh sách các liên kết bài viết
        group_post_links = set()
        links = driver.find_elements(By.TAG_NAME, 'a')
        for link in links:
            href = link.get_attribute('href')
            if '/photo/' in href:
                group_post_links.add(href)

        print(f"Found {len(group_post_links)} posts in group {group_link}")

        # Xóa từng bài viết
        for post_link in group_post_links:
            try:
                driver.get(post_link)
                time.sleep(2)

                # Click vào menu "Hành động với bài viết này"
                driver.find_element(By.XPATH, "//div[@aria-label='Hành động với bài viết này']").click()
                time.sleep(2)

                # Click vào "Xóa ảnh"
                driver.find_element(By.XPATH, "//span[contains(text(), 'Xóa ảnh')]").click()
                time.sleep(2)

                # Xác nhận xóa
                driver.find_element(By.XPATH, "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f xtk6v10']").click()
                time.sleep(3)

                # Kiểm tra có thông báo chặn không
                if "Có vẻ như bạn đang dùng nhầm tính năng này do sử dụng quá nhanh. Bạn tạm thời đã bị chặn sử dụng nó." in driver.page_source:
                    print("Bị chặn, dừng lại!")
                    driver.quit()

            except Exception as e:
                print(f"Failed to delete post {post_link}: {e}")

        print(f"Deleted posts successfully in group: {group_link}")

    except Exception as e:
        print(f"Failed to delete posts in group {group_link}: {e}")

# Lặp qua danh sách các tài khoản và thực hiện các thao tác
for account in accounts:
    email = account["email"]
    password = account["password"]

    print(f"Processing account: {email}")
    login_and_delete_posts(email, password)

print("All accounts processed successfully")
