import os
import tempfile
from dotenv import load_dotenv
from price_notifier import PriceNotifier
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
load_dotenv()

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# ✅ اضافه کردن مسیر یکتا برای user-data-dir
user_data_dir = tempfile.mkdtemp()
chrome_options.add_argument(f'--user-data-dir={user_data_dir}')

def format_price(num):
    return f"{num:,}"

if __name__ == "__main__":
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    product_urls = [
        "https://torob.com/p/a94944c6-5a62-445e-8292-e88dc82f9968/",
        "https://torob.com/p/118e3935-69b1-4cb8-8fc7-5c34a317eb19/",
        "https://torob.com/p/ab048c8b-700a-4a64-9cd2-bb2185a1af79/",
        "https://torob.com/p/8610b3ec-72af-4d64-b398-3acfdda7cdf4/",
        "https://torob.com/p/4dff4119-804b-4c32-b30c-92711c23ca2a/",
        "https://torob.com/p/d6f102fd-c1b4-4ed5-97d6-258d24bfb43b/"
    ]

    target_prices = {
        "ساعت هوشمند هوآوی مدل FIT 3": 7500000,
        "ساعت هوشمند Xiaomi Watch S3 (نسخه گلوبال)": 8000000,
        "پاوربانک انکر مدل PowerCore 20K A1336 200W ظرفیت 20000mAh": 7500000,
        "کوله لپ تاپ 15.6 اینچی شیائومی مدل Business 2": 1100000,
        "کوله پشتی لپ تاپ ضد اب دل مدل 15 - PO1520P": 2000000,
        "پاوربانک وایرلس باسئوس مدل PPCXZ10 با ظرفیت 10000mAh" : 1800000
    }

    notifier = PriceNotifier(product_urls, target_prices, driver)
    notifier.run()