from controllers.database import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    fs_token_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))
    
    
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))
    
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))
    
    
class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(255)) # Image file name
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_offer = db.Column(db.Boolean, default=False)
    offer_percentage = db.Column(db.Float, default=0.0)
    category = db.relationship('Categories', backref=db.backref('products', lazy=True))

    def __repr__(self):
        return f'<Products {self.name}>'
    
class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    #image_file = db.Column(db.String(255))
    
    
    def __repr__(self):
        return f'<Categories {self.name}>'
    
class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    
    order_items = db.relationship(
        'OrderItems',
        backref='order',
        cascade="all, delete-orphan",
        lazy=True
    )
    
    def __repr__(self):
        return f'<Orders {self.id} - User {self.user_id}>'
    
class OrderItems(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    # order = db.relationship('Orders', backref=db.backref('order_items', lazy=True))
    product = db.relationship('Products', backref=db.backref('order_items', lazy=True))
    
    def __repr__(self):
        return f'<OrderItems Order {self.order_id} - Product {self.product_id}>'
    
# class Cart(db.Model):
#     __tablename__ = 'cart'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     items = db.relationship('CartItems', backref='cart', lazy=True)
#     user = db.relationship('User', backref=db.backref('cart', uselist=False))
    
#     def __repr__(self):
#         return f'<Cart User {self.user_id}>'


class CartItems(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    product = db.relationship('Products', backref=db.backref('cart_items', lazy=True))
    
    def __repr__(self):
        return f'<CartItems User {self.user_id} - Product {self.product_id}>'
    
    
    
    
class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    offer_type = db.Column(db.String(50))  # 'product' or 'category'
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
  
    offer_percentage = db.Column(db.Float, nullable=False)
    
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    product = db.relationship('Products', backref=db.backref('offers', lazy=True))
    category = db.relationship('Categories', backref=db.backref('offers', lazy=True))
    
    def __repr__(self):
        return f'<Offer Product {self.product_id} - {self.offer_percentage}%>'
    
    
# class Payments(db.Model):
#     id = db.Column(db.Integer, primary_key=True)

#     order_id = db.Column(db.Integer)
#     razorpay_payment_id = db.Column(db.String(120))
#     razorpay_signature = db.Column(db.String(200))

#     amount = db.Column(db.Float)
#     status = db.Column(db.String(30))

#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     def __repr__(self):
#         return f'<Payments Order {self.order_id} - Status {self.status}>'