from price_tracker import PriceTracker

class EmailContentBuilder:
    def __init__(self, discounted_products):
        self.discounted = discounted_products

    def build(self):
        if not self.discounted:
            return "هیچ محصولی قیمتش کاهش نیافته."

        lines = ["لیست محصولات با قیمت کاهش یافته:\n"]
        for product in self.discounted:
            lines.append(f"{product['name']} , قیمت {product['price_text']}")
            lines.append(f"⚠️ قیمت محصول '{product['name']}' کاهش یافته است!")
            lines.append(
                f"قیمت فعلی: {PriceTracker.format_price(product['current_price'])} تومان، "
                f"قیمت هدف: {PriceTracker.format_price(product['target_price'])} تومان"
            )
            lines.append(f"لینک محصول: {product['url']}")
            lines.append("=" * 40)
        return "\n".join(lines)