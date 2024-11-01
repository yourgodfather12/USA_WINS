import os
import subprocess
import random
import string

# Project root name
root_project_name = "tor_website"  # The root directory for your project

# Main project and app names
project_name = "core"  # Main Django project folder
app_name = "app"  # Custom Django app for the anonymous image board
admin_username = "admin"
admin_email = "admin@example.com"
admin_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

# Function to run shell commands
def run_command(command):
    print(f"Running command: {command}")  # Debugging statement
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")  # Print the error if command fails
        raise subprocess.CalledProcessError(result.returncode, command)
    else:
        print(result.stdout)  # Print command output for success

# Create the main project root directory
def create_project_structure():
    # Create the root project directory if it doesn't exist
    if not os.path.exists(root_project_name):
        os.makedirs(root_project_name)
    os.chdir(root_project_name)

    # Create Django project if it doesn't exist
    if not os.path.exists(project_name):
        run_command(f"django-admin startproject {project_name}")
    print(f"Django project '{project_name}' created successfully.")

    # Create Django app if it doesn't exist
    project_path = os.path.join(os.getcwd(), project_name)
    os.chdir(project_path)
    app_path = os.path.join(project_path, app_name)
    if not os.path.exists(app_path):
        run_command(f"python manage.py startapp {app_name}")
    print(f"Django app '{app_name}' created successfully.")

    # Create the static and templates directories
    os.makedirs(f"{app_path}/static/{app_name}/css", exist_ok=True)
    os.makedirs(f"{app_path}/static/{app_name}/js", exist_ok=True)
    os.makedirs(f"{app_path}/templates/{app_name}", exist_ok=True)

    # Create initial CSS and JS files
    with open(f"{app_path}/static/{app_name}/css/style.css", "w") as file:
        file.write("/* Custom stylesheet */\n")

    with open(f"{app_path}/static/{app_name}/js/script.js", "w") as file:
        file.write("// Custom JavaScript\n")

    # Create initial HTML templates
    create_initial_templates(app_path)

    print(f"Project structure for '{root_project_name}' created successfully.")

def create_initial_templates(app_path):
    templates = {
        "base.html": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Anonymous Image Board</title>
    <link rel="stylesheet" href="{% static 'app/css/style.css' %}">
</head>
<body>
    <header><h1>Anonymous Image Board</h1></header>
    <main>{% block content %}{% endblock %}</main>
    <script src="{% static 'app/js/script.js' %}"></script>
</body>
</html>
""",
        "county.html": "{% extends 'app/base.html' %}\n{% block content %}<h2>County: {{ county.name }}</h2><div id='posts'>{{ posts }}</div>{% endblock %}",
        "new_post.html": """
{% extends 'app/base.html' %}
{% block content %}
<h2>New Post</h2>
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    <textarea name="content" placeholder="Write your post..."></textarea>
    <input type="file" name="image" />
    <button type="submit">Post</button>
</form>
{% endblock %}
""",
        "state.html": "{% extends 'app/base.html' %}\n{% block content %}<h2>State: {{ state.name }}</h2>{% endblock %}",
    }

    for filename, content in templates.items():
        with open(f"{app_path}/templates/{app_name}/{filename}", "w") as file:
            file.write(content)

    print(f"Initial HTML templates for '{app_name}' created successfully.")

def setup_app_structure():
    # Navigate to the app directory to create additional structure
    app_path = os.path.join(os.getcwd(), app_name)

    # Models
    models_content = """
from django.db import models

class State(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.name

class County(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, related_name='counties', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.state.name}"

class Post(models.Model):
    county = models.ForeignKey(County, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post in {self.county.name} at {self.timestamp}"
    """
    with open(f"{app_path}/models.py", "w") as file:
        file.write(models_content)

    # Serializers
    serializers_content = """
from rest_framework import serializers
from .models import State, County, Post

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name', 'abbreviation']

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = ['id', 'name', 'state']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'county', 'content', 'image', 'timestamp']
    """
    with open(f"{app_path}/serializers.py", "w") as file:
        file.write(serializers_content)

    # API Views
    views_content = """
from rest_framework import viewsets
from .models import State, County, Post
from .serializers import StateSerializer, CountySerializer, PostSerializer

class StateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer

class CountyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = County.objects.all()
    serializer_class = CountySerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    """
    with open(f"{app_path}/views.py", "w") as file:
        file.write(views_content)

    # URL Routing for API
    urls_content = """
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'states', views.StateViewSet)
router.register(r'counties', views.CountyViewSet)
router.register(r'posts', views.PostViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
    """
    with open(f"{app_path}/urls.py", "w") as file:
        file.write(urls_content)

    # Link app URLs in the project
    project_urls_path = f"{project_name}/urls.py"
    with open(project_urls_path, "a") as file:
        file.write(f"\nfrom django.urls import include\nurlpatterns += [path('{app_name}/', include('{app_name}.urls'))]\n")

    print(f"App structure for '{app_name}' set up successfully.")

def update_django_settings():
    settings_path = f"{project_name}/settings.py"

    # Ensure `import os` exists in settings
    with open(settings_path, "r+") as file:
        content = file.read()

        # Add import os if it's missing
        if 'import os' not in content:
            content = "import os\n" + content

        # Ensure app is added to INSTALLED_APPS
        if f"'{app_name}'" not in content:
            content = content.replace("INSTALLED_APPS = [", f"INSTALLED_APPS = ['{app_name}', ")

        # Append necessary settings for media, static, and Django REST Framework
        content += f"""
# Media and Static files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, '{app_name}/static')]

# Django REST Framework configuration
INSTALLED_APPS += ['rest_framework']
"""
        file.seek(0)
        file.write(content)
        file.truncate()

    print(f"Django settings for project '{project_name}' updated successfully.")

def run_migrations_and_create_admin():
    run_command("python manage.py makemigrations")
    run_command("python manage.py migrate")

    # Create superuser
    if input("Do you want to create a superuser? (y/n): ").lower() == 'y':
        run_command(f"python manage.py createsuperuser --username {admin_username} --email {admin_email} --noinput")
        os.environ.setdefault("DJANGO_SUPERUSER_PASSWORD", admin_password)
        print(f"Superuser created successfully.\nUsername: {admin_username}\nPassword: {admin_password}")

# Main setup function
def setup_project():
    create_project_structure()
    setup_app_structure()
    update_django_settings()
    run_migrations_and_create_admin()
    print(f"Project setup for '{root_project_name}' complete.")

# Run the setup
if __name__ == "__main__":
    setup_project()
