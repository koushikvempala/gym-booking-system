import glob
import re

for f in glob.glob('frontend/manager/*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Remove sidebar link
    content = re.sub(r'\s*<a[^>]*href="enroll-gym\.html"[^>]*>Gym Profile</a>\n?', '\n', content)
    
    # Replace emoji
    content = content.replace('👩🏽‍💼', '👤')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
print("Updated all files!")
