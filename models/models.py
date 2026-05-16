from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) # Hashed password

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    full_description = db.Column(db.Text, nullable=True)
    tech_stack = db.Column(db.String(255), nullable=False)
    github_link = db.Column(db.String(255), nullable=True)
    demo_link = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'full_description': self.full_description,
            'tech_stack': self.tech_stack,
            'github_link': self.github_link,
            'demo_link': self.demo_link,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SiteContent(db.Model):
    __tablename__ = 'site_content'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    tagline = db.Column(db.Text, nullable=False)
    about = db.Column(db.Text, nullable=False)
    about_title = db.Column(db.String(200), nullable=True)
    about_subtitle = db.Column(db.String(100), nullable=True)
    about_initials = db.Column(db.String(10), nullable=True)
    looking_for_1 = db.Column(db.String(100), nullable=True)
    looking_for_2 = db.Column(db.String(100), nullable=True)
    stat1_value = db.Column(db.String(50), nullable=True)
    stat1_label = db.Column(db.String(50), nullable=True)
    stat2_value = db.Column(db.String(50), nullable=True)
    stat2_label = db.Column(db.String(50), nullable=True)
    stat3_value = db.Column(db.String(50), nullable=True)
    stat3_label = db.Column(db.String(50), nullable=True)
    section1_title = db.Column(db.String(100), nullable=True)
    section1_desc = db.Column(db.Text, nullable=True)
    section2_title = db.Column(db.String(100), nullable=True)
    section2_desc = db.Column(db.Text, nullable=True)
    section3_title = db.Column(db.String(100), nullable=True)
    section3_desc = db.Column(db.Text, nullable=True)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    skills = db.Column(db.Text, nullable=False) # Comma-separated
    github_link = db.Column(db.String(255), nullable=True)
    linkedin_link = db.Column(db.String(255), nullable=True)
    whatsapp = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    resume_url = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'tagline': self.tagline,
            'about': self.about,
            'about_title': self.about_title,
            'about_subtitle': self.about_subtitle,
            'about_initials': self.about_initials,
            'looking_for_1': self.looking_for_1,
            'looking_for_2': self.looking_for_2,
            'stat1_value': self.stat1_value,
            'stat1_label': self.stat1_label,
            'stat2_value': self.stat2_value,
            'stat2_label': self.stat2_label,
            'stat3_value': self.stat3_value,
            'stat3_label': self.stat3_label,
            'section1_title': self.section1_title,
            'section1_desc': self.section1_desc,
            'section2_title': self.section2_title,
            'section2_desc': self.section2_desc,
            'section3_title': self.section3_title,
            'section3_desc': self.section3_desc,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'resume_url': self.resume_url,
            'skills': self.skills,
            'github_link': self.github_link,
            'linkedin_link': self.linkedin_link,
            'whatsapp': self.whatsapp,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Education(db.Model):
    __tablename__ = 'educations'
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(150), nullable=False)
    institution = db.Column(db.String(150), nullable=False)
    date_range = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'degree': self.degree,
            'institution': self.institution,
            'date_range': self.date_range,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Experience(db.Model):
    __tablename__ = 'experiences'
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    date_range = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'job_title': self.job_title,
            'company': self.company,
            'date_range': self.date_range,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Certificate(db.Model):
    __tablename__ = 'certificates'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    issuer = db.Column(db.String(150), nullable=True)
    year = db.Column(db.String(50), nullable=False)
    short_description = db.Column(db.String(255), nullable=False)
    full_description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.String(255), nullable=True) # Comma-separated
    category = db.Column(db.String(100), nullable=False)
    certificate_id = db.Column(db.String(100), nullable=True)
    external_link = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'issuer': self.issuer,
            'year': self.year,
            'short_description': self.short_description,
            'full_description': self.full_description,
            'skills': self.skills,
            'category': self.category,
            'certificate_id': self.certificate_id,
            'external_link': self.external_link,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    icon_class = db.Column(db.String(100), nullable=True)
    devicon_name = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'icon_class': self.icon_class,
            'devicon_name': self.devicon_name,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
