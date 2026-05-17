import glob

for f in glob.glob('frontend/manager/*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Add cache buster to css
    content = content.replace('href="css/manager.css"', 'href="css/manager.css?v=2"')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
print("Added cache buster!")
