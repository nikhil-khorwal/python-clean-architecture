from app.ecommerce.category.repository.category_repository import (
    CategoryRepository
)
from app.core.error.response import (
    ResponseFailure,
    ResponseTypes
)

repository = CategoryRepository()


def category_get_all_use_case():
    try:
        return repository.get_all_categories()
    except Exception as err:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, err)
