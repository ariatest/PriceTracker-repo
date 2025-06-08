from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json

def parse_price(price_text):
    price_text = price_text.replace('تومان', '').replace(',', '').strip()
    if 'تا' in price_text:
        low_price = price_text.split('تا')[0].strip()
        return int(low_price)
    else:
        return int(price_text)


class PriceTracker:
    def __init__(self, chromedriver_path, product_urls, target_prices):
        service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(service=service)
        self.product_urls = product_urls
        self.target_prices = target_prices
        self.discounted_products = []  # برای ذخیره محصولات با قیمت پایین‌تر از هدف

    def check_prices(self):
        for url in self.product_urls:
            self.driver.get(url)
            time.sleep(2)

            try:
                script_tag = self.driver.find_element(By.CSS_SELECTOR, 'script[type="application/ld+json"]')
                data = json.loads(script_tag.get_attribute('innerHTML'))
            except Exception as e:
                print(f"خطا در گرفتن اطلاعات محصول در {url}: {e}")
                continue

            product_name = data.get("name", "نام محصول نامشخص")
            price_text = "قیمت یافت نشد"

            if "offers" in data:
                offers = data["offers"]
                if isinstance(offers, dict):
                    if "price" in offers:
                        price_text = f"{self.format_price(int(offers['price']) // 10)} تومان"
                    elif "lowPrice" in offers and "highPrice" in offers:
                        low_price = int(offers['lowPrice']) // 10
                        high_price = int(offers['highPrice']) // 10
                        price_text = f"{self.format_price(low_price)} تا {self.format_price(high_price)} تومان"

            print(f"{product_name} , قیمت {price_text}")

            try:
                current_price = parse_price(price_text)
            except Exception:
                current_price = None

            if current_price is not None and product_name in self.target_prices:

                target_price = self.target_prices[product_name]
                if current_price < target_price:
                    print(f"⚠️ قیمت محصول '{product_name}' کاهش یافته است!")
                    print(f"قیمت فعلی: {self.format_price(current_price)} تومان، قیمت هدف: {self.format_price(target_price)} تومان")
                    print(f"لینک محصول: {url}")
                    self.discounted_products.append({
                        "name": product_name,
                        "current_price": current_price,
                        "target_price": target_price,
                        "url": url,
                        "price_text": price_text  # اضافه کردن این خط
                    })
            print("=" * 40)

    def close(self):
        self.driver.quit()

    @staticmethod
    def format_price(num):
        return f"{num:,}"
