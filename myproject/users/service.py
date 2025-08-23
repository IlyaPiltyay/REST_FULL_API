import os

import stripe

stripe.api_key = os.getenv('STRIPE_API_KEY')


def create_price(amount, course_name):
    """Создает цену в Stripe с указанием названия курса"""
    return stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product_data={"name": course_name},  # Используем название курса
    )


def create_sessions(price):
    """Создает сессию в страйпе"""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/success",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')


def create_product(product):
    """Создает продукт в страйпе"""
    return stripe.Product.create(name=product)
