import os
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, send_file, current_app
from models import db
from models.models import Contact, SiteContent, Education, Experience, Certificate, Skill

public_bp = Blueprint('public', __name__)

@public_bp.route('/', methods=['GET'])
def index():
    try:
        site = SiteContent.query.first()
        educations = Education.query.order_by(Education.created_at.desc()).all()
        experiences = Experience.query.order_by(Experience.created_at.desc()).all()
        certificates = Certificate.query.order_by(Certificate.created_at.desc()).all()
        
        # Group skills by category with full objects
        all_skills = Skill.query.all()
    except:
        site = None
        educations = []
        experiences = []
        certificates = []
        all_skills = []

    skills_by_category = {}
    for skill in all_skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
        
    return render_template('index.html', 
                         site=site, 
                         educations=educations, 
                         experiences=experiences, 
                         certificates=certificates,
                         skills_by_category=skills_by_category)

@public_bp.route('/view-resume')
def view_resume():
    try:
        site = SiteContent.query.first()
    except:
        site = None
        
    if not site or not site.resume_url:
        return redirect(url_for('public.index'))
    return render_template('resume_view.html', site=site)

@public_bp.route('/certificate/MohammedNazmi-Portfolio/<path:title_slug>/<int:id>')
def view_certificate(title_slug, id):
    cert = Certificate.query.get_or_404(id)
    return render_template('cert_viewer.html', cert=cert)

@public_bp.route('/contact', methods=['POST'])
def submit_contact():
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('email') or not data.get('message'):
        return jsonify({'error': 'All fields are required.'}), 400
        
    contact = Contact(
        name=data['name'],
        email=data['email'],
        message=data['message']
    )
    db.session.add(contact)
    db.session.commit()
    
    return jsonify({'message': 'Message sent successfully! I will get back to you soon.'}), 201

@public_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
