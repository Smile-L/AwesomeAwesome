import requests
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader
import os
import subprocess

# 配置GitHub令牌
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    # 尝试使用GitHub Actions的默认token
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', 'github-token')

headers = {
    'Authorization': f'Bearer {GITHUB_TOKEN}'
}

# GitHub API的基础URL
GITHUB_API_URL = 'https://api.github.com'

# 搜索仓库的URL
SEARCH_REPOS_URL = f"{GITHUB_API_URL}/search/repositories"

# 从环境变量获取搜索参数
query = os.getenv('SEARCH_QUERY')
params = eval(os.getenv('SEARCH_PARAMS'))

response = requests.get(SEARCH_REPOS_URL, headers=headers, params=params)
data = response.json()
repos = data.get('items', [])

# 提取仓库信息
repositories = []
for repo in repos:
    repo_info = {
        'name': repo['name'],
        'full_name': repo['full_name'],
        'html_url': repo['html_url'],
        'description': repo['description'] or '无描述',
        'stars': repo['stargazers_count'],
        'updated_at': repo['updated_at'].split('T')[0],
        'language': repo['language'] or 'Unknown',
        'topics': repo.get('topics', [])
    }
    repositories.append(repo_info)

# 分类
categorized_repos = defaultdict(list)
for repo in repositories:
    language = repo['language']
    categorized_repos[language].append(repo)

# 渲染模板
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('README_template.md')
output = template.render(categorized_repos=categorized_repos)

# 写入README.md
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(output)

# 自动提交和推送
subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'])
subprocess.run(['git', 'config', 'user.email', 'github-actions[bot]@users.noreply.github.com'])
subprocess.run(['git', 'add', 'README.md'])
subprocess.run(['git', 'commit', '-m', 'Auto update README'])
subprocess.run(['git', 'push'])
