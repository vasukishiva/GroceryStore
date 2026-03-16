from operator import or_
from flask_restful import Resource
from flask import request, jsonify, make_response
from controllers.user_datastore import user_datastore
from flask_security import utils, auth_token_required, roles_required
from controllers.database import db
from controllers.models import *
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os
from flask import current_app


UPLOAD_FOLDER = 'static/uploads/products/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# if not os.path.exists('static/images/categories/'):
#     os.makedirs('static/images/categories/')
# UPLOAD_FOLDER = 'static/images/categories/'
#ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

#CRUD APIS for the Categories model

class CategoryCrudAPI(Resource):
    def get(self, category_id=None):
        if category_id:
            
            category = Categories.query.get_or_404(category_id)
            result = {
                'id': category.id,
                'name': category.name,
                'description': category.description
               
            }
            return make_response(jsonify(result), 200)
        else:
            categories = Categories.query.all()
            result = []
            for category in categories:
                result.append({
                    'id': category.id,
                    'name': category.name,
                    'description': category.description
                   
                })
            return make_response(jsonify(result), 200)
        
    @auth_token_required
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        if not data or not data.get('name'):
            result = {'message': 'Category name is required'}
            return make_response(jsonify(result), 400)
        name = data.get('name')
        description = data.get('description')
        #image_file = data.get('image_file')
        
        if not name:
            result = {'message': 'Category name is required'}
            return make_response(jsonify(result), 400)
        if not description:
            description = ''
        if Categories.query.filter_by(name=name).first():
            
            result = {'message': 'Category name already exists'}
            return make_response(jsonify(result), 400)
        
        # image_filename = None
        # if image:

        #     filename = secure_filename(image.filename)
        #     image_path = os.path.join(UPLOAD_FOLDER, filename)
        #     image.save(image_path)
        #     image_filename = filename
            
            
        
        # data = request.get_json()
        # if not data or not data.get('name'):
        #     result = {'message': 'Category name is required'}
        #     return make_response(jsonify(result), 400)
        # name = data.get('name')
        # description = data.get('description')
        # image_file = data.get('image_file')
        
        #save images to static/images/categories/
        # image_filename = None
        # if image_file:
        #     filename = f"{name.replace(' ', '_').lower()}.png"
        #     image_path = f"static/images/categories/{filename}"
        #     with open(image_path, "wb") as img_file:
        #         img_file.write(image_file.encode('utf-8'))
        #     image_filename = filename
            
        
        # if Categories.query.filter_by(name=name).first():
        #     result = {'message': 'Category name already exists'}
        #     return make_response(jsonify(result), 400)
        
        
        new_category = Categories(
            name=name,
            description=description
           
        )
        db.session.add(new_category)
        db.session.commit()
        
        result = {
            'message': 'Category created successfully',
            'data': {
                    'id': new_category.id,
                    'name': new_category.name,
                    'description': new_category.description
                    #'image_file': new_category.image_file
                }}
        return make_response(jsonify(result), 201)
    
    @auth_token_required
    @roles_required('admin')
    def put(self, category_id):
        category = Categories.query.get(category_id)
        if not category:
            result = {'message': 'Category not found'}
            return make_response(jsonify(result), 404)
        
        data = request.get_json()
        
        # name = data.get('name')
        # description = data.get('description')
        #image_file = data.get('image_file')
        
        if not data:
            result = {'message': 'No data provided for update'}
            return make_response(jsonify(result), 400)
        name = data.get('name')
        description = data.get('description')
        # image_file = data.get('image_file')
        
        if name:
            if Categories.query.filter(Categories.name == name, Categories.id != category_id).first():
                result = {'message': 'Category name already exists'}
                return make_response(jsonify(result), 400)
            category.name = name
        if description:
            category.description = description
            
        # if image:
            
                
        #     ext = os.path.splitext(image.filename)[1]
        #     filename = secure_filename(f"{image.filename}.{ext}")
        #     image_path = os.path.join(UPLOAD_FOLDER, filename)
        #     image.save(image_path)
        #     category.image_file = filename
            
        # if image_file:
        #     category.image_file = image_file
        
        db.session.commit()
        
        result = {
            'message': 'Category updated successfully',
            'data': {
                    'id': category.id,
                    'name': category.name,
                    'description': category.description
                    #'image_file': category.image_file
                }}
        return make_response(jsonify(result), 200)
    
    @auth_token_required
    @roles_required('admin')
    def delete(self, category_id):
        category = Categories.query.get(category_id)
        if not category:
            result = {'message': 'Category not found'}
            return make_response(jsonify(result), 404)
        
        db.session.delete(category)
        db.session.commit()
        
        result = {'message': 'Category deleted successfully'}
        return make_response(jsonify(result), 200)
    
    
    
# crud apis for Products

