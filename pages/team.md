---
layout: page
title: Meet the Zhang Lab
description: The people of the Zhang Statistical Genomics Lab at Penn
extra_css: team.css
wide: true
---

{%- assign T = site.data.team -%}
{%- assign REEL = site.data.photos.reel -%}
{%- assign MEM = site.data.photos.memory -%}
{%- assign CAP = T.captions -%}

{%- comment -%} Photos are addressed by slug so the composition is stable
even if the build script is rerun. {%- endcomment -%}
{%- assign reel_order = "img-0801,img-2383,img-5506,img-4189,img-3879,ee9587ac-027c-4c2c-ae3a-db57c82abcea,img-4186,img-0693" | split: "," -%}
{%- assign life_order = "img-2066,img-5587,img-5921,img-2058" | split: "," -%}
{%- assign lane_order = "img-2365,img-6057,img-3954,img-6701" | split: "," -%}

<div class="team">

<header class="team-hero team-section">
  <h1>Meet the Zhang Lab</h1>
  <p>{{ T.tagline }}</p>
</header>

<!-- ---------------------------------------------------------------- reel -->
<section class="team-section" aria-label="Recent photographs from the lab">
  <div class="team-reel-wrap">
    <div class="team-reel" id="team-reel" tabindex="0" role="region" aria-label="Recent lab photographs, scrollable">
      {%- for slug in reel_order -%}
        {%- assign p = REEL | where: "slug", slug | first -%}
        {%- if p -%}
        {%- assign cap = CAP[slug] -%}
        {%- assign is_first = forloop.first -%}
        <figure>
          {% include labphoto.html photo=p dir="reel" alt=cap
             sizes="(max-width: 600px) 87vw, (max-width: 900px) 62vw, 44vw"
             eager=is_first %}
          <figcaption>{{ CAP[slug] }}{% if p.date %} &middot; {{ p.date | date: "%B %Y" }}{% endif %}</figcaption>
        </figure>
        {%- endif -%}
      {%- endfor -%}
    </div>
    <div class="team-reel-nav" hidden>
      <button type="button" data-reel-prev aria-controls="team-reel" aria-label="Scroll photographs left">&#8592;</button>
      <button type="button" data-reel-next aria-controls="team-reel" aria-label="Scroll photographs right">&#8594;</button>
    </div>
  </div>
</section>

<!-- -------------------------------------------------------------- people -->
<section class="team-section" aria-labelledby="people-h">
  <p class="team-eyebrow">Our People</p>
  <h2 class="team-h2" id="people-h">The group today</h2>

  {%- for g in T.groups -%}
  <div class="team-group">
    <h3>{{ g.name }}</h3>
    <ul class="team-people">
      {%- for m in g.members -%}
      {%- assign portrait = site.data.photos.members | where: "slug", m.photo | first -%}
      <li class="team-person">
        <figure>
          {%- if portrait -%}
            {%- assign palt = m.name | prepend: "Portrait of " -%}
            {% include labphoto.html photo=portrait dir="members" alt=palt
               sizes="(max-width: 380px) 90vw, (max-width: 600px) 44vw, (max-width: 900px) 44vw, 30vw" %}
          {%- else -%}
            {%- assign parts = m.name | split: " " -%}
            <div class="team-initials" aria-hidden="true">{% for w in parts %}{{ w | slice: 0 }}{% endfor %}</div>
          {%- endif -%}
        </figure>
        <p class="name">{% if m.url %}<a href="{{ m.url }}">{{ m.name }}</a>{% else %}{{ m.name }}{% endif %}</p>
        <p class="role">{{ m.role }}</p>
      </li>
      {%- endfor -%}
    </ul>
  </div>

  {%- comment -%} One candid breaks the grid after the PhD students. {%- endcomment -%}
  {%- if forloop.first -%}
    {%- assign brk = REEL | where: "slug", "img-4186" | first -%}
    {%- if brk -%}
    {%- assign brkcap = CAP["img-4186"] -%}
    <div class="team-break">
      <figure>
        {% include labphoto.html photo=brk dir="reel" alt=brkcap sizes="(max-width: 1240px) 100vw, 1240px" %}
        <figcaption>{{ CAP["img-4186"] }}{% if brk.date %} &middot; {{ brk.date | date: "%B %Y" }}{% endif %}</figcaption>
      </figure>
    </div>
    {%- endif -%}
  {%- endif -%}
  {%- endfor -%}
</section>

<!-- ------------------------------------------------------------- lab life -->
<section class="team-section" aria-labelledby="life-h">
  <p class="team-eyebrow">Lab Life</p>
  <h2 class="team-h2" id="life-h">Between the results</h2>
  <p class="team-lede">Group meetings and conference trips, hikes, birthdays and the
  occasional defence celebration.</p>

  <div class="team-life">
    {%- for slug in life_order -%}
      {%- assign p = REEL | where: "slug", slug | first -%}
      {%- if p -%}
      {%- assign cap = CAP[slug] -%}
      <figure class="{% if forloop.first %}tall{% else %}wide{% endif %}">
        {% include labphoto.html photo=p dir="reel" alt=cap
           sizes="(max-width: 600px) 92vw, (max-width: 900px) 46vw, 40vw" %}
      </figure>
      {%- endif -%}
    {%- endfor -%}
  </div>
</section>

<!-- --------------------------------------------------------------- alumni -->
<section class="team-section" aria-labelledby="alumni-h">
  <p class="team-eyebrow">Alumni</p>
  <h2 class="team-h2" id="alumni-h">Where Are They Now?</h2>
  <p class="team-lede">Members of the lab have gone on to faculty positions in statistics
  and biostatistics, to research institutes, to medicine and to industry research.</p>

  <ul class="team-featured">
    {%- for fname in T.featured_alumni -%}
      {%- assign a = T.alumni | where: "name", fname | first -%}
      {%- if a -%}
      <li>
        <p class="name">{{ a.name }}</p>
        <p class="then">{{ a.was }} &middot; left {{ a.year }}</p>
        <p class="now">{{ a.now }}</p>
      </li>
      {%- endif -%}
    {%- endfor -%}
  </ul>

  <!-- ------------------------------------------------------- memory lane -->
  <div class="team-memory">
    <p class="team-eyebrow">Memory Lane</p>
    <h2 class="team-h2">The lab over the years</h2>
    <p class="team-lede">Photographs from the lab's own albums. Dates are taken from the
    photographs themselves; a few carry none.</p>

    <div class="team-lane">
      {%- assign per_row = 3 -%}
      {%- for slug in lane_order -%}
        {%- assign p = MEM | where: "slug", slug | first -%}
        {%- if p -%}
        {%- assign start = forloop.index0 | times: per_row -%}
        {%- assign lanecap = CAP[slug] -%}
        <div class="team-lane-row">
          <div class="team-lane-text">
            <ul class="team-lane-list">
              {%- for a in T.alumni offset: start limit: per_row -%}
              <li>
                <span class="name">{{ a.name }}</span>
                <span class="meta">{{ a.was }}, left {{ a.year }} &mdash; now {{ a.now }}</span>
              </li>
              {%- endfor -%}
            </ul>
          </div>
          <div class="team-lane-photo">
            <figure>
              {% include labphoto.html photo=p dir="memory" alt=lanecap
                 sizes="(max-width: 600px) 92vw, 46vw" %}
              <figcaption>
                <span>{{ CAP[slug] }}</span>
                {%- if p.date %}<span class="year">{{ p.date | date: "%Y" }}</span>{% endif -%}
              </figcaption>
            </figure>
          </div>
        </div>
        {%- endif -%}
      {%- endfor -%}
    </div>
  </div>

  <!-- --------------------------------------------------- full alumni list -->
  <details class="team-all">
    <summary>View all alumni ({{ T.alumni | size }})</summary>
    <table class="team-table">
      <caption>Everyone who has been part of the lab, most recent first.</caption>
      <thead>
        <tr><th scope="col">Name</th><th scope="col">Left</th><th scope="col">Role in lab</th><th scope="col">Position after the lab</th></tr>
      </thead>
      <tbody>
        {%- for a in T.alumni -%}
        <tr>
          <td>{{ a.name }}</td>
          <td class="yr" data-label="Left">{{ a.year }}</td>
          <td data-label="In the lab">{{ a.was }}</td>
          <td data-label="Now">{{ a.now }}</td>
        </tr>
        {%- endfor -%}
      </tbody>
    </table>
  </details>
</section>

<!-- ----------------------------------------------------------------- join -->
<section class="team-section team-join" aria-labelledby="join-h">
  <div>
    <h2 class="team-h2" id="join-h">Interested in Joining Us?</h2>
    <p>We are always looking for motivated students from Statistics, Biology, Computer
    Science, Bioinformatics, or similar fields. If you are interested, please get in
    touch and include your CV and a brief research statement.</p>
    <a class="team-cta" href="mailto:nzh@wharton.upenn.edu">Contact Nancy</a>
  </div>
  <div class="team-join-photo">
    {%- assign jp = REEL | where: "slug", "img-5494" | first -%}
    {%- if jp -%}
      {%- assign jcap = CAP["img-5494"] -%}
      {% include labphoto.html photo=jp dir="reel" alt=jcap sizes="(max-width: 900px) 92vw, 40vw" %}
    {%- endif -%}
  </div>
</section>

</div>

<script>
/* Progressive enhancement only: the reel is a scroll container and works
   without this. Arrows appear solely when JS can drive them. */
(function () {
  var reel = document.getElementById('team-reel');
  if (!reel) return;
  var nav = document.querySelector('.team-reel-nav');
  var prev = document.querySelector('[data-reel-prev]');
  var next = document.querySelector('[data-reel-next]');
  if (!nav || !prev || !next) return;
  nav.hidden = false;

  function step() {
    var first = reel.querySelector('figure');
    return first ? first.getBoundingClientRect().width + 16 : reel.clientWidth * 0.8;
  }
  function sync() {
    var max = reel.scrollWidth - reel.clientWidth - 2;
    prev.disabled = reel.scrollLeft <= 2;
    next.disabled = reel.scrollLeft >= max;
  }
  prev.addEventListener('click', function () { reel.scrollBy({ left: -step(), behavior: 'smooth' }); });
  next.addEventListener('click', function () { reel.scrollBy({ left: step(), behavior: 'smooth' }); });
  reel.addEventListener('scroll', sync, { passive: true });
  window.addEventListener('resize', sync);
  sync();
}());
</script>
