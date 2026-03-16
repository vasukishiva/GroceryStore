from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0')

celery.conf.update(
    timezone='Asia/Kolkata',
    enable_utc=False,
)


from app import app
import time
from mail import send_email
from controllers.models import User

@celery.task
def example_task():
    time.sleep(10)  # Simulate a long-running task
    print("Task completed")
    
    
    

@celery.task()
def generate_csv():
    
    # get all users from the database
    from controllers.models import User
    with app.app_context():
        users = User.query.all()
    # create a CSV file
        import csv
        filename = 'users.csv'
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Email'])
            for user in users:
                writer.writerow([user.id, user.email])
        print(f"CSV file '{filename}' has been generated with {len(users)} users.")
        
        send_email('user1@gmail.com', 'User Export Completed', f'The user export has been completed. The file {filename} has been generated.')

@celery.task()
def send_daily_remainder():
    with app.app_context():
        subject = "Daily Reminder"
        body = "This is your daily reminder to check the grocery store app for new offers and updates opens now!"  
        users = User.query.all()
        for user in users:
            send_email(user.email, subject, body)  
            
        return "Daily reminder emails have been sent to all users."


from celery.schedules import crontab
from datetime import timedelta

celery.conf.beat_schedule = {
    'send-daily-reminder': {
        'task': 'celery_app.send_daily_remainder',
        #'schedule': timedelta(seconds=3),
        'schedule': crontab(hour=9, minute=0),  # Every day at 9:00 AM
    },  
}

@celery.task()
def send_offer_notification(offer_id):
    
    from controllers.models import Products, Categories, User, Offer 
    with app.app_context():
        
        offer = Offer.query.get(offer_id)
        if not offer:
            print(f"Offer with ID {offer_id} not found.")
            return
        
        subject = "New Offer Available!"
        if offer.product_id:
            product = Products.query.get(offer.product_id)
            body = f"A new offer of {offer.offer_percentage}% is now available on the product: {product.name}."
        else:
            category = Categories.query.get(offer.category_id)
            body = f"A new offer of {offer.offer_percentage}% is now available on all products in the category: {category.name}."
        
        users = User.query.all()
        for user in users:
            send_email(user.email, subject, body)
        
        print(f"Offer notification emails have been sent for offer ID {offer_id}.")       