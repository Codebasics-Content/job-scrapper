"""Remove all duplicate skills from skills_reference_2025.json."""
import json
from collections import defaultdict

# Load the JSON file
with open('skills_reference_2025.json', 'r') as f:
    data = json.load(f)

# Track all skills and their locations
skill_tracker = defaultdict(list)
total_before = 0

# Find all duplicates
for category, skills_list in data['skills'].items():
    for idx, skill in enumerate(skills_list):
        total_before += 1
        skill_name = skill['name']
        skill_tracker[skill_name].append((category, idx))

# Remove duplicates (keep first occurrence)
duplicates_removed = []
for skill_name, locations in skill_tracker.items():
    if len(locations) > 1:
        print(f"\n{skill_name}: {len(locations)} occurrences")
        # Keep first, remove rest
        for i, (category, idx) in enumerate(locations):
            print(f"  {i+1}. {category}")
            if i > 0:  # Remove duplicates
                duplicates_removed.append((category, skill_name, idx))

# Remove duplicates in reverse order to maintain indices
for category in data['skills'].keys():
    skills_to_remove = [(idx, name) for cat, name, idx in duplicates_removed if cat == category]
    skills_to_remove.sort(reverse=True)  # Remove from end to start
    
    for idx, skill_name in skills_to_remove:
        data['skills'][category].pop(idx)
        print(f"✓ Removed duplicate '{skill_name}' from {category}")

# Save cleaned JSON
with open('skills_reference_2025.json', 'w') as f:
    json.dump(data, f, indent=2)

total_after = sum(len(skills) for skills in data['skills'].values())
print(f"\n{'='*70}")
print(f"CLEANUP COMPLETE")
print(f"{'='*70}")
print(f"Total skills before: {total_before}")
print(f"Total skills after: {total_after}")
print(f"Duplicates removed: {total_before - total_after}")
