import os
import re
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Update index.html with correct React build hashes'

    def handle(self, *args, **options):
        build_dir = os.path.join(settings.BASE_DIR, 'static')
        template_path = os.path.join(settings.BASE_DIR, 'templates', 'index.html')
        
        if not os.path.exists(build_dir) or not os.path.isdir(build_dir):
            self.stderr.write(self.style.ERROR("Build directory does not exist"))
            return
        
        js_files = os.listdir(os.path.join(build_dir, 'js'))
        css_files = os.listdir(os.path.join(build_dir, 'css'))

        if not js_files and not css_files:
            self.stderr.write(self.style.ERROR("No JS/CSS files found in build directory"))
            return
        
        with open(template_path, 'r') as template_file:
            content = template_file.read()
        
        js_pattern = re.compile(r'{% static \'js\/.*\.js\' %}')
        css_pattern = re.compile(r'{% static \'css\/.*\.css\' %}')
        
        new_content = js_pattern.sub(f"{{% static 'js/{js_files[0]}' %}}", content)
        new_content = css_pattern.sub(f"{{% static 'css/{css_files[0]}' %}}", new_content)
        
        with open(template_path, 'w') as template_file:
            template_file.write(new_content)
        
        self.stdout.write(self.style.SUCCESS('Successfully updated index.html with latest React build hashes'))