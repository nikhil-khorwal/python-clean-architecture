from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
    config_file = f"app.application.config.{config_name.capitalize()}Config"
    app.config.from_object(config_file)
    app.app_context().push()

    from app.application.rest import (
        user,
        product,
        category,
        cart,
        order,
        address
    )
    app.register_blueprint(user.blueprint)
    app.register_blueprint(product.blueprint)
    app.register_blueprint(category.blueprint)
    app.register_blueprint(cart.blueprint)
    app.register_blueprint(order.blueprint)
    app.register_blueprint(address.blueprint)
    return app
