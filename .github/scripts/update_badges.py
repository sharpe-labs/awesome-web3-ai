import os
import re
from github import Github

# Initialize GitHub API client
g = Github(os.getenv('GITHUB_TOKEN'))

# Path to the README file
readme_path = 'README.md'

# List of repositories to update
repos = [
    'covalenthq/ai-agent-sdk',
    'coinbase/agentkit',
    # Add other repositories here
]

# Function to create a custom badge URL
def create_badge(language):
    return f"https://img.shields.io/badge/language-{language}-black?style=flat"

# Read the current README content
with open(readme_path, 'r') as file:
    readme_content = file.read()

# Update the README with new language badges
for repo_name in repos:
    repo = g.get_repo(repo_name)
    languages = repo.get_languages()
    if languages:
        top_language = max(languages, key=languages.get)
        badge_url = create_badge(top_language)
        # Regex to find and replace the existing badge
        readme_content = re.sub(
            rf"!\[Language\]\(https://img\.shields\.io/github/languages/top/{repo_name}[^)]+\)",
            f"![Language]({badge_url})",
            readme_content
        )

# Write the updated README content back to the file
with open(readme_path, 'w') as file:
    file.write(readme_content) 