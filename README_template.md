# Awesome-Awesome

收集GitHub上标题包含"awesome"的高星项目，按主要语言分类。

{% for language, repos in categorized_repos.items() %}
## {{ language }}

{% for repo in repos %}
- [{{ repo['full_name'] }}]({{ repo['html_url'] }})  
  ⭐ {{ repo['stars'] }} | 最后更新：{{ repo['updated_at'] }}  
  {{ repo['description'] }}
{% endfor %}

{% endfor %}
