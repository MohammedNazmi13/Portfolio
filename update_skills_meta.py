from app import create_app
from models.models import db, Skill

app = create_app()

def update_skills_meta():
    with app.app_context():
        # Create table if it doesn't exist
        db.create_all()
        
        # Skill details mapping
        meta = {
            "Python": ("fas fa-brands fa-python", "High-level programming for backend and data science."),
            "REST API": ("fas fa-network-wired", "Designing and implementing scalable web services."),
            "Authentication": ("fas fa-user-lock", "Secure user login systems using JWT and OAuth."),
            "Authorization": ("fas fa-shield-alt", "Role-based access control and permission management."),
            "HTML": ("fas fa-code", "Structuring web content with semantic HTML5."),
            "CSS": ("fas fa-paint-brush", "Advanced styling with CSS3, Grid, and Flexbox."),
            "JavaScript": ("fas fa-brands fa-js", "Interactive frontend logic and ES6+ features."),
            "Bootstrap": ("fas fa-brands fa-bootstrap", "Responsive design using the Bootstrap framework."),
            "MySQL": ("fas fa-database", "Relational database design and query optimization."),
            "NumPy": ("fas fa-calculator", "Numerical computing and array processing in Python."),
            "Pandas": ("fas fa-table", "Data manipulation and analysis for complex datasets."),
            "Security": ("fas fa-user-shield", "Implementing best practices for web application safety."),
            "Deployment": ("fas fa-cloud-upload-alt", "Hosting and managing production environments."),
            "Git & GitHub": ("fas fa-brands fa-github", "Version control and collaborative development."),
            "SEO": ("fas fa-search", "Optimizing search visibility and performance."),
            "Microsoft Word": ("fas fa-file-word", "Professional documentation and reporting.")
        }
        
        skills = Skill.query.all()
        for s in skills:
            if s.name in meta:
                s.icon_class = meta[s.name][0]
                s.description = meta[s.name][1]
            else:
                s.icon_class = "fas fa-star"
                s.description = "Advanced professional expertise."
                
        db.session.commit()
        print("Successfully updated skills with icons and descriptions.")

if __name__ == "__main__":
    update_skills_meta()
