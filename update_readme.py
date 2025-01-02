import requests
import time
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

# 获取多页结果
repositories = []
page = 1
while True:
    params['page'] = page
    response = requests.get(SEARCH_REPOS_URL, headers=headers, params=params)
    data = response.json()
    
    if not data.get('items'):
        break
        
    repos = data.get('items', [])
    if not repos:
        break
        
    print(f"Fetching page {page}, got {len(repos)} repositories")
    
    for repo in repos:
        repo_info = {
            'name': repo['name'],
            'full_name': repo['full_name'],
            'html_url': repo['html_url'],
            'description': (repo['description'] or 'No description').replace('\n', ' ').replace('|', '\\|').replace('\r', ''),
            'stars': repo['stargazers_count'],
            'updated_at': repo['updated_at'].split('T')[0],
            'language': repo['language'] or 'Unknown',
            'topics': repo.get('topics', [])
        }
        repositories.append(repo_info)
    
    # GitHub API有速率限制，添加延时
    time.sleep(2)
    
    if page >= 30:
        break
    
    page += 1

print(f"Total repositories fetched: {len(repositories)}")

# 按star数排序
repositories.sort(key=lambda x: x['stars'], reverse=True)

# 渲染模板
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('README_template.md')
output = template.render(repositories=repositories)

# 添加调试信息
# debug_info = f"""
# ## Debug Info
# - GITHUB_TOKEN: {'设置' if GITHUB_TOKEN else '未设置'}
# - Search Query: {query}
# - Search Params: {params}
# - API Response Status: {response.status_code}
# """

# 写入README.md
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(output) #+ "\n\n" + debug_info)

# 自动提交和推送
subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'])
subprocess.run(['git', 'config', 'user.email', 'github-actions[bot]@users.noreply.github.com'])
subprocess.run(['git', 'add', 'README.md'])
subprocess.run(['git', 'commit', '-m', 'Auto update README'])
subprocess.run(['git', 'push'])
