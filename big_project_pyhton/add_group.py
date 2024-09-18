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

    def add_group(self, driver, group_link):
        """Hàm tham gia group"""
        driver.get(group_link)
        time.sleep(5)
        try:
            add_button = driver.find_element(By.XPATH, "//div[@aria-label='Tham gia nhóm']")
            add_button.click()
            time.sleep(5)
            print(f"Tham gia thành công nhóm: {group_link}")
        except Exception as e:
            print(f"Không thể tham gia nhóm {group_link}: {e}")

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

            scroll_count = 0
            max_scroll_count = 5
            last_height = driver.execute_script("return document.body.scrollHeight")

            while scroll_count < max_scroll_count:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2.5)
                new_height = driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    break
                scroll_count += 1
                last_height = new_height

            group_links = set()
            links = driver.find_elements(By.TAG_NAME, 'a')

            for link in links:
                href = link.get_attribute('href')
                if '/groups/' in href and 32 < len(href) < 100:
                    cleaned_href = href.split("?__tn__=")[0]
                    group_links.add(cleaned_href)

            return group_links
        except Exception as e:
            print(f"Lỗi tìm kiếm nhóm: {e}")
            return set()

    def all_add_group(self):
        """Hàm chính để đăng nhập và tham gia các nhóm"""
        chromedriver_autoinstaller.install()

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-popup-blocking")
        driver = webdriver.Chrome(options=options)

        # Lấy từ khóa tìm kiếm từ Entry
        content_search = self.key_entry.get()

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
                self.add_group(driver, group_link)

        driver.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = Add_group(root)
    root.mainloop()
