from flask_restful import Resource
from flask import request, jsonify, make_response
#from celery_app import send_offer_notification
from controllers.user_datastore import user_datastore
from flask_security import utils, auth_token_required, roles_required, auth_required
from controllers.database import db
from controllers.models import *
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os
from flask import current_app

class OfferProductAPI(Resource):
    def get(self):
        offers = Products.query.filter_by(is_offer=True).all()
        offer_list = []
        for product in offers:
            offer_list.append({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'is_offer': product.is_offer,
                'offer_percentage': product.offer_percentage,
                'final_price': product.price * (1 - product.offer_percentage / 100),
                'stock': product.stock,
                'image_file': product.image_file,
                'category_id': product.category_id
            })
        return make_response(jsonify(offer_list), 200)
    @auth_token_required
    @roles_required('admin')
    def post(self, product_id):
        data = request.get_json()
        offer_percentage = data.get('offer_percentage', 0.0)

        product = Products.query.get(product_id)
        if not product:
            return make_response(jsonify({'message': 'Product not found'}), 404)

        product.is_offer = True
        product.offer_percentage = offer_percentage
        db.session.commit()

        return make_response(jsonify({'message': f'Offer of {offer_percentage}% applied to product {product.name}'}), 200)
    @auth_token_required
    @roles_required('admin')
    def delete(self, product_id):
        
        Offer.query.filter_by(product_id=product_id).delete()
        product = Products.query.get(product_id)
        if product:
            product.is_offer = False
            product.offer_percentage = 0.0
        #     db.session.commit()
        #     return make_response(jsonify({'message': f'Offer removed from product {product.name}
        # if not product:
        #     return make_response(jsonify({'message': 'Product not found'}), 404)

        # product.is_offer = False
        # product.offer_percentage = 0.0
        db.session.commit()

        return make_response(jsonify({'message': f'Offer removed from product {product.name}'}), 200)
    
class OfferCategoryAPI(Resource):
    def get(self, category_id):
        offers = Products.query.filter_by(category_id=category_id, is_offer=True).all()
        offer_list = []
        for product in offers:
            offer_list.append({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'is_offer': product.is_offer,
                'offer_percentage': product.offer_percentage,
                'final_price': product.price * (1 - product.offer_percentage / 100),
                'stock': product.stock,
                'image_file': product.image_file,
                'category_id': product.category_id
            })
        return make_response(jsonify(offer_list), 200)
    @auth_token_required
    @roles_required('admin')
    def post(self, category_id):
        data = request.get_json()
        offer_percentage = data.get('offer_percentage', 0.0)

        products = Products.query.filter_by(category_id=category_id).all()
        if not products:
            return make_response(jsonify({'message': 'No products found in this category'}), 404)

        for product in products:
            product.is_offer = True
            product.offer_percentage = offer_percentage
        db.session.commit()

        return make_response(jsonify({'message': f'Offer of {offer_percentage}% applied to all products in category {category_id}'}), 200)
    @auth_token_required
    @roles_required('admin')
    def delete(self, category_id):
        
        Offer.query.filter_by(category_id=category_id).delete()
        
        products = Products.query.filter_by(category_id=category_id).all()
        # if not products:
        #     return make_response(jsonify({'message': 'No products found in this category'}), 404)

        for product in products:
            product.is_offer = False
            product.offer_percentage = 0.0
        db.session.commit()

        return make_response(jsonify({'message': f'Offer removed from all products in category {category_id}'}), 200)
    
class OfferMetaAPI(Resource):
    def get(self):
        products = Products.query.all()
        categories = Categories.query.all()
        
        return {
            "products":[{ "id": p.id, "name": p.name } for p in products],
            "categories":[{ "id": c.id, "name": c.name } for c in categories]   
        } ,200



class OffersAPI(Resource):
    @auth_token_required
    
    def post(self):
        data = request.get_json()

        offer = Offer(
            offer_type=data['offer_type'],
            product_id=data.get('product_id'),
            category_id=data.get('category_id'),
            offer_percentage=data['offer_percentage']
        )

        db.session.add(offer)
        # product offer
        if offer.offer_type == 'product' and offer.product_id:
            product = Products.query.get(offer.product_id)
            if product:
                product.is_offer = True
                product.offer_percentage = offer.offer_percentage
                #send_offer_notification.delay("Product",product.name, offer.offer_percentage)

        # category offer
        else:
            products = Products.query.filter_by(category_id=offer.category_id).all()
            for product in products:
                product.is_offer = True
                product.offer_percentage = offer.offer_percentage
                # send_offer_notification.delay("Category",product.name, offer.offer_percentage)

        db.session.commit()
        from celery_app import send_offer_notification
        send_offer_notification.delay(offer.id)

        return {"message": "Offer applied successfully"}, 201
        
        
class OfferListAPI(Resource):

    def get(self):

        offers = Offer.query.all()

        result = []

        for o in offers:
            product = Products.query.get(o.product_id) if o.product_id else None
            category = Categories.query.get(o.category_id) if o.category_id else None

            result.append({
                "id": o.id,
                "offer_type": o.offer_type,
                "is_offer": product.is_offer if product else False,
                "offer_percentage": o.offer_percentage,
                "product_id": o.product_id,
                "category_id": o.category_id,
                "product_name": product.name if product else None,
                "category_name": category.name if category else None
            })

        return result, 200
        
    
    