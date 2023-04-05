import json


class CategorySerializer(json.JSONEncoder):
    def default(self, o):
        return {
            "id": o.id,
            "title": o.title
        }
