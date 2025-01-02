# Awesome-Awesome

A curated list of awesome repositories on GitHub, sorted by stars.

| Repository | Language | ⭐Stars | Last Updated | Description |
|------------|----------|-------|--------------|-------------|
{% for repo in repositories %}| [{{ repo['full_name'] }}]({{ repo['html_url'] }}) | {{ repo['language'] }} | {{ repo['stars'] }} | {{ repo['updated_at'] }} | {{ repo['description'] }} |
{% endfor %}

> Note: This list is automatically updated weekly. Last update time can be found in the debug info below.
