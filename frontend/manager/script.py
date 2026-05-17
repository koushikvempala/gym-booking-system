import os
import re

directory = r'c:\Users\keert\Desktop\gym-booking-system\frontend\manager'
files = [
    'bookings.html', 'buy-subscription.html', 'dashboard.html', 'diet-plans.html', 'enroll-gym.html',
    'manage-equipment.html', 'manage-plans.html', 'manage-slots.html', 'manage-trainers.html'
]

for filename in files:
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove any existing Buy Subscription links to prevent duplicates
        content = re.sub(r'<a[^>]*href=[\"\'\']bookings\.html[\"\'\'][^>]*>\s*Buy Subscription\s*</a>\s*', '', content)
        content = re.sub(r'<a[^>]*href=[\"\'\']buy-subscription\.html[\"\'\'][^>]*>\s*Buy Subscription\s*</a>\s*', '', content)
        
        # Inject it accurately after Diet Plans
        content = re.sub(
            r'(<a href=[\"\']diet-plans\.html[\"\']>Diet Plans</a>)',
            r'\1\n            <a href="buy-subscription.html">Buy Subscription</a>',
            content
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
