import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from models import db
from models.models import User, Project, SiteContent, Contact, Education, Experience, Certificate, Skill
from functools import wraps
import fitz # PyMuPDF for PDF thumbnails
import time

admin_bp = Blueprint('admin', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'admin_logged_in' in session:
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['admin_logged_in'] = True
            flash('Logged in successfully.', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('admin.login'))

# --- Default Dashboard (formerly Site Settings) ---
@admin_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    site = SiteContent.query.first()
    if request.method == 'POST':
        site.name = request.form.get('name')
        site.title = request.form.get('title')
        site.tagline = request.form.get('tagline')
        site.email = request.form.get('email')
        site.phone = request.form.get('phone')
        site.address = request.form.get('address')
        site.skills = request.form.get('skills')
        site.github_link = request.form.get('github_link')
        site.linkedin_link = request.form.get('linkedin_link')
        site.whatsapp = request.form.get('whatsapp')
        
        # Handle Resume Upload
        if 'resume_file' in request.files:
            file = request.files['resume_file']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                filename = f"resume_{int(time.time())}_{filename}"
                upload_path = current_app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)
                file.save(os.path.join(upload_path, filename))
                
                if site.resume_url and site.resume_url.startswith('/static/'):
                    old_path = os.path.join(current_app.root_path, site.resume_url.lstrip('/'))
                    if os.path.exists(old_path):
                        try: os.remove(old_path)
                        except: pass
                site.resume_url = f"/static/uploads/certificates/{filename}"
        
        db.session.commit()
        flash('Dashboard settings updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/site_settings.html', site=site)

# --- Projects ---
@admin_bp.route('/projects')
@login_required
def projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/manage_projects.html', projects=projects)

@admin_bp.route('/project/new', methods=['GET', 'POST'])
@login_required
def new_project():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        full_description = request.form.get('full_description')
        tech_stack = request.form.get('tech_stack')
        github_link = request.form.get('github_link')
        demo_link = request.form.get('demo_link')
        
        if description and len(description.split()) > 30:
            flash('Short description must be within 30 words.', 'error')
            return render_template('admin/project_form.html', project=request.form)

        image_url = ''
        if 'project_image' in request.files:
            file = request.files['project_image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                filename = f"project_{int(time.time())}_{filename}"
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'projects')
                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)
                file_full_path = os.path.join(upload_path, filename)
                file.save(file_full_path)
                image_url = f"/static/uploads/projects/{filename}"
                if filename.lower().endswith('.pdf'):
                    try:
                        doc = fitz.open(file_full_path)
                        page = doc.load_page(0)
                        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                        pix.save(os.path.join(upload_path, f"{filename}.png"))
                        doc.close()
                    except Exception as e: print(f"Thumbnail error: {e}")
        
        if not title or not description or not tech_stack:
            flash('Required fields are missing.', 'error')
            return render_template('admin/project_form.html')
            
        project = Project(title=title, description=description, full_description=full_description,
                         tech_stack=tech_stack, github_link=github_link, demo_link=demo_link, image_url=image_url)
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('admin.projects'))
    return render_template('admin/project_form.html', project=None)

