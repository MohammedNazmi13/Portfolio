from flask import Flask
from config import Config
from models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    with app.app_context():
        # Import routes
        from routes.public import public_bp
        from routes.admin import admin_bp
        from routes.api import api_bp

        # Context Processor for site content (Safe for initial deployment)
        from models.models import SiteContent
        @app.context_processor
        def inject_site():
            try:
                return dict(site=SiteContent.query.first())
            except:
                return dict(site=None)

        # Register blueprints
        app.register_blueprint(public_bp)
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(api_bp, url_prefix='/api')

    # Setup route for first-time initialization
    @app.route('/setup-db')
    def setup_db():
        from models.models import User, SiteContent
        from werkzeug.security import generate_password_hash
        
        # Create tables
        db.create_all()
        
        # Create default admin if doesn't exist
        if not User.query.filter_by(username='admin').first():
            hashed_pw = generate_password_hash('admin123', method='pbkdf2:sha256')
            admin = User(username='admin', password=hashed_pw)
            db.session.add(admin)
            
        # Create default site content if doesn't exist
        if not SiteContent.query.first():
            default_content = SiteContent(
                name="Mohammed Nazmi",
                title="Full Stack Developer",
                tagline="Building scalable systems.",
                about="Welcome to my portfolio.",
                email="hello@example.com",
                phone="+1234567890",
                skills="Python, Flask, JavaScript"
            )
            db.session.add(default_content)
            
        db.session.commit()
        return "Database initialized successfully! Log in at /admin with admin/admin123"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
