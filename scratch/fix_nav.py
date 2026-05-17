import glob
import re

for f in glob.glob('frontend/manager/*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 1. Remove the "Gym Profile" link from the sidebar nav
    # It looks like: <a href="enroll-gym.html">Gym Profile</a> or <a class="active" href="enroll-gym.html">Gym Profile</a>
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if '>Gym Profile</a>' in line and 'enroll-gym.html' in line:
            # Skip this line (removes it from sidebar)
            continue
        
        # 2. Swap the order in the dropdown and change "Edit Gym Profile" to "Gym Profile"
        if 'href="enroll-gym.html">Edit Gym Profile</a>' in line:
            # Skip it, we will add it after View Bookings
            continue
        
        new_lines.append(line)
        
        if 'href="bookings.html">View Bookings</a>' in line:
            # Add Gym Profile after View Bookings
            indent = line[:len(line) - len(line.lstrip())]
            new_lines.append(indent + '<a href="enroll-gym.html">Gym Profile</a>')
            
    with open(f, 'w', encoding='utf-8') as file:
        file.write('\n'.join(new_lines))
        
print("Fixed navigation!")
