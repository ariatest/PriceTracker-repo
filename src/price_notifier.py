from price_tracker import PriceTracker
from email_content_builder import EmailContentBuilder
import os
from email_sender import EmailSender
from dotenv import load_dotenv

load_dotenv()

class PriceNotifier:
    def __init__(self, product_urls, target_prices):
        self.tracker = PriceTracker(product_urls, target_prices)

    def run(self):
        self.tracker.check_prices()
        discounted = self.tracker.discounted_products

        builder = EmailContentBuilder(discounted)
        email_body = builder.build()
        print(email_body)

        self.tracker.close()

        if not discounted:
            return

        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("GOOGLE_ACC_PASSWORD")
        receiver_email = os.getenv("RECEIVER_EMAIL")

        if not all([sender_email, sender_password, receiver_email]):
            print("خطا: مقادیر ایمیل یا پسورد در .env تنظیم نشده‌اند.")
            return

        sender = EmailSender(sender_email, sender_password, receiver_email)
        sender.send("Torob Wishlist Tracker", email_body)
