import tkinter as tk
import sqlite3
import chromedriver_autoinstaller
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tkinter import ttk
from selenium import webdriver
from tkinter import messagebox
from tkinter import scrolledtext

class Post_group:

    # Connect to the database
    conn = sqlite3.connect('via.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS acc (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT
    )
    ''')

    def __init__(self, root):
        self.root = root
        self.root.title("Add_group")
        self.root.geometry("700x700")

        post_frame = ttk.LabelFrame(self.root, text="Nhap cac thong tin")
        post_frame.pack(padx=20, pady=20, fill="both")

        # Keyword for group search
        keyword_label = ttk.Label(post_frame, text="Từ khóa tìm kiếm nhóm:")
        keyword_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.keyword_entry = ttk.Entry(post_frame, width=40)
        self.keyword_entry.grid(row=2, column=1, padx=10, pady=5)

        # Post content
        content_label = ttk.Label(post_frame, text="Nội dung bài đăng:")
        content_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.content_text = scrolledtext.ScrolledText(post_frame, width=40, height=10)
        self.content_text.grid(row=3, column=1, padx=10, pady=5)

        # Image path
        image_label = ttk.Label(post_frame, text="Đường dẫn ảnh:")
        image_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.image_entry = ttk.Entry(post_frame, width=30)
        self.image_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.browse_button = ttk.Button(post_frame, text="Chọn ảnh", command=self.browse_image)
        self.browse_button.grid(row=4, column=2, padx=10, pady=5)

        # Start button
        start_button = ttk.Button(self.root, text="Bắt đầu đăng bài", command=self.start_posting)
        start_button.pack(pady=20)



    def login(self, driver, email, password):
        """Hàm đăng nhập Facebook"""
        driver.get("https://www.facebook.com/")
        time.sleep(2)
        try:
            email_field = driver.find_element(By.ID, "email")
            password_field = driver.find_element(By.ID, "pass")
            login_button = driver.find_element(By.NAME, "login")

            email_field.send_keys(email)
            password_field.send_keys(password)
            login_button.click()
            time.sleep(2)
            print(f"Đăng nhập thành công với {email}")
        except Exception as e:
            print(f"Đăng nhập thất bại với {email}: {e}")

    def post_group(driver, group_link,content, image_path):
        driver.get(group_link)
        time.sleep(2)
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
        
            # for char in post_content:
            post_box.send_keys(content)
                # time.sleep(0.000001)  
            time.sleep(2)
                    
            post_button = driver.find_element(By.XPATH, "//div[@aria-label='Đăng']")
            post_button.click()
            time.sleep(4)

            if driver.find_element(By.XPATH, "//div[contains(text(), 'Để bảo vệ cộng đồng khỏi spam, chúng tôi giới hạn tần suất bạn đăng bài, bình luận hoặc làm các việc khác trong khoảng thời gian nhất định. Bạn có thể thử lại sau.')]").is_displayed():
                print("Phần tử mong muốn hiển thị, dừng lại!")
                driver.quit()
            else:
                print("thuc hien thanh cong group_link: " + group_link)
        
        except Exception as e:
            print(f"Failed to post in group {group_link}: {e}")

    def search_groups(self, driver, content_search):
        """Hàm tìm kiếm nhóm và trả về danh sách link nhóm"""
        driver.get('https://www.facebook.com/groups/?category=membership')
        time.sleep(3)

        try:
            box_search = driver.find_element(By.XPATH, "//input[@aria-label='Tìm kiếm nhóm']")
            box_search.click()
            box_search.send_keys(content_search)
            box_search.send_keys(Keys.RETURN)
            time.sleep(2)

            url = "https://www.facebook.com/groups/search/groups/?q=" + content_search + "&__tsid__=0.6966745255588549&__epa__=SERP_TAB&__eps__=GROUPS_HOME_SERP_ALL_TAB"
            driver.get(url)
            time.sleep(2)

            group_search_output = driver.find_element(By.XPATH, "//input[@aria-label='Nhóm của tôi']")
            group_search_output .click()
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
                    
            return group_links
        except Exception as e:
            print(f"Lỗi tìm kiếm nhóm: {e}")
            return set()

    def all_post_group(self):
        """Hàm chính để đăng nhập và tham gia các nhóm"""
        chromedriver_autoinstaller.install()

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-popup-blocking")
        driver = webdriver.Chrome(options=options)

        # Lấy từ khóa tìm kiếm từ Entry
        content_search = self.keyword_entry.get()
        content = self.content_text.get("1.0", tk.END)
        image_path = self.image_entry.get()

        if not content_search:
            messagebox.showerror("Lỗi", "Bạn cần nhập từ khóa tìm kiếm!")
            return

        self.cursor.execute("SELECT email, password FROM acc")
        rows = self.cursor.fetchall()

        for row in rows:
            email, password = row
            self.login(driver, email, password)

            group_links = self.search_groups(driver, content_search)

            for group_link in group_links:
                self.post_group(driver, group_link,content,image_path)

        driver.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = Post_group(root)
    root.mainloop()
