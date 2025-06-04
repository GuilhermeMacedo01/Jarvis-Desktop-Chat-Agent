import json
from pathlib import Path

class UserProfile:
    def __init__(self):
        self.name = ''
        self.stack = []
        self.interests = []
        self.profile_path = Path(__file__).parent.parent.parent / 'data' / 'profile.json'
        self.load()
    
    def load(self):
        """Load user profile from JSON file"""
        try:
            if self.profile_path.exists():
                with open(self.profile_path, 'r') as f:
                    data = json.load(f)
                    self.name = data.get('name', '')
                    self.stack = data.get('stack', [])
                    self.interests = data.get('interests', [])
        except Exception as e:
            print(f"Error loading profile: {e}")
    
    def save(self):
        """Save user profile to JSON file"""
        try:
            data = {
                'name': self.name,
                'stack': self.stack,
                'interests': self.interests
            }
            self.profile_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.profile_path, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving profile: {e}")
    
    def update_profile(self, name=None, stack=None, interests=None):
        """Update profile with new information"""
        
        if name is not None:
            self.name = name
        if stack is not None:
            self.stack = stack
        if interests is not None:
            self.interests = interests
        self.save() 