class ProductCrudAPI(Resource):
    def get(self, product_id=None):
        category_id = request.args.get('category_id')
        search = request.args.get('search')
        if product_id:
            product = Products.query.get(product_id)
            
            if not product:
                return {'message': 'Product not found'}, 404
            return {
                'id': product.id,   
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'is_offer': product.is_offer,
                'offer_percentage': product.offer_percentage,
                'stock': product.stock,
                'category_id': product.category_id,
                'image_file': product.image_file,
            
                'image_url':f"http://localhost:5000/static/uploads/products/{product.image_file}"
            }
            
        query = Products.query
        if search:
            query = query.filter(or_(
                Products.name.ilike(f'%{search}%'),
                Products.description.ilike(f'%{search}%')
            ))
            
        if category_id:
            query = query.filter_by(category_id=category_id)
            
        products = query.all()
        
        
        # if category_id:
        #     products = Products.query.filter_by(category_id=category_id).all()
        result = []
        for p in products:
            result.append({
                'id': p.id,
                'name': p.name,
                'description': p.description,
                'price': p.price,
                'stock': p.stock,
                'is_offer': p.is_offer,
                'offer_percentage': p.offer_percentage,
                'category_id': p.category_id,
                'image_file': p.image_file,
                'image_url':f"http://localhost:5000/static/uploads/products/{p.image_file}"
            })
        return result, 200
        #     if not product:
        #         result = {'message': 'Product not found'}
        #         return make_response(jsonify(result), 404)
        #     result = {
        #         'id': product.id,
        #         'name': product.name,
        #         'description': product.description,
        #         'price': product.price,
        #         'stock': product.stock,
        #         'category_id': product.category_id
        #     }
        #     return make_response(jsonify(result), 200)
        # else:
        #     products = Products.query.all()
        #     result = []
        #     for product in products:
        #         result.append({
        #             'id': product.id,
        #             'name': product.name,
        #             'description': product.description,
        #             'price': product.price,
        #             'stock': product.stock,
        #             'category_id': product.category_id
        #         })
        #     return make_response(jsonify(result), 200)  

    @auth_token_required
    @roles_required('admin')
    def post(self):
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        stock = request.form.get('stock')
        category_id = request.form.get('category_id')
        file = request.files.get('image')
        
        if not name or not price or not file:
            result = {'message': 'Name, price, and image are required'}
            return make_response(jsonify(result), 400)
        if not allowed_file(file.filename):
            result = {'message': 'Invalid image file type'}
            return make_response(jsonify(result), 400)
        
        filename = secure_filename(file.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        product = Products(
            name=name,
            description=description,
            price=float(price),
            stock=int(stock) if stock else 0,
            category_id = category_id,
            image_file = filename
        )
        db.session.add(product)
        db.session.commit()
        
        return make_response(jsonify({
            'message': 'Product created successfully'}), 201)

    @auth_token_required
    @roles_required('admin')
    def put(self, product_id):
        product = Products.query.get(product_id)
        if not product:
            result = {'message': 'Product not found'}
            return make_response(jsonify(result), 404)
        
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        stock = request.form.get('stock')
        category_id = request.form.get('category_id')
        file = request.files.get('image_file')
        if name:
            product.name = name
        if description:
            product.description = description
        if price:
            product.price = float(price)
        if stock:
            product.stock = int(stock)  
        if category_id:
            product.category_id = category_id
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            product.image_file = filename
        db.session.commit()
        return make_response(jsonify({
            'message': 'Product updated successfully'}), 200)
        
        
        
        
    
    @auth_token_required
    @roles_required('admin')        
    def delete(self, product_id):
        product = Products.query.get(product_id)
        if not product:
            result = {'message': 'Product not found'}
            return make_response(jsonify(result), 404)
        
        db.session.delete(product)
        db.session.commit()
        
        result = {'message': 'Product deleted successfully'}
        return make_response(jsonify(result), 200)
    
    
class LatestProductsAPI(Resource):
    def get(self):
        # products = Products.query.order_by(Products.created_at.desc()).limit(5).all()
        # return [p.to_dict() for p in products]
            latest_products = Products.query.order_by(Products.created_at.desc()).limit(5).all()
            result = []
            for p in latest_products:
                result.append({
                    'id': p.id,
                    'name': p.name,
                    'description': p.description,
                    'price': p.price,
                    'stock': p.stock,
                    'is_offer': p.is_offer,
                    'offer_percentage': p.offer_percentage,
                    'category_id': p.category_id,
                    'image_file': p.image_file,
                    'image_url':f"http://localhost:5000/static/uploads/products/{p.image_file}"
                })
            return make_response(jsonify(result), 200)
    
class CategoryProductsAPI(Resource):
    def get(self, category_id):
        products = Products.query.filter_by(category_id=category_id).all()
        return [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "is_offer": p.is_offer,
                "offer_percentage": p.offer_percentage,
                "image_file": p.image_file
            }
            for p in products
        ], 200
   


