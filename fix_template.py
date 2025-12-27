
import os

file_path = "templates/content/article_detail.html"

# Correct content
content = """{% extends "base.html" %}

{% block title %}{{ article.meta_title }}{% endblock %}
{% block meta_description %}{{ article.meta_description }}{% endblock %}

{% block content %}

<article class="article-body">

    <!-- HEADER: MEDIUM (Allows header to be slightly wider than text if needed, but keeping it focused for now) -->
    <header class="container-reading article-header">
        <h1>{{ article.title }}</h1>
        <div style="font-size: 20px; color: var(--c-grey-dark); line-height: 1.5; margin-bottom: 24px;">
            {{ article.target_persona|safe }}
        </div>

        <div style="font-size: 13px; color: var(--c-grey-light); text-transform: uppercase; letter-spacing: 0.1em;">
            {% if article.author.linkedin_url %}
            <a href="{{ article.author.linkedin_url }}" target="_blank" rel="noopener noreferrer" style="color: inherit; text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 4px;">{{ article.author.display_name }}</a>
            {% else %}
            {{ article.author.display_name }}
            {% endif %}
             — {{ article.updated_at|date:"F Y" }}
        </div>
    </header>

    <!-- BODY: READING WIDTH (SACRED) -->
    <div class="container-reading">
        <section>
            <h2>The Expectation</h2>
            {{ article.common_expectation|safe }}
        </section>

        <section>
            <h2>The Reality</h2>
            {{ article.actual_reality|safe }}
        </section>

        <section>
            <h2>Salary & Growth Reality</h2>
            <div class="table-scroll">
                {{ article.salary_reality|safe }}
            </div>
        </section>

        <section>
            <h2>Where Most People Get Stuck</h2>
            {{ article.stuck_point|safe }}
        </section>

        <section>
            <h2>Who Should Avoid This Path</h2>
            {{ article.who_should_avoid|safe }}
        </section>

        <div style="margin-top: 5rem;">
            <h3
                style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.15em; border-top: 2px solid var(--c-black); padding-top: 1rem; margin-bottom: 2rem; display: inline-block;">
                Final Verdict
            </h3>

            <div style="font-size: 20px; line-height: 1.5; color: var(--c-black);">
                {{ article.verdict|safe }}
            </div>

            <div style="margin-top: 3rem; font-size: 13px; color: var(--c-grey-light); font-family: monospace;">
                Last Updated: {{ article.updated_at|date:"F Y" }}
            </div>
        </div>
    </div>

</article>

{% endblock %}
"""

with open(file_path, "w", encoding='utf-8') as f:
    f.write(content)

print("Template fixed.")
