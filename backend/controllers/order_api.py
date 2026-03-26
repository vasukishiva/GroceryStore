from flask_restful import Resource
from flask_security import current_user
from controllers.database import db
from controllers.models import CartItems, Orders, OrderItems, Offer
from flask import request, jsonify, make_response
from flask_security import auth_required
from sqlalchemy import or_
class CheckoutAPI(Resource):
    @auth_required('token')
    def post(self):

        user_id = current_user.id

        cart_items = CartItems.query.filter_by(user_id=user_id).all()

        if not cart_items:
            return {"message": "Cart is empty"}, 400

        total = 0

        # ✅ Step 1: calculate total
        for item in cart_items:
            product = item.product
            base_price = product.price

            offer = Offer.query.filter(
                Offer.is_active == True,
                or_(
                    Offer.product_id == product.id,
                    Offer.category_id == product.category_id
                )
            ).first()

            final_price = base_price

            if offer:
                final_price = base_price * (1 - offer.offer_percentage / 100)

            total += final_price * item.quantity

        # ✅ Step 2: create ONE order
        order = Orders(
            user_id=user_id,
            total_amount=total,
            status="Pending"
        )

        db.session.add(order)
        db.session.flush()  # ✅ get order.id without commit

        # ✅ Step 3: add MULTIPLE items
        for item in cart_items:
            product = item.product
            base_price = product.price

            offer = Offer.query.filter(
                Offer.is_active == True,
                or_(
                    Offer.product_id == product.id,
                    Offer.category_id == product.category_id
                )
            ).first()

            final_price = base_price

            if offer:
                final_price = base_price * (1 - offer.offer_percentage / 100)

            order_item = OrderItems(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=round(final_price, 2)
            )

            db.session.add(order_item)

        # ✅ Step 4: clear cart
        CartItems.query.filter_by(user_id=user_id).delete()

        db.session.commit()

        return {
            "message": "Order placed successfully",
            "order_id": order.id,
            "total": total
        }, 200

























# class CheckoutAPI(Resource):
    
#     @auth_required('token')
    
#     def post(self):

#         user_id = current_user.id

#         #  Get cart items
#         cart_items = CartItems.query.filter_by(user_id=user_id).all()

#         if not cart_items:
#             return {"message": "Cart is empty"}, 400

#         total = 0
        
#         for item in cart_items:
#             product = item.product
#             base_price = product.price

#             offer = Offer.query.filter(
#                 Offer.is_active == True,
#                 or_(
#                     Offer.product_id == product.id,
#                     Offer.category_id == product.category_id
#                 )
#             ).first()

#             final_price = base_price

#             if offer:
#                 final_price = base_price * (1 - offer.offer_percentage / 100)

#             total += final_price * item.quantity

#         #######################################
#         # #  Calculate total
#         # for item in cart_items:
#         #     total += item.product.price * item.quantity
        
#         #  Create Order
#         ###########################################
#         order = Orders(
#             user_id=user_id,
#             total_amount=total,
#             status="Pending"
#             )

#             db.session.add(order)
#             db.session.commit()  # important for order.id
        
#             order_item = OrderItems(
#                     order_id=order.id,
#                     product_id=item.product_id,
#                     quantity=item.quantity,
#                     price=round(final_price, 2)   # SAVE discounted price
#                 )

#             db.session.add(order_item)
        
        
#         ############################################
#         # Clear cart
#         CartItems.query.filter_by(user_id=user_id).delete()

#         db.session.commit()

#         return {
#             "message": "Order placed successfully",
#             "order_id": order.id,
#             "total": total
#         }, 200

class FakePaymentAPI(Resource):

    @auth_required('token')
    def post(self):

        data = request.get_json()
        order_id = data.get("order_id")

        order = Orders.query.get(order_id)

        if not order:
            return {"message": "Order not found"}, 404

        # Mark order as PAID
        order.status = "PAID"

        db.session.commit()

        return {
            "message": "Payment successful",
            "order_id": order.id,
            "status": order.status
        }, 200
       





















###########################################
        # #  Create OrderItems
        # for item in cart_items:
        #     order_item = OrderItems(
        #         order_id=order.id,
        #         product_id=item.product_id,
        #         quantity=item.quantity,
        #         price=item.product.price
        #     )
        #     db.session.add(order_item)











# class CreatePaymentAPI(Resource):

#     @auth_required('token')
#     def post(self, order_id):

#         order = Orders.query.get(order_id)

#         razorpay_order = client.order.create({
#             "amount": int(order.total_amount * 100),
#             "currency": "INR",
#             "payment_capture": 1
#         })

#         order.razorpay_order_id = razorpay_order['id']
#         db.session.commit()

#         return {
#             "razorpay_order_id": razorpay_order['id'],
#             "amount": order.total_amount,
#             "key": "YOUR_KEY"
#         }, 200
        
    
