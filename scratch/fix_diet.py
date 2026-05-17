import glob

for f in glob.glob('frontend/manager/*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        # Remove any existing Diet Plans links so we don't have duplicates
        if '>Diet Plans</a>' in line:
            continue
            
        new_lines.append(line)
        
        # Add Diet Plans into the dropdown right after View Bookings
        if 'href="bookings.html">View Bookings</a>' in line:
            indent = line[:len(line) - len(line.lstrip())]
            new_lines.append(indent + '<a href="diet-plans.html">Diet Plans</a>')
            
    with open(f, 'w', encoding='utf-8') as file:
        file.write('\n'.join(new_lines))
        
print("Updated Diet Plans navigation for all files!")
