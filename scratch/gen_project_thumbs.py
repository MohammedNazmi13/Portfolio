import os
import fitz
from app import create_app
from models.models import Project

def generate_thumbnails():
    app = create_app()
    with app.app_context():
        projects = Project.query.all()
        for project in projects:
            if project.image_url and project.image_url.lower().endswith('.pdf'):
                # Convert URL to path
                rel_path = project.image_url.lstrip('/')
                full_path = os.path.join(app.root_path, rel_path)
                
                if os.path.exists(full_path):
                    thumb_path = full_path + ".png"
                    if not os.path.exists(thumb_path):
                        print(f"Generating thumbnail for {project.title}...")
                        try:
                            doc = fitz.open(full_path)
                            page = doc.load_page(0)
                            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                            pix.save(thumb_path)
                            doc.close()
                            print("Success.")
                        except Exception as e:
                            print(f"Error: {e}")
                    else:
                        print(f"Thumbnail already exists for {project.title}.")
                else:
                    print(f"File not found: {full_path}")

if __name__ == '__main__':
    generate_thumbnails()