@admin_bp.route('/project/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        if description and len(description.split()) > 30:
            flash('Short description must be within 30 words.', 'error')
            return render_template('admin/project_form.html', project=project)
        project.title = title
        project.description = description
        project.full_description = request.form.get('full_description')
        project.tech_stack = request.form.get('tech_stack')
        project.github_link = request.form.get('github_link')
        project.demo_link = request.form.get('demo_link')
        if 'project_image' in request.files:
            file = request.files['project_image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                filename = f"project_{int(time.time())}_{filename}"
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'projects')
                if not os.path.exists(upload_path): os.makedirs(upload_path)
                file_full_path = os.path.join(upload_path, filename)
                file.save(file_full_path)
                if project.image_url and project.image_url.startswith('/static/'):
                    old_path = os.path.join(current_app.root_path, project.image_url.lstrip('/'))
                    if os.path.exists(old_path):
                        try: os.remove(old_path)
                        except: pass
                        if old_path.lower().endswith('.pdf'):
                            try: os.remove(old_path + ".png")
                            except: pass
                project.image_url = f"/static/uploads/projects/{filename}"
                if filename.lower().endswith('.pdf'):
                    try:
                        doc = fitz.open(file_full_path)
                        page = doc.load_page(0)
                        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                        pix.save(os.path.join(upload_path, f"{filename}.png"))
                        doc.close()
                    except Exception as e: print(f"Thumbnail error: {e}")
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.projects'))
    return render_template('admin/project_form.html', project=project)

@admin_bp.route('/project/delete/<int:id>', methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.projects'))

# --- About Section ---
@admin_bp.route('/about', methods=['GET', 'POST'])
@login_required
def about():
    site = SiteContent.query.first()
    if request.method == 'POST':
        site.about_subtitle = request.form.get('about_subtitle')
        site.about_title = request.form.get('about_title')
        site.about_initials = request.form.get('about_initials')
        site.looking_for_1 = request.form.get('looking_for_1')
        site.looking_for_2 = request.form.get('looking_for_2')
        site.stat1_value = request.form.get('stat1_value')
        site.stat1_label = request.form.get('stat1_label')
        site.stat2_value = request.form.get('stat2_value')
        site.stat2_label = request.form.get('stat2_label')
        site.stat3_value = request.form.get('stat3_value')
        site.stat3_label = request.form.get('stat3_label')
        site.section1_title = request.form.get('section1_title')
        site.section1_desc = request.form.get('section1_desc')
        site.section2_title = request.form.get('section2_title')
        site.section2_desc = request.form.get('section2_desc')
        site.section3_title = request.form.get('section3_title')
        site.section3_desc = request.form.get('section3_desc')
        db.session.commit()
        flash('About section updated successfully!', 'success')
        return redirect(url_for('admin.about'))
    return render_template('admin/about_settings.html', site=site)

# --- Education ---
@admin_bp.route('/education')
@login_required
def education():
    educations = Education.query.order_by(Education.created_at.desc()).all()
    return render_template('admin/manage_education.html', educations=educations)

@admin_bp.route('/education/new', methods=['GET', 'POST'])
@login_required
def new_education():
    if request.method == 'POST':
        degree = request.form.get('degree')
        institution = request.form.get('institution')
        date_range = request.form.get('date_range')
        description = request.form.get('description')
        if not degree or not institution or not date_range or not description:
            flash('All fields are required.', 'error')
            return render_template('admin/education_form.html')
        education = Education(degree=degree, institution=institution, date_range=date_range, description=description)
        db.session.add(education)
        db.session.commit()
        flash('Education entry created successfully!', 'success')
        return redirect(url_for('admin.education'))
    return render_template('admin/education_form.html', education=None)

@admin_bp.route('/education/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_education(id):
    education = Education.query.get_or_404(id)
    if request.method == 'POST':
        education.degree = request.form.get('degree')
        education.institution = request.form.get('institution')
        education.date_range = request.form.get('date_range')
        education.description = request.form.get('description')
        db.session.commit()
        flash('Education entry updated successfully!', 'success')
        return redirect(url_for('admin.education'))
    return render_template('admin/education_form.html', education=education)

@admin_bp.route('/education/delete/<int:id>', methods=['POST'])
@login_required
def delete_education(id):
    education = Education.query.get_or_404(id)
    db.session.delete(education)
    db.session.commit()
    flash('Education entry deleted successfully!', 'success')
    return redirect(url_for('admin.education'))

# --- Experience ---
@admin_bp.route('/experience')
@login_required
def experience():
    experiences = Experience.query.order_by(Experience.created_at.desc()).all()
    return render_template('admin/manage_experience.html', experiences=experiences)

@admin_bp.route('/experience/new', methods=['GET', 'POST'])
@login_required
def new_experience():
    if request.method == 'POST':
        job_title = request.form.get('job_title'),
        company = request.form.get('company'),
        date_range = request.form.get('date_range'),
        description = request.form.get('description')
        # Handle tuple issue from comma
        job_title = request.form.get('job_title')
        company = request.form.get('company')
        date_range = request.form.get('date_range')
        
        if not job_title or not company or not date_range or not description:
            flash('All fields are required.', 'error')
            return render_template('admin/experience_form.html')
        experience = Experience(job_title=job_title, company=company, date_range=date_range, description=description)
        db.session.add(experience)
        db.session.commit()
        flash('Experience entry created successfully!', 'success')
        return redirect(url_for('admin.experience'))
    return render_template('admin/experience_form.html', education=None)

@admin_bp.route('/experience/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_experience(id):
    experience = Experience.query.get_or_404(id)
    if request.method == 'POST':
        experience.job_title = request.form.get('job_title')
        experience.company = request.form.get('company')
        experience.date_range = request.form.get('date_range')
        experience.description = request.form.get('description')
        db.session.commit()
        flash('Experience entry updated successfully!', 'success')
        return redirect(url_for('admin.experience'))
    return render_template('admin/experience_form.html', experience=experience)

@admin_bp.route('/experience/delete/<int:id>', methods=['POST'])
@login_required
def delete_experience(id):
    experience = Experience.query.get_or_404(id)
    db.session.delete(experience)
    db.session.commit()
    flash('Experience entry deleted successfully!', 'success')
    return redirect(url_for('admin.experience'))

# --- Certificates ---
@admin_bp.route('/certificates')
@login_required
def certificates():
    certificates = Certificate.query.order_by(Certificate.created_at.desc()).all()
    return render_template('admin/manage_certificates.html', certificates=certificates)

@admin_bp.route('/certificate/new', methods=['GET', 'POST'])
@login_required
def new_certificate():
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        short_description = request.form.get('short_description')
        full_description = request.form.get('full_description')
        skills = request.form.get('skills')
        category = request.form.get('category')
        image_url = ''
        if 'certificate_file' in request.files:
            file = request.files['certificate_file']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                filename = f"cert_{int(time.time())}_{filename}"
                upload_path = current_app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_path): os.makedirs(upload_path)
                file_full_path = os.path.join(upload_path, filename)
                file.save(file_full_path)
                image_url = f"/static/uploads/certificates/{filename}"
                if filename.lower().endswith('.pdf'):
                    try:
                        doc = fitz.open(file_full_path)
                        page = doc.load_page(0)
                        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                        pix.save(os.path.join(upload_path, f"{filename}.png"))
                        doc.close()
                    except Exception as e: print(f"Thumbnail error: {e}")
        if not title or not year or not short_description or not category:
            flash('Required fields are missing.', 'error')
            return render_template('admin/certificate_form.html')
        certificate = Certificate(title=title, issuer='', year=year, short_description=short_description,
                                 full_description=full_description, skills=skills, category=category,
                                 certificate_id='', external_link='', image_url=image_url)
        db.session.add(certificate)
        db.session.commit()
        flash('Certificate created successfully!', 'success')
        return redirect(url_for('admin.certificates'))
    return render_template('admin/certificate_form.html', certificate=None)

@admin_bp.route('/certificate/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_certificate(id):
    certificate = Certificate.query.get_or_404(id)
    if request.method == 'POST':
        certificate.title = request.form.get('title')
        certificate.year = request.form.get('year')
        certificate.short_description = request.form.get('short_description')
        certificate.full_description = request.form.get('full_description')
        certificate.skills = request.form.get('skills')
        certificate.category = request.form.get('category')
        if 'certificate_file' in request.files:
            file = request.files['certificate_file']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                filename = f"cert_{int(time.time())}_{filename}"
                upload_path = current_app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_path): os.makedirs(upload_path)
                file_full_path = os.path.join(upload_path, filename)
                file.save(file_full_path)
                if certificate.image_url and certificate.image_url.startswith('/static/'):
                    old_path = os.path.join(current_app.root_path, certificate.image_url.lstrip('/'))
                    if os.path.exists(old_path):
                        try: os.remove(old_path)
                        except: pass
                        if old_path.lower().endswith('.pdf'):
                            try: os.remove(old_path + ".png")
                            except: pass
                certificate.image_url = f"/static/uploads/certificates/{filename}"
                if filename.lower().endswith('.pdf'):
                    try:
                        doc = fitz.open(file_full_path)
                        page = doc.load_page(0)
                        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                        pix.save(os.path.join(upload_path, f"{filename}.png"))
                        doc.close()
                    except Exception as e: print(f"Thumbnail error: {e}")
        db.session.commit()
        flash('Certificate updated successfully!', 'success')
        return redirect(url_for('admin.certificates'))
    return render_template('admin/certificate_form.html', certificate=certificate)

@admin_bp.route('/certificate/delete/<int:id>', methods=['POST'])
@login_required
def delete_certificate(id):
    certificate = Certificate.query.get_or_404(id)
    db.session.delete(certificate)
    db.session.commit()
    flash('Certificate deleted successfully!', 'success')
    return redirect(url_for('admin.certificates'))

# --- Skills ---
@admin_bp.route('/skills')
@login_required
def skills():
    skills = Skill.query.order_by(Skill.category).all()
    return render_template('admin/skills.html', skills=skills)

@admin_bp.route('/skill/new', methods=['GET', 'POST'])
@login_required
def new_skill():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        icon_class = request.form.get('icon_class')
        description = request.form.get('description')
        image_url = None
        if 'skill_logo' in request.files:
            file = request.files['skill_logo']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                filename = f"skill_{int(time.time())}_{filename}"
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'skills')
                if not os.path.exists(upload_path): os.makedirs(upload_path)
                file.save(os.path.join(upload_path, filename))
                image_url = f"/static/uploads/skills/{filename}"
        if not name or not category:
            flash('Name and Category are required.', 'error')
            return render_template('admin/skill_form.html', skill=None)
        skill = Skill(name=name, category=category, icon_class=icon_class, description=description, image_url=image_url)
        db.session.add(skill)
        db.session.commit()
        flash('Skill added successfully!', 'success')
        return redirect(url_for('admin.skills'))
    return render_template('admin/skill_form.html', skill=None)

@admin_bp.route('/skill/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_skill(id):
    skill = Skill.query.get_or_404(id)
    if request.method == 'POST':
        skill.name = request.form.get('name')
        skill.category = request.form.get('category')
        skill.icon_class = request.form.get('icon_class')
        skill.description = request.form.get('description')
        if 'skill_logo' in request.files:
            file = request.files['skill_logo']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                filename = f"skill_{int(time.time())}_{filename}"
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'skills')
                if not os.path.exists(upload_path): os.makedirs(upload_path)
                file.save(os.path.join(upload_path, filename))
                if skill.image_url and skill.image_url.startswith('/static/'):
                    old_path = os.path.join(current_app.root_path, skill.image_url.lstrip('/'))
                    if os.path.exists(old_path):
                        try: os.remove(old_path)
                        except: pass
                skill.image_url = f"/static/uploads/skills/{filename}"
        db.session.commit()
        flash('Skill updated successfully!', 'success')
        return redirect(url_for('admin.skills'))
    return render_template('admin/skill_form.html', skill=skill)

@admin_bp.route('/skill/delete/<int:id>', methods=['POST'])
@login_required
def delete_skill(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted successfully!', 'success')
    return redirect(url_for('admin.skills'))

# --- Messages ---
@admin_bp.route('/messages')
@login_required
def messages():
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/messages.html', contacts=contacts)

@admin_bp.route('/messages/delete/<int:id>', methods=['POST'])
@login_required
def delete_message(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash('Message deleted successfully!', 'success')
    return redirect(url_for('admin.messages'))
