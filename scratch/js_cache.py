import glob

for f in glob.glob('frontend/manager/*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Add cache buster to all JS files to force the browser to load the new JS!
    content = content.replace('.js"', '.js?v=3"').replace('.js?v=2?v=3"', '.js?v=3"').replace('.js?v=2"', '.js?v=3"')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
        
print("JS Cache buster applied!")
