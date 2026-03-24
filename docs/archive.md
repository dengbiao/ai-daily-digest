---
layout: default
title: 归档
permalink: /archive/
---

<h2 class="text-2xl font-bold mb-8">📚 历史归档</h2>

{% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}

{% for year in posts_by_year %}
<section class="mb-12">
  <h3 class="text-xl font-semibold mb-6 text-blue-400">{{ year.name }}年</h3>
  
  <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
    {% for post in year.items %}
    <a href="{{ post.url | relative_url }}" class="bg-dark-surface border border-dark-border rounded-lg p-4 hover:border-blue-500/50 transition-all duration-300 hover:-translate-y-1">
      <div class="flex items-center justify-between mb-2">
        <span class="text-2xl font-bold text-blue-400">{{ post.date | date: "%m.%d" }}</span>
        <span class="text-xs text-gray-500 px-2 py-1 bg-dark-bg rounded">{{ post.news_count | default: 0 }} 条</span>
      </div>
      <h4 class="text-gray-200 font-medium line-clamp-2">{{ post.title }}</h4>
    </a>
    {% endfor %}
  </div>
</section>
{% endfor %}

{% if site.posts.size == 0 %}
<div class="text-center py-16 text-gray-500">
  <svg class="w-16 h-16 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
  </svg>
  <p>暂无归档内容</p>
  <p class="text-sm mt-2">日报内容即将上线</p>
</div>
{% endif %}
