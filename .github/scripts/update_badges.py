import os
import re
from github import Github

def get_primary_language(repo):
    try:
        languages = repo.get_languages()
        if languages:
            return max(languages.items(), key=lambda x: x[1])[0]
        return None
    except:
        return None

def update_readme():
    token = os.getenv('GITHUB_TOKEN')
    g = Github(token)
    
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find Developer Tools section
    tools_section = re.search(r'## 🛠️ Developer Tools & Frameworks(.*?)##', content, re.DOTALL)
    if not tools_section:
        return
        
    section_content = tools_section.group(1)
    
    # Find all GitHub repository URLs
    pattern = r'\[.*?\]\((https://github\.com/([^/]+)/([^/)]+))\)'
    matches = re.finditer(pattern, section_content)
    
    updated_content = content
    for match in matches:
        url, owner, repo_name = match.groups()
        try:
            repo = g.get_repo(f"{owner}/{repo_name}")
            language = get_primary_language(repo)
            if language:
                # Create new badge without percentage
                new_badge = f'![{language}](https://img.shields.io/static/v1?label=&message={language}&color=black)'
                
                # Replace old badge with new one
                old_badge_pattern = f'!\[.*?\]\(https://img\.shields\.io/github/languages/top/{owner}/{repo_name}[^)]+\)'
                updated_content = re.sub(old_badge_pattern, new_badge, updated_content)
        except:
            continue
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(updated_content)

if __name__ == '__main__':
    update_readme() 