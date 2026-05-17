import glob

for f in glob.glob('frontend/manager/*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    lines = content.split('\n')
    new_lines = []
    
    # First, make sure it's not already there to prevent duplicates
    if 'href="enroll-gym.html">Gym Profile</a>' in content:
        print(f"Skipping {f}, already has link.")
        continue
        
    for line in lines:
        new_lines.append(line)
        if 'href="bookings.html"' in line:
            indent = line[:len(line) - len(line.lstrip())]
            
            if 'enroll-gym.html' in f:
                new_lines.append(indent + '<a class="active" href="enroll-gym.html">Gym Profile</a>')
            else:
                new_lines.append(indent + '<a href="enroll-gym.html">Gym Profile</a>')
                
    with open(f, 'w', encoding='utf-8') as file:
        file.write('\n'.join(new_lines))
        
print("Added Nav links!")
