import json


class CartSerializer(json.JSONEncoder):
    def default(self, o):
        return {
            "id": o.id,
            "cart_items": [{
                "id": i.id,
                "product": {
                    "id": i.product.id,
                    "title": i.product.title,
                    "desc": i.product.desc,
                    "images": [{
                        "id":i.id,
                        "file_name":i.file_name,
                        "file_path":i.file_path
                    }
                    for i in i.product.images],
                    "price": i.product.price,
                    "gst_percentage": i.product.gst_percentage,
                    "discount_percentage": i.product.discount_percentage,
                    "stock": i.product.stock,
                    "category": {
                        "id": i.product.category.id,
                        "title": i.product.category.title,
                    }
                },
                "quantity": i.quantity
            }
                for i in o.cart_items
            ]
        }


class CartAdminSerializer(json.JSONEncoder):
    def default(self, o):
        return {
            "id": o.id,
            "user": {
                "id": o.user.id,
                "first_name": o.user.first_name,
                "last_name": o.user.last_name,
                "email": o.user.email,
                "phone":o.user.phone,
                "is_admin": o.user.is_admin,
                "is_delete": o.user.is_delete,
                "is_active": o.user.is_active
            },
            "cart_items": [{
                "id": i.id,
                "product": {
                    "id": i.product.id,
                    "title": i.product.title,
                    "desc": i.product.desc,
                    "images": [{
                        "id":i.id,
                        "file_name":i.file_name,
                        "file_path":i.file_path
                    }
                    for i in i.product.images],
                    "price": i.product.price,
                    "stock": i.product.stock,
                    "gst_percentage": i.product.gst_percentage,
                    "discount_percentage": i.product.discount_percentage,
                    "category": {
                        "id": i.product.category.id,
                        "title": i.product.category.title,
                    }
                },
                "quantity": i.quantity
            }
                for i in o.cart_items
            ]
        }