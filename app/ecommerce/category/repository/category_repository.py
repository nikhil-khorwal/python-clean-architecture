from app.core.error.response import ResponseFailure, ResponseTypes
from app.core.error.response import ResponseSuccess
from app.core.db.postgres_configuration import PostgresConfiguration, CategoryTable
from app.ecommerce.category.domain.category_domain import CategoryDomain


class CategoryRepository:
    def __init__(self):
        self.session = PostgresConfiguration.get_session()

    def create_category(self, data):
        new_category = CategoryTable(
            title=data["title"],
        )
        self.session.add(new_category)
        self.session.commit()
        return ResponseSuccess({
            "message": "Data added successfully",
            "data": CategoryDomain.from_db(new_category)
        })

    def get_all_categories(self):
        all_categories = self.session.query(CategoryTable).all()
        all_categories_obj = [
            CategoryDomain.from_db(i)
            for i in all_categories
        ]
        return ResponseSuccess(
            all_categories_obj
        )

    def get_category_by_id(self, id):
        category = self.session.query(CategoryTable).filter_by(id=id).first()
        if category is None:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No category found for this id!"
            )
        category_obj = CategoryDomain.from_db(category)
        return ResponseSuccess(category_obj)

    def update_category(self, data):
        id = data.pop("id")
        exist_category = self.session.query(
            CategoryTable).filter_by(id=id).first()
        if exist_category is None:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No category found for this id!"
            )
        for key, value in data.items():
            setattr(exist_category, key, value)

        category_obj = CategoryDomain.from_db(exist_category)

        self.session.commit()
        return ResponseSuccess({
            "message": "Update category successfully",
            "data": category_obj
        })

    def delete_category(self, id):
        category = self.session.query(CategoryTable).filter_by(id=id).first()
        if category is None:
            return ResponseFailure(
                type_=ResponseTypes.BADREQUEST_ERROR,
                message="No category found for this id!"
            )
        self.session.delete(category)
        self.session.commit()

        return ResponseSuccess(
            value={
                "message": "delete category successfully"
            })
