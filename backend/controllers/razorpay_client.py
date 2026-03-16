import razorpay
from flask import current_app

def get_razorpay_client():
    return razorpay.Client(
        auth=(
            current_app.config['RAZORPAY_KEY'],
            current_app.config['RAZORPAY_SECRET']
        )
    )


