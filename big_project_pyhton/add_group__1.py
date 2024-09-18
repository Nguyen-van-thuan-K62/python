import tkinter as tk
import sqlite3
import chromedriver_autoinstaller
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tkinter import ttk
from selenium import webdriver
from tkinter import messagebox

class Add_group:

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

        function_frame = ttk.LabelFrame(self.root, text="Chỉnh Sửa Thông Tin Tài Khoản")
        function_frame.pack(padx=20, pady=20, fill="both")

        key_label = ttk.Label(function_frame, text="Từ Khóa Tìm Kiếm:")
        key_label.grid(row=0, column=3, padx=10, pady=5, sticky="w")
        self.key_entry = ttk.Entry(function_frame, width=40)
        self.key_entry.grid(row=0, column=4, padx=10, pady=5)

        search_button = ttk.Button(function_frame, text="Tìm Kiếm", command=self.all_add_group)
        search_button.grid(row=0, column=5, padx=10, pady=5, sticky="w")

        self.button = tk.Button(function_frame, text="Quay lại Giao diện 1", command=self.root.quit)
        self.button.grid(pady=20)

    def all_add_group(self):
        # Cài đặt chromedriver
        chromedriver_autoinstaller.install()

        # Thông tin đăng nhập
        email = "61556243280796"
        password = "12112002"

        self.cursor.execute("SELECT * FROM acc")
        rows = self.cursor.fetchall()

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
        for row in rows :
            email = row['email']
            password = row['password']
            login(email,password)
            
if __name__ == "__main__":
    root = tk.Tk()
    app = Add_group(root)
    root.mainloop()
