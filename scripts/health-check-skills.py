#!/usr/bin/env python3
import os
import sys

skills_dir = "/home/elogic360/Desktop/little QUANTUM/IntegralMarket/software-factory/skills"
found_skills = []

for root, dirs, files in os.walk(skills_dir):
    if "SKILL.md" in files:
        skill_path = os.path.join(root, "SKILL.md")
        with open(skill_path, "r") as f:
            content = f.read()
            if "name:" in content:
                found_skills.append(os.path.basename(root))

print(f"Verified {len(found_skills)} valid skills in software-factory/skills/")
for s in sorted(found_skills)[:10]:
    print(f" - {s}")
if len(found_skills) > 10:
    print(f" ... and {len(found_skills) - 10} more.")
