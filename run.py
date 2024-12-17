from app import create_app
from app.extensions import db

app = create_app()

if __name__ == "__main__":
    app.app_context().push()
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)