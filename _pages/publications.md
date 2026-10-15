---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
redirect_from:
  - /publications
---

{% assign scholar = site.data.scholar_publications %}
{% assign publications = scholar.publications %}

<style>
  /* Scoped styles: only the Publications page is affected. */
  .scholar-pubs { --pub-blue: #337da3; --pub-ink: #233648; --pub-muted: #627585; --pub-line: #dfe9f0; }
  .scholar-pubs .scholar-intro { margin: .15rem 0 1.25rem; color: var(--pub-muted); line-height: 1.7; font-size: .98rem; }
  .scholar-pubs .scholar-toolbar { display:flex; align-items:center; justify-content:space-between; gap: 1rem; flex-wrap:wrap; margin: 0 0 1.35rem; padding: 1rem 1.1rem; border: 1px solid var(--pub-line); border-radius: 10px; background:#f6fafc; }
  .scholar-pubs .scholar-summary strong { display:block; font-size:1.65rem; line-height:1.15; color:var(--pub-ink); font-weight:750; }
  .scholar-pubs .scholar-summary span { display:block; font-size:.83rem; color:var(--pub-muted); margin-top:.2rem; }
  .scholar-pubs .scholar-source { margin-left:auto; text-align:right; font-size:.78rem; color:var(--pub-muted); }
  .scholar-pubs .scholar-source a { color:var(--pub-blue); font-weight:650; text-decoration:none; }
  .scholar-pubs .scholar-source a:hover { text-decoration:underline; }
  .scholar-pubs .scholar-search { display:block; box-sizing:border-box; width:100%; padding:.78rem .95rem; border:1px solid #cadbe6; border-radius:8px; background:#fff; color:#233648; font:inherit; font-size:.9rem; margin: 0 0 1.35rem; }
  .scholar-pubs .scholar-search:focus { outline:2px solid #a2cddd; outline-offset:2px; }
  .scholar-pubs .scholar-year-section { margin:1.5rem 0 1.9rem; }
  .scholar-pubs .scholar-year-heading { display:flex; align-items:center; gap:.75rem; font-size:1.2rem; font-weight:750; margin:0 0 .6rem; padding:0 0 .55rem; border-bottom:2px solid #c9e3f0; color:var(--pub-ink); }
  .scholar-pubs .scholar-year-heading::after { content:""; height:1px; flex:1; }
  .scholar-pubs .scholar-paper { border-bottom:1px solid var(--pub-line); padding: 1rem .15rem 1.05rem; }
  .scholar-pubs .scholar-paper:last-child { border-bottom:0; }
  .scholar-pubs .scholar-paper-title { display:block; margin:0 0 .33rem; color:#24729b; font-weight:680; line-height:1.45; text-decoration:none; font-size:1.01rem; }
  .scholar-pubs .scholar-paper-title:hover { color:#185576; text-decoration:underline; }
  .scholar-pubs .scholar-authors { font-size:.84rem; color:#536775; line-height:1.6; margin:.15rem 0; }
  .scholar-pubs .scholar-venue { font-size:.83rem; color:#687988; line-height:1.55; margin:.2rem 0 .45rem; font-style:italic; }
  .scholar-pubs .scholar-paper-meta { display:flex; gap:.55rem; align-items:center; flex-wrap:wrap; font-size:.77rem; color:#5d7280; }
  .scholar-pubs .scholar-pill { background:#eaf4f8; color:#2c688a; border:1px solid #d1e8f1; border-radius:999px; padding:.12rem .55rem; }
  .scholar-pubs .scholar-paper-meta a { color:var(--pub-blue); text-decoration:none; }
  .scholar-pubs .scholar-paper-meta a:hover { text-decoration:underline; }
  .scholar-pubs .scholar-empty { background:#f8fafb; border:1px solid var(--pub-line); border-radius:10px; padding:1.5rem; line-height:1.7; color:#4d6170; }
  .scholar-pubs .scholar-footer { border-top:1px solid var(--pub-line); padding-top:1rem; margin-top:1.1rem; font-size:.83rem; color:var(--pub-muted); }
  .scholar-pubs .scholar-no-matches { display:none; padding:1rem; font-size:.9rem; color:var(--pub-muted); }
  @media(max-width:550px) { .scholar-pubs .scholar-toolbar{align-items:flex-start;} .scholar-pubs .scholar-source{margin-left:0;text-align:left;} }
</style>

<div class="scholar-pubs" id="scholar-publications">
  <p class="scholar-intro">Explore my research publications, organized by year and synchronized with my Google Scholar profile.</p>

  {% if publications and publications.size > 0 %}
    <div class="scholar-toolbar">
      <div class="scholar-summary">
        <strong id="scholar-visible-count">{{ publications.size }}</strong>
        <span>Publications listed</span>
      </div>
      <div class="scholar-source">
        <a href="{{ site.author.googlescholar | default: 'https://scholar.google.com/citations?user=DoJQbfoAAAAJ' }}" target="_blank" rel="noopener noreferrer">View Google Scholar ↗</a>
        {% if scholar.updated_at %}<br>Last synchronized: {{ scholar.updated_at | date: '%B %-d, %Y' }}{% endif %}
      </div>
    </div>

    <label for="scholar-search-input" class="visually-hidden">Search publications</label>
    <input class="scholar-search" id="scholar-search-input" type="search" placeholder="Search publications by title, author, or journal…" aria-label="Search publications" autocomplete="off">

    {% assign current_year = '' %}
    {% for pub in publications %}
      {% unless pub.year == current_year %}
        {% unless forloop.first %}</section>{% endunless %}
        {% assign current_year = pub.year %}
        <section class="scholar-year-section">
          <h2 class="scholar-year-heading">{{ pub.year | escape }}</h2>
      {% endunless %}
      <article class="scholar-paper">
        <a class="scholar-paper-title" href="{{ pub.url | escape }}" target="_blank" rel="noopener noreferrer">{{ pub.title | escape }}</a>
        {% if pub.authors != '' %}<p class="scholar-authors">{{ pub.authors | escape }}</p>{% endif %}
        {% if pub.venue != '' %}<p class="scholar-venue">{{ pub.venue | escape }}</p>{% endif %}
        <div class="scholar-paper-meta">
          <span class="scholar-pill">{{ pub.citations | default: 0 }} citation{% unless pub.citations == 1 %}s{% endunless %}</span>
          <a href="{{ pub.url | escape }}" target="_blank" rel="noopener noreferrer">Google Scholar ↗</a>
          {% if pub.cited_by_url != '' and pub.citations > 0 %}
            <span aria-hidden="true">·</span><a href="{{ pub.cited_by_url | escape }}" target="_blank" rel="noopener noreferrer">Cited by</a>
          {% endif %}
        </div>
      </article>
      {% if forloop.last %}</section>{% endif %}
    {% endfor %}
    <p id="scholar-no-matches" class="scholar-no-matches">No publications match your search.</p>
  {% else %}
    <div class="scholar-empty">
      Publication data has not been synchronized yet. Once the Google Scholar update workflow runs successfully, your publications will appear here automatically.
      <p><a href="{{ site.author.googlescholar | default: 'https://scholar.google.com/citations?user=DoJQbfoAAAAJ' }}" target="_blank" rel="noopener noreferrer">Browse publications on Google Scholar ↗</a></p>
    </div>
  {% endif %}

  <p class="scholar-footer">Source: Google Scholar. Citation counts reflect the latest successful synchronization and may differ from other indexing services.</p>
</div>

<script>
(function () {
  var input = document.getElementById('scholar-search-input');
  if (!input) return;
  var papers = Array.prototype.slice.call(document.querySelectorAll('#scholar-publications .scholar-paper'));
  var groups = Array.prototype.slice.call(document.querySelectorAll('#scholar-publications .scholar-year-section'));
  var count = document.getElementById('scholar-visible-count');
  var empty = document.getElementById('scholar-no-matches');
  input.addEventListener('input', function () {
    var q = input.value.trim().toLocaleLowerCase();
    var visibleCount = 0;
    papers.forEach(function (paper) {
      var visible = !q || paper.textContent.toLocaleLowerCase().indexOf(q) !== -1;
      paper.hidden = !visible;
      if (visible) visibleCount++;
    });
    groups.forEach(function (group) {
      group.hidden = !group.querySelector('.scholar-paper:not([hidden])');
    });
    if (count) count.textContent = String(visibleCount);
    if (empty) empty.style.display = visibleCount ? 'none' : 'block';
  });
})();
</script>
