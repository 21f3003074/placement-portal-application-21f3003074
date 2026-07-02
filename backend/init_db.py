from app import app
from controllers import db
from models import User

with app.app_context():

    admin = User.query.filter_by(
        email="21f3003074@ds.study.iitm.ac.in"
    ).first()

    if not admin:

        admin = User(
            name="Admin",
            email="21f3003074@ds.study.iitm.ac.in",
            password="admin123",
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin Created Successfully")

    else:
        print("Admin Already Exists")