"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User,Company, Category,Product,ProductOrders
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

# company endpoints ////////////////////////////////////////////////////

@api.route('/company', methods=['GET'])
def get_companies():
    all_companies = Company.query.all()
    results = list(map(lambda elemento: elemento.serialize() , all_companies))

    return jsonify(results), 200


@api.route('/company/<int:company_id>', methods=['GET'])
def get_company(company_id):
    one_company = Company.query.filter_by(id=company_id).first()

    return jsonify(one_company.serialize()), 200


@api.route('/company', methods=['POST'])
def add_company():
    body= request.get_json()
    new_company = Company(
        name=body['name'],
        email=body['email'],
        password=body['password']
    )
    db.session.add(new_company)
    db.session.commit()

    return jsonify(new_company.serialize()), 201

@api.route('/company/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    one_company = Company.query.filter_by(id=company_id).first()
    db.session.delete(one_company)
    db.session.commit()
    response_body = {
        "msg": "Company eliminada correctamente",
        "company_id": company_id,
        
    }

    return jsonify(response_body), 200

@api.route('/company/<int:company_id>', methods=['PUT'])
def update_company(company_id):
    company = Company.query.filter_by(id=company_id).first()
    body= request.get_json()
    if 'name' in body:
        company.name = body['name']
    if 'email' in body:
        company.email = body['email']
    if 'password' in body:
        company.password = body['password']
    db.session.commit()
 

    return jsonify(company.serialize()), 200


#Endpoint product

@api.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    results = list(map(lambda elemento: elemento.serialize() , all_products))

    return jsonify(results), 200


@api.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    one_product = Product.query.filter_by(id=product_id).first()

    return jsonify(one_product.serialize()), 200


@api.route('/product', methods=['POST'])
def add_product():
    body= request.get_json()
    new_product = Product(
        name=body['name'],
        description=body['description'],
        quantity=body['quantity'],
        price=body['price'],
        category_id=body['category_id'],
        company_id=body['company_id']
    )
    db.session.add(new_product)
    db.session.commit()

    return jsonify(new_product.serialize()), 201

@api.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    one_product = Product.query.filter_by(id=product_id).first()
    db.session.delete(one_product)
    db.session.commit()
    response_body = {
        "msg": "Product eliminado correctamente",
        "product_id": product_id,
        
    }

    return jsonify(response_body), 200

@api.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.filter_by(id=product_id).first()
    body= request.get_json()
    if 'name' in body:
        product.name = body['name']
    if 'description' in body:
        product.description = body['description']
    if 'quantity' in body:
        product.quantity = body['quantity']
    if 'price' in body:
        product.price = body['price']
    if 'category_id' in body:
        product.category_id = body['category_id']
    if 'company_id' in body:
         product.companany_id = body['company_id']
    
    db.session.commit()
 

    return jsonify(product.serialize()), 200
# category endpoints ////////////////////////////////////////////////////

@api.route('/category', methods=['GET'])
def get_category():
    category = Category.query.all()
    serialize_category = list(map(lambda x: x.serialize(), category))
    
    return jsonify(serialize_category), 200

@api.route('/category/<int:category_id>', methods=['GET'])
def get_category_by_id(category_id):
    single_category = Category.query.get(category_id)
    if single_category is None:
        return jsonify({"msg":"Category not found"}), 404
    serialize_one_category = single_category.serialize()

    return jsonify(serialize_one_category), 200

@api.route('/category', methods=['POST'])
def add_categories():
    body= request.get_json()
    new_category = Category(name=body['name'])
    db.session.add(new_category)
    db.session.commit()

    return jsonify({"msg": "Category added successfully!"}), 200

@api.route('/category/<int:category_id>', methods=['PUT'])
def modify_category(category_id):
    category = Category.query.get(category_id)
    body= request.get_json()
    if 'name' in body:
        category.name = body['name']
    db.session.commit()
    
    return jsonify(category.serialize(), {"msg": "Category updated successfully"}), 200

@api.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category_id(category_id):
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({"msg": "Category successfully deleted!"}), 200
    else:
        return jsonify({"msg": "Try again"}), 404

#ENDPOINTS ProductOrders

@api.route('/product-orders', methods=['GET'])
def get_product_orders():
    all_product_orders = ProductOrders.query.all()
    results = list(map(lambda elemento: elemento.serialize() , all_product_orders))

    return jsonify(results), 200


@api.route('/product-orders/<int:product_orders_id>', methods=['GET'])
def get_product_order(product_orders_id):
    one_product_orders = ProductOrders.query.filter_by(id=product_orders_id).first()

    return jsonify(one_product_orders.serialize()), 200


@api.route('/product-orders', methods=['POST'])
def add_product_orders():
    body= request.get_json()
    new_product_orders = ProductOrders(
        product_id=body['product_id'],
        #order_id=body['order_id'],
        quantity=body['quantity'],
        price=body['price'],
    )
    db.session.add(new_product_orders)
    db.session.commit()

    return jsonify(new_product_orders.serialize()), 201

@api.route('/product-orders/<int:product_orders_id>', methods=['DELETE'])
def delete_product_orders(product_orders_id):
    one_product_orders = ProductOrders.query.filter_by(id=product_orders_id).first()
    db.session.delete(one_product_orders)
    db.session.commit()
    response_body = {
        "msg": "Product eliminado correctamente",
        "product_id": product_orders_id,
        
    }

    return jsonify(response_body), 200

@api.route('/product-orders/<int:product_orders_id>', methods=['PUT'])
def update_product_orders(product_orders_id):
    product_orders = ProductOrders.query.filter_by(id=product_orders_id).first()
    body= request.get_json()
    # if 'order_id' in body:
    #     product_orders.order_id = body['order_id']
    if 'product_id' in body:
        product_orders.product_id = body['product_id']
    if 'quantity' in body:
        product_orders.quantity = body['quantity']
    if 'price' in body:
        product_orders.price = body['price']
    
    db.session.commit()
 

    return jsonify(product_orders.serialize()), 200
    
# user endpoints ////////////////////////////////////////////////////

@api.route('/user', methods=['GET'])
def get_users():
    user = User.query.all()
    serialize_user = list(map(lambda x: x.serialize(), user))
    
    return jsonify(serialize_user), 200

@api.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    single_user = User.query.get(user_id)
    if single_user is None:
        return jsonify({"msg":"User not found"}), 404
    serialize_one_user = single_user.serialize()

    return jsonify(serialize_one_user), 200

@api.route('/user', methods=['POST'])
def add_user():
    body= request.get_json()
    new_user = User(
        name=body['name'],
        email=body['email'],
        password=body['password']
        )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User added successfully!"}), 200

@api.route('/user/<int:user_id>', methods=['PUT'])
def modify_user(user_id):
    user = User.query.get(user_id)
    body= request.get_json()
    if 'name' in body:
        user.name = body['name']
    if 'email' in body:
        user.email = body['email']
    if 'password' in body:
        user.password = body['password']
    db.session.commit()
    
    return jsonify(user.serialize(), {"msg": "User updated successfully"}), 200

@api.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user_id(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "User successfully deleted!"}), 200
    else:
        return jsonify({"msg": "Try again"}), 404
    
