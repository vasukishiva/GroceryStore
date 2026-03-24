from flask import Flask, send_from_directory
from flask_security import Security, utils
from controllers.database import db
from controllers.config import Config
from controllers.user_datastore import user_datastore
from flask_restful import Api
import os
from flask_mail import Mail
from controllers.cache import init_cache


from flask_cors import CORS

def create_app():
    
        app = Flask(__name__)
        app.config.from_object(Config)
        
        # app.config['CACHE_TYPE'] = 'RedisCache'
        # app.config['CACHE_REDIS_URL'] = os.getenv('REDIS_URL')
        # app.config['CACHE_DEFAULT_TIMEOUT'] = 60
        #print("Redis URL:", os.getenv("REDIS_URL"))
        CORS(app)

        db.init_app(app)
        init_cache(app)

        security = Security(app, user_datastore)
        api = Api(app)
        with app.app_context():
            db.create_all()
            admin_role = user_datastore.find_or_create_role(name='admin', description='Administrator')
            user_role = user_datastore.find_or_create_role(name='user', description='End user')
            
            if not user_datastore.find_user(email='admin@gmail.com'):
                user_datastore.create_user(
                    email='admin@gmail.com',
                    password=utils.hash_password('admin123'),
                    roles=[admin_role]
                )
                
            db.session.commit()

        return app, api
    
app, api = create_app()

@app.route('/static/uploads/products/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/uploads/products'), filename)

@app.route('/celery_example', methods=['GET'])
def celery_example():
    from celery_app import example_task
    example_task.delay()
    return {
        "message": "Celery task has been triggered!"
    }, 200
 
@app.route('/generate_csv', methods=['GET'])
def generate_csv():
    from celery_app import generate_csv
    generate_csv.delay()
    return {
        "message": "CSV generation task has been triggered!"
    }, 200

# @app.route('/export-users', methods=['POST'])
# def export_users():
#     from tasks import generate_csv
#     task = generate_csv.delay()
#     return {
#         "message": "CSV generation task has been triggered!",
#         "task_id": task.id
#     }, 200 
# endpoint registrations 
from controllers.authentication_api import LoginAPI, LogoutAPI, RegisterAPI, CheckEmailAPI

api.add_resource(LoginAPI, '/api/login')
api.add_resource(LogoutAPI, '/api/logout')
api.add_resource(RegisterAPI, '/api/register')
api.add_resource(CheckEmailAPI, '/api/check_email')

from controllers.order_api import CheckoutAPI, FakePaymentAPI
api.add_resource(CheckoutAPI, '/checkout')
api.add_resource(FakePaymentAPI, '/fake_payment')

from controllers.crud_apis import CategoryCrudAPI, ProductCrudAPI, LatestProductsAPI, CategoryProductsAPI
api.add_resource(LatestProductsAPI, '/products/latest')
api.add_resource(CategoryCrudAPI, '/categories', '/categories/<int:category_id>')
api.add_resource(ProductCrudAPI, '/products', '/products/<int:product_id>')
api.add_resource(CategoryProductsAPI, '/categories/<int:category_id>/products')

from controllers.action_apis import OfferListAPI, OfferProductAPI, OfferCategoryAPI, OfferMetaAPI, OffersAPI 
api.add_resource(OfferProductAPI, '/offers/products', '/offers/products/<int:product_id>')
api.add_resource(OfferCategoryAPI, '/offers/categories/<int:category_id>')  
api.add_resource(OfferMetaAPI, '/offers/meta')
api.add_resource(OfferListAPI, '/offers/list')
print(type(OfferMetaAPI))
print(type(OffersAPI))



api.add_resource(OffersAPI, '/offers')

from controllers.user_cartorder_crud_apis import UserCartAPI, UserOrderAPI
api.add_resource(UserCartAPI,'/user_cart','/user_cart/<int:cart_item_id>')
api.add_resource(UserOrderAPI,'/orders')
if __name__ == '__main__':
    app.run(debug=True)
    
