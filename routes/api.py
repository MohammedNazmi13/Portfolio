from flask import Blueprint, jsonify, request
from models import db
from models.models import Project, SiteContent

api_bp = Blueprint('api', __name__)

@api_bp.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return jsonify([p.to_dict() for p in projects]), 200

@api_bp.route('/projects/<int:id>', methods=['GET'])
def get_project(id):
    project = Project.query.get_or_404(id)
    return jsonify(project.to_dict()), 200

@api_bp.route('/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('description') or not data.get('tech_stack'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_project = Project(
        title=data['title'],
        description=data['description'],
        tech_stack=data['tech_stack'],
        github_link=data.get('github_link'),
        demo_link=data.get('demo_link')
    )
    db.session.add(new_project)
    db.session.commit()
    
    return jsonify(new_project.to_dict()), 201

@api_bp.route('/projects/<int:id>', methods=['PUT'])
def update_project(id):
    project = Project.query.get_or_404(id)
    data = request.get_json()
    
    if 'title' in data:
        project.title = data['title']
    if 'description' in data:
        project.description = data['description']
    if 'tech_stack' in data:
        project.tech_stack = data['tech_stack']
    if 'github_link' in data:
        project.github_link = data['github_link']
    if 'demo_link' in data:
        project.demo_link = data['demo_link']
        
    db.session.commit()
    return jsonify(project.to_dict()), 200

@api_bp.route('/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted successfully'}), 200

@api_bp.route('/site-content', methods=['GET'])
def get_site_content():
    content = SiteContent.query.first()
    if not content:
        return jsonify({'error': 'No site content found'}), 404
    return jsonify(content.to_dict()), 200

@api_bp.route('/site-content', methods=['PUT'])
def update_site_content():
    content = SiteContent.query.first()
    if not content:
        return jsonify({'error': 'No site content found'}), 404
        
    data = request.get_json()
    
    if 'name' in data: content.name = data['name']
    if 'title' in data: content.title = data['title']
    if 'tagline' in data: content.tagline = data['tagline']
    if 'about' in data: content.about = data['about']
    if 'email' in data: content.email = data['email']
    if 'phone' in data: content.phone = data['phone']
    if 'skills' in data: content.skills = data['skills']
    if 'github_link' in data: content.github_link = data['github_link']
    if 'linkedin_link' in data: content.linkedin_link = data['linkedin_link']
    if 'whatsapp' in data: content.whatsapp = data['whatsapp']
        
    db.session.commit()
    return jsonify(content.to_dict()), 200
