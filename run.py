from app import create_app
from app.config import DevelopmentConfig
from app import db

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
