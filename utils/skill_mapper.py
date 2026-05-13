# Skill Mapping System
# Maps skill names to Font Awesome icons, Devicon identifiers, and categories.

SKILL_MAP = {
    # Backend
    "python": {"name": "Python", "icon": "fab fa-python", "devicon": "python-plain", "category": "Backend Development"},
    "flask": {"name": "Flask", "icon": "fas fa-flask", "devicon": "flask-original", "category": "Backend Development"},
    "django": {"name": "Django", "icon": "fab fa-python", "devicon": "django-plain", "category": "Backend Development"},
    "rest api": {"name": "REST API", "icon": "fas fa-network-wired", "devicon": "api-plain", "category": "Backend Development"},
    "authentication": {"name": "Authentication", "icon": "fas fa-user-lock", "devicon": "auth0-plain", "category": "Backend Development"},
    "authorization": {"name": "Authorization", "icon": "fas fa-shield-alt", "devicon": "guardian-plain", "category": "Backend Development"},
    "fastapi": {"name": "FastAPI", "icon": "fas fa-bolt", "devicon": "fastapi-plain", "category": "Backend Development"},
    "node.js": {"name": "Node.js", "icon": "fab fa-node-js", "devicon": "nodejs-plain", "category": "Backend Development"},
    
    # Frontend
    "html": {"name": "HTML", "icon": "fab fa-html5", "devicon": "html5-plain", "category": "Frontend Development"},
    "css": {"name": "CSS", "icon": "fab fa-css3-alt", "devicon": "css3-plain", "category": "Frontend Development"},
    "javascript": {"name": "JavaScript", "icon": "fab fa-js", "devicon": "javascript-plain", "category": "Frontend Development"},
    "js": {"name": "JavaScript", "icon": "fab fa-js", "devicon": "javascript-plain", "category": "Frontend Development"},
    "bootstrap": {"name": "Bootstrap", "icon": "fab fa-bootstrap", "devicon": "bootstrap-plain", "category": "Frontend Development"},
    "react": {"name": "React", "icon": "fab fa-react", "devicon": "react-original", "category": "Frontend Development"},
    "vue": {"name": "Vue", "icon": "fab fa-vuejs", "devicon": "vuejs-plain", "category": "Frontend Development"},
    
    # Database & Analytics
    "mysql": {"name": "MySQL", "icon": "fas fa-database", "devicon": "mysql-plain", "category": "Database & Analytics"},
    "postgresql": {"name": "PostgreSQL", "icon": "fas fa-database", "devicon": "postgresql-plain", "category": "Database & Analytics"},
    "mongodb": {"name": "MongoDB", "icon": "fas fa-leaf", "devicon": "mongodb-plain", "category": "Database & Analytics"},
    "numpy": {"name": "NumPy", "icon": "fas fa-calculator", "devicon": "numpy-plain", "category": "Database & Analytics"},
    "pandas": {"name": "Pandas", "icon": "fas fa-table", "devicon": "pandas-plain", "category": "Database & Analytics"},
    "r": {"name": "R", "icon": "fas fa-chart-line", "devicon": "r-plain", "category": "Database & Analytics"},
    
    # Security & Deployment
    "security": {"name": "Security", "icon": "fas fa-user-shield", "devicon": "security-plain", "category": "Security & Deployment"},
    "deployment": {"name": "Deployment", "icon": "fas fa-cloud-upload-alt", "devicon": "cloud-plain", "category": "Security & Deployment"},
    "git": {"name": "Git", "icon": "fab fa-git-alt", "devicon": "git-plain", "category": "Security & Deployment"},
    "github": {"name": "GitHub", "icon": "fab fa-github", "devicon": "github-original", "category": "Security & Deployment"},
    "docker": {"name": "Docker", "icon": "fab fa-docker", "devicon": "docker-plain", "category": "Security & Deployment"},
    "aws": {"name": "AWS", "icon": "fab fa-aws", "devicon": "amazonwebservices-plain", "category": "Security & Deployment"},
    "seo": {"name": "SEO", "icon": "fas fa-search", "devicon": "seo-plain", "category": "Security & Deployment"},
}

def get_skill_data(skill_name):
    normalized = skill_name.lower().strip()
    
    # Try exact match
    if normalized in SKILL_MAP:
        return SKILL_MAP[normalized]
        
    # Default fallback
    return {
        "name": skill_name.strip().title(),
        "icon": "fas fa-code",
        "devicon": None,
        "category": "Other Technical Skills"
    }
