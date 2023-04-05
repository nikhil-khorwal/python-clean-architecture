
import json


class OrderSerializer(json.JSONEncoder):
    def default(self, o):
        return {
            "id": o.id,
            "email":o.email,
            "phone":o.phone,
            "user":{
                "id": o.user.id,
                "first_name": o.user.first_name,
                "last_name": o.user.last_name,
                "email": o.user.email,
                "phone": o.user.phone
                },
            "address":{
                "id":o.address.id,
                "house_no":o.address.house_no,
                "street":o.address.street,
                "landmark":o.address.landmark,
                "pincode":o.address.pincode,
                "city":o.address.city,
                "state":o.address.state
            },
            "order_items": [{
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
                for i in o.order_items
            ],
            "price_detail":{
                "id":o.payment.id,
                "price":o.payment.price,
                "discount_price":o.payment.discount_price,
                "sub_total":o.payment.sub_total,
                "gst_price":o.payment.gst_price,
                "net_price":o.payment.net_price
                },
        }