from app import create_app
from models.models import db, Skill, SiteContent

app = create_app()

def migrate_skills():
    with app.app_context():
        # Create table if it doesn't exist
        db.create_all()
        
        # Check if skills already exist
        if Skill.query.first():
            print("Skills table already populated.")
            return

        # Initial skills data from user request
        initial_skills = [
            # Backend Development
            {"name": "Python", "category": "Backend Development"},
            {"name": "REST API", "category": "Backend Development"},
            {"name": "Authentication", "category": "Backend Development"},
            {"name": "Authorization", "category": "Backend Development"},
            
            # Frontend Development
            {"name": "HTML", "category": "Frontend Development"},
            {"name": "CSS", "category": "Frontend Development"},
            {"name": "JavaScript", "category": "Frontend Development"},
            {"name": "Bootstrap", "category": "Frontend Development"},
            
            # Database & Analytics
            {"name": "MySQL", "category": "Database & Analytics"},
            {"name": "NumPy", "category": "Database & Analytics"},
            {"name": "Pandas", "category": "Database & Analytics"},
            
            # Security & Deployment
            {"name": "Security", "category": "Security & Deployment"},
            {"name": "Deployment", "category": "Security & Deployment"},
            {"name": "Git & GitHub", "category": "Security & Deployment"},
            
            # Tools & Productivity
            {"name": "SEO", "category": "Tools & Productivity"},
            {"name": "Microsoft Word", "category": "Tools & Productivity"},
        ]
        
        for s in initial_skills:
            skill = Skill(name=s["name"], category=s["category"])
            db.session.add(skill)
            
        db.session.commit()
        print("Successfully migrated skills to new table.")

if __name__ == "__main__":
    migrate_skills()
