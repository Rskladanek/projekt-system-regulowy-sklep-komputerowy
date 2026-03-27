from decimal import Decimal
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config


db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    instance_path = Path(app.root_path).parent / "instance"
    instance_path.mkdir(exist_ok=True)

    db.init_app(app)

    register_template_filters(app)

    with app.app_context():
        from . import models  # noqa: F401
        from .models import Product

        db.create_all()

        if Product.query.count() == 0:
            seed_products()

    from .routes import main_bp

    app.register_blueprint(main_bp)
    return app


def register_template_filters(app: Flask) -> None:
    @app.template_filter("money")
    def money_filter(value) -> str:
        amount = Decimal(value or 0).quantize(Decimal("0.01"))
        formatted = f"{amount:,.2f}".replace(",", " ").replace(".", ",")
        return f"{formatted} zł"



def seed_products() -> None:
    from .models import Product

    products = [
        Product(name="Lenovo Legion T5", category="komputer", brand="Lenovo", price=Decimal("5499.00"), active=True),
        Product(name="MSI Creator P100X", category="komputer", brand="MSI", price=Decimal("7299.00"), active=True),
        Product(name="Dell UltraSharp 27", category="monitor", brand="Dell", price=Decimal("1299.00"), active=True),
        Product(name="LG UltraGear 27", category="monitor", brand="LG", price=Decimal("1199.00"), active=True),
        Product(name="Keychron K2", category="klawiatura", brand="Keychron", price=Decimal("399.00"), active=True),
        Product(name="Logitech G Pro X", category="klawiatura", brand="Logitech", price=Decimal("549.00"), active=True),
        Product(name="Logitech G502 X", category="mysz", brand="Logitech", price=Decimal("259.00"), active=True),
        Product(name="Razer DeathAdder V3", category="mysz", brand="Razer", price=Decimal("299.00"), active=True),
        Product(name="HP LaserJet Pro 400", category="drukarka", brand="HP", price=Decimal("899.00"), active=True),
        Product(name="Brother HL-L2442DW", category="drukarka", brand="Brother", price=Decimal("849.00"), active=True),
    ]

    db.session.add_all(products)
    db.session.commit()
