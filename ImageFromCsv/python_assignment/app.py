from flask import Flask
from models import db
from api.routes import api_blueprint
from config import Config

app = Flask(__name__)

# Load the configuration from Config class
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(api_blueprint, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run(debug=True)
