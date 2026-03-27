from operator import or_
from flask_restful import Resource
from flask import request, jsonify, make_response
from controllers.user_datastore import user_datastore
from flask_security import utils, auth_token_required, roles_required, current_user
from controllers.database import db
from controllers.models import *
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os
from flask import current_app
from flask import request
from controllers.cache import cache

class RecommendationAPI(Resource):

    @auth_token_required
    def get(self):

        user = current_user

        # 1️ Get last ordered items
        orders = Orders.query.filter_by(user_id=user.id).all()

        product_ids = set()

        for order in orders:
            for item in order.order_items:
                product_ids.add(item.product_id)

        # 2️ If no orders  fallback to cart
        if not product_ids:
            cart_items = CartItems.query.filter_by(user_id=user.id).all()
            for item in cart_items:
                product_ids.add(item.product_id)

        # 3️ If still empty  return popular products
        if not product_ids:
            products = Products.query.limit(5).all()
        else:
            # 4️ Get categories of these products
            categories = set()

            for pid in product_ids:
                product = Products.query.get(pid)
                categories.add(product.category_id)

            # 5️ Recommend products from same categories
            products = Products.query.filter(
                Products.category_id.in_(categories),
                ~Products.id.in_(product_ids)  # exclude already bought
            ).limit(5).all()

        # 6️ Format response
        result = []
        for p in products:
            result.append({
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "image_file": p.image_file
            })

        return result, 200