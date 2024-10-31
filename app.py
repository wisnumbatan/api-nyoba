from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

# Data contoh produk skincare yang lebih lengkap
skincare_products = [
    {"id": "1", "name": "Moisturizer Glow", "description": "Hydrating moisturizer for glowing skin.", "price": 150000},
    {"id": "2", "name": "Acne Spot Treatment", "description": "Effective treatment for acne spots.", "price": 95000},
    {"id": "3", "name": "Sunscreen SPF 50", "description": "Protects skin from harmful UV rays.", "price": 125000},
    {"id": "4", "name": "Brightening Serum", "description": "Brightens and evens out skin tone.", "price": 210000},
    {"id": "5", "name": "Exfoliating Toner", "description": "Removes dead skin cells and impurities.", "price": 85000},
    {"id": "6", "name": "Night Repair Cream", "description": "Deeply nourishes and repairs skin overnight.", "price": 175000},
    {"id": "7", "name": "Anti-Aging Eye Cream", "description": "Reduces wrinkles and fine lines around eyes.", "price": 140000},
    {"id": "8", "name": "Vitamin C Serum", "description": "Boosts collagen and brightens skin.", "price": 195000},
    {"id": "9", "name": "Hydrating Sheet Mask", "description": "Instant hydration for dry skin.", "price": 25000},
    {"id": "10", "name": "Pore Minimizing Essence", "description": "Refines pores and improves skin texture.", "price": 110000}
]

# Detail produk yang lebih lengkap
product_details = {product['id']: {**product, "customerReviews": []} for product in skincare_products}

app = Flask(__name__)
api = Api(app)

class ProductList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(skincare_products),
            "products": skincare_products
        }

class ProductDetail(Resource):
    def get(self, product_id):
        if product_id in product_details:
            return {
                "error": False,
                "message": "success",
                "product": product_details[product_id]
            }
        return {"error": True, "message": "Product not found"}, 404

class ProductSearch(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        result = [p for p in skincare_products if query in p['name'].lower() or query in p['description'].lower()]
        return {
            "error": False,
            "found": len(result),
            "products": result
        }

class AddReview(Resource):
    def post(self):
        data = request.get_json()
        product_id = data.get('id')
        name = data.get('name')
        review = data.get('review')
        
        if product_id in product_details:
            new_review = {
                "name": name,
                "review": review,
                "date": datetime.now().strftime("%d %B %Y")
            }
            product_details[product_id]['customerReviews'].append(new_review)
            return {
                "error": False,
                "message": "Review added successfully",
                "customerReviews": product_details[product_id]['customerReviews']
            }
        return {"error": True, "message": "Product not found"}, 404

class UpdateReview(Resource):
    def put(self):
        data = request.get_json()
        product_id = data.get('id')
        name = data.get('name')
        new_review_text = data.get('review')
        
        if product_id in product_details:
            reviews = product_details[product_id]['customerReviews']
            review_to_update = next((r for r in reviews if r['name'] == name), None)
            if review_to_update:
                review_to_update['review'] = new_review_text
                review_to_update['date'] = datetime.now().strftime("%d %B %Y")
                return {
                    "error": False,
                    "message": "Review updated successfully",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Product not found"}, 404

class DeleteReview(Resource):
    def delete(self):
        data = request.get_json()
        product_id = data.get('id')
        name = data.get('name')
        
        if product_id in product_details:
            reviews = product_details[product_id]['customerReviews']
            review_to_delete = next((r for r in reviews if r['name'] == name), None)
            if review_to_delete:
                reviews.remove(review_to_delete)
                return {
                    "error": False,
                    "message": "Review deleted successfully",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Product not found"}, 404

# Menambahkan resource ke API
api.add_resource(ProductList, '/list')
api.add_resource(ProductDetail, '/detail/<string:product_id>')
api.add_resource(ProductSearch, '/search')
api.add_resource(AddReview, '/review')
api.add_resource(UpdateReview, '/review/update')
api.add_resource(DeleteReview, '/review/delete')

if __name__ == '__main__':
    app.run(debug=True)
