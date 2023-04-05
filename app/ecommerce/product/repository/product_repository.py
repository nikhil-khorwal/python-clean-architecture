
import json
import os
from flask import current_app, jsonify, request
from app.core.db.postgres_configuration import CategoryTable, ImageTable
from app.core.methods.core_method import allowed_file, create_file_name, get_file_extension
from app.ecommerce.category.domain.category_domain import CategoryDomain
from app.core.error.response import ResponseFailure, ResponseTypes
from app.core.error.response import ResponseSuccess
from app.core.db.postgres_configuration import PostgresConfiguration, ProductTable
from app.ecommerce.product.domain.product_domain import ProductDomain


class ProductRepository:
    def __init__(self):
        self.session = PostgresConfiguration.get_session()

    def create_product(self, data):
        category = self.session.query(CategoryTable).filter_by(
            id=data["category_id"]
        ).first()
        if category is None:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No product found for this category!"
            )
        images = data.pop("images")
        new_product = ProductTable(**data)
        self.session.add(new_product)
        self.session.commit()

        images_result = []
        
        for i in images:
            if i and allowed_file(i.filename):
                filename = f"{new_product.title}_{create_file_name(i.filename)}"
                i.save(os.path.join(current_app.config["MEDIA_PATH"], filename))
                image_path = current_app.config["MEDIA_PATH"]+"/"+filename
                image = ImageTable(
                        file_name = filename,
                        file_path = image_path,
                        product_id = new_product.id
                )
                self.session.add(image)
                self.session.commit()
                images_result.append(image_path)

        return ResponseSuccess({
            "message": "Data added successfully",
            "data": ProductDomain.from_db(new_product)
        })

    def get_all_products(self):
        res = self.session.query(ProductTable).all()
        all_products_obj = [
            ProductDomain.from_db(i)
            for i in res
        ]
        return ResponseSuccess(
            all_products_obj
        )

    def get_product_by_id(self, id):
        res = self.session.query(ProductTable)\
            .filter(ProductTable.id == id)\
            .first()
        if res is None:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No product found for this id!"
            )
        product_obj = ProductDomain.from_db(res)
        return ResponseSuccess(product_obj)

    def update_product(self, data):
        id = data.pop("id")
        exist_product = self.session.query(ProductTable).filter_by(id=id).first()
        if exist_product is None:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No product found for this id!"
            )
        for key, value in data.items():
            setattr(exist_product, key, value)

        product_obj = ProductDomain.from_db(exist_product)
        self.session.commit()
        return ResponseSuccess({
            "message": "Update product successfully",
            "data": product_obj
        })

    def delete_product(self, id):
        product = self.session.query(ProductTable).filter_by(id=id).first()
        if product is None:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No product found for this id!"
            )
        self.session.delete(product)
        self.session.commit()
        return ResponseSuccess(
            value={
                "message": "delete product successfully"
            })
