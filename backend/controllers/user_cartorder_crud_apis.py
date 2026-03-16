from flask_restful import Resource
from flask import request, jsonify, make_response
from sqlalchemy import or_
from controllers.user_datastore import user_datastore
from flask_security import utils, auth_token_required, roles_required, current_user, auth_required
from controllers.database import db
from controllers.models import *
from datetime import datetime, timedelta


#CART APIS
class UserCartAPI(Resource):
    #@auth_token_required
    @auth_required('token')
    
    
    def get(self):
        user= current_user
        user_id = user.id
        print("Current user ID:", user_id)
        #user = user_datastore.get_user(user_id)
        if not user:    
            result = {'message': 'User not found'}
            return make_response(jsonify(result), 404)  
        
        cart_items = CartItems.query.filter_by(user_id=user_id).join(Products).all()
        print("Current user:", current_user.id)
        print("Cart items count:", len(cart_items))


        result = []
        for item in cart_items:
            product = item.product
            base_price = product.price
            # Apply offer if available
            
            offer = Offer.query.filter(Offer.is_active == True, or_(Offer.product_id == product.id, Offer.category_id == product.category_id)).first()
            
            final_price = base_price
            offer_percentage = 0.0
            if offer:
                offer_percentage = offer.offer_percentage
                final_price = base_price * (1 - offer_percentage / 100)
                
            
            #product = Products.query.get(item.product_id)
            result.append({
                'id': item.id,
                'product_id': item.product_id,
                'product_name': item.product.name,
                'quantity': item.quantity,
                
                'base_price': base_price,
                'offer_percentage': offer_percentage,
                'final_price': round(final_price, 2),
                
                # 'price': item.product.price,
                'total_price': round(final_price * item.quantity, 2)
            })
        return {
                "items":result,
                "count":len(result)},200
            
            # result.append({
            #     'cart_item_id': item.id,
            #     'product_id': item.product_id,
            #     'product_name': item.product.name,
            #     'quantity': item.quantity,
            #     'price_per_unit': item.product.price,
            #     'total_price': item.product.price * item.quantity
            # })
        #return make_response(jsonify(result), 200)
    #@auth_token_required
    @auth_required('token')
    @roles_required('user') 
    def post(self):
        data = request.get_json()
        user = current_user
        
        if not data:
            result = {'message': 'No input data provided'}
            return make_response(jsonify(result), 400)
        #user_id = request.user.id
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        # user = user_datastore.get_user(user_id)
        # if not user:
        #     result = {'message': 'User not found'}
        #     return make_response(jsonify(result), 404)
        
        if not product_id:
            result = {'message': 'Product ID is required'}
            return make_response(jsonify(result), 400)
        
        # product = Products.query.get(product_id)
        # if not product:
        #     result = {'message': 'Product not found'}
        #     return make_response(jsonify(result), 404)
        
        # if product.stock < quantity:
        #     result = {'message': 'Insufficient stock'}
        #     return make_response(jsonify(result), 400)
        
        # cart = Cart.query.filter_by(user_id=user.id).first()
        # if not cart:
        #     cart = Cart(user_id=user.id)
        #     db.session.add(cart)
        #     db.session.commit()
            
        cart_item = CartItems.query.filter_by(user_id=user.id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItems(
                user_id=user.id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
        
        db.session.commit()
        return make_response(jsonify({'message': 'Product added to cart successfully'}), 201)
        
        # result = {
        #     'message': 'Product added to cart successfully',
        #     'cart_item': {
        #         'cart_item_id': cart_item.id,
        #         'product_id': product.id,
        #         'product_name': product.name,
        #         'quantity': cart_item.quantity,
        #         'price_per_unit': product.price,
        #         'total_price': product.price * cart_item.quantity
        #     }
        # }
        #return make_response(jsonify(result), 201)
    @auth_required('token')
    @roles_required('user') 
    
    def put(self, cart_item_id):
        data = request.get_json()
        quantity = data.get('quantity')
        
        cart_item = CartItems.query.get(cart_item_id)
        if not cart_item:
            result = {'message': 'Cart item not found'}
            return make_response(jsonify(result), 404)
        
        # product = Products.query.get(cart_item.product_id)
        # if product.stock < quantity:
        #     result = {'message': 'Insufficient stock'}
        #     return make_response(jsonify(result), 400)
        
        cart_item.quantity = data['quantity']
        db.session.commit()
        return make_response(jsonify({'message': 'Cart item updated successfully'}), 200)
        
        # result = {
        #     'message': 'Cart item updated successfully',
        #     'cart_item': {
        #         'cart_item_id': cart_item.id,
        #         'product_id': product.id,
        #         'product_name': product.name,
        #         'quantity': cart_item.quantity,
        #         'price_per_unit': product.price,
        #         'total_price': product.price * cart_item.quantity
        #     }
        # }
        #return make_response(jsonify(result), 200)
    
    @auth_required('token')
    @roles_required('user')
    def delete(self, cart_item_id):
        cart_item = CartItems.query.get(cart_item_id)
        if not cart_item:
            result = {'message': 'Cart item not found'}
            return make_response(jsonify(result), 404)
        
        db.session.delete(cart_item)
        db.session.commit()
        
        result = {'message': 'Cart item deleted successfully'}
        return make_response(jsonify(result), 200)
    
    
#ORDER APIS
class UserOrderAPI(Resource):
    @auth_required('token', 'session')
    
    def post(self):
        user = current_user
        # data = request.get_json()
        # user_id = data.get('user_id')
        
        # user = user_datastore.get_user(user_id)
        if not user:
            result = {'message': 'User not found'}
            return make_response(jsonify(result), 404)
        
        cart_items = CartItems.query.filter_by(user_id=user.id).all()
        if not cart_items:
            result = {'message': 'Cart is empty'}
            return make_response(jsonify(result), 400)
        
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        
        new_order = Orders(
            user_id=user.id,
            total_amount=total_amount,
            status='Pending'
        )
        db.session.add(new_order)
        db.session.commit()
        
        for item in cart_items:
            order_item = OrderItems(
                order_id=new_order.id,
                product_id=item.product.id,
                quantity=item.quantity,
                price=item.product.price
            )
            db.session.add(order_item)
            product = Products.query.get(item.product.id)
            product.stock -= item.quantity
            db.session.delete(item)
        
        db.session.commit()
        
        result = {
            'message': 'Order placed successfully',
            'order': {
                'order_id': new_order.id,
                'total_amount': new_order.total_amount,
                'status': new_order.status,
                'created_at': new_order.created_at
            }
        }
        return make_response(jsonify(result), 201)
    
    @auth_required('token', 'session')
    
    def get(self):
        print("CURRENT USER:", current_user)
        print("USER ID:", current_user.id)

        user = current_user
        if not user:
            result = {'message': 'User not found'}
            return make_response(jsonify(result), 404)
        
        orders = Orders.query.filter_by(user_id=user.id).all()
        
        result = []
        for order in orders:
            order_data = {
                'order_id': order.id,
                'total_amount': order.total_amount,
                'status': order.status,
                'created_at': order.created_at.strftime("%Y-%m-%d %H:%M"),

                'items': []
            }
            for item in order.order_items:
                order_data['items'].append({
                    'product_id': item.product.id,
                    'product_name': item.product.name,
                    'quantity': item.quantity,
                    'price_per_unit': item.price,
                    'total_price': item.price * item.quantity
                })
            result.append(order_data)
        
        return make_response(jsonify(result), 200)
