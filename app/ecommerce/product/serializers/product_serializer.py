import json


class ProductSerializer(json.JSONEncoder):
    def default(self, o):
        return {
            "id": o.id,
            "title": o.title,
            "desc": o.desc,
            "price": o.price,
            "stock": o.stock,
            "gst_percentage": o.gst_percentage,
            "discount_percentage": o.discount_percentage,
            "images": [{
                "id":i.id,
                "file_name":i.file_name,
                "file_path":i.file_path
            }
            for i in o.images],
            "category": {
                "id": o.category.id,
                "title": o.category.title,
            }
        }
