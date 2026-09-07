---
layout: page
title: Publications &amp; Software
description: Publications and software from the Zhang Statistical Genomics Lab
---

<style>
/* ---- filter bar ---- */
.pubfilter { margin: 0 0 22px 0; }
.pubfilter .grp { margin-bottom: 9px; }
.pubfilter .grplab {
  display: block; font-size: 10px; letter-spacing: .09em; text-transform: uppercase;
  color: #999; margin-bottom: 5px; }
.tg {
  display: inline-block; cursor: pointer; user-select: none;
  font-size: 11px; line-height: 1.5; padding: 2px 7px; margin: 0 4px 4px 0;
  border-radius: 3px; white-space: nowrap; }
.tg-m { color: #000; border: 1px solid transparent; }
.tg-b { background: none; font-weight: bold; border: 1px solid transparent; }
.pubfilter .tg { opacity: .95; }
.pubfilter .tg:hover { opacity: 1; box-shadow: 0 0 0 1px rgba(0,0,0,.18); }
.pubfilter .tg.on { box-shadow: 0 0 0 2px #444; opacity: 1; }
.pubstatus { font-size: 11px; color: #999; margin-top: 6px; }
.pubstatus a { cursor: pointer; }
.publegend { font-size: 11px; color: #999; margin: 0 0 18px 0; }
.publegend strong { color: #555; }
.publegend .mk { color: #555; font-weight: bold; }

/* ---- entries ---- */
.pubyear {
  font-size: 13px; font-weight: bold; color: #666; letter-spacing: .06em;
  border-bottom: 1px solid #e2e2e2; padding-bottom: 3px; margin: 26px 0 12px 0; }
.pub { margin: 0 0 16px 0; line-height: 1.45; }
.pub .t { font-weight: bold; }
.pub .a { color: #444; font-size: 12px; }
.pub .v { color: #333; }
.pub .v em { font-style: normal; font-weight: bold; }
.pub-preprint .v, .pub-review .v { color: #999; font-size: 12px; }
.pub-preprint .v em, .pub-review .v em { font-weight: normal; font-style: italic; }
.pub .lnk { font-size: 11px; margin-top: 2px; }
.pub .lnk a { color: #08c; text-decoration: none; }
.pub .lnk a:hover { text-decoration: underline; }
.pub .lnk .sep { color: #ccc; padding: 0 5px; }
.pub .tags { margin-top: 4px; }
.pub .tags .tg { cursor: pointer; }
.pub .tags .tg:hover { box-shadow: 0 0 0 1px rgba(0,0,0,.25); }
.pub.hide, .pubyear.hide, .pubsec.hide { display: none; }
.pubnote { font-size: 12px; color: #777; margin-top: 30px; }
{% for t in site.data.pubtags.method %}
.tg-{{ t.key }} { background: {{ t.fill }}; border-color: {{ t.edge }}; }
{% endfor %}
{% for t in site.data.pubtags.bio %}
.tg-{{ t.key }} { color: {{ t.color }}; }
{% endfor %}
</style>

<div class="pubfilter">
  <div class="grp">
    <span class="grplab">Methodology</span>
    {% for t in site.data.pubtags.method %}<span class="tg tg-m tg-{{ t.key }}" data-g="m" data-k="{{ t.key }}">{{ t.label }}</span>{% endfor %}
  </div>
  <div class="grp">
    <span class="grplab">Biology</span>
    {% for t in site.data.pubtags.bio %}<span class="tg tg-b tg-{{ t.key }}" data-g="b" data-k="{{ t.key }}">{{ t.label }}</span>{% endfor %}
  </div>
  <div class="pubstatus"><span id="pubcount"></span><span id="pubclear"></span></div>
</div>

<div class="publegend">
  Lab members in <strong>bold</strong>.
  <span class="mk">&dagger;</span> equal contribution.
  <span class="mk">*</span> corresponding author.
</div>

{% assign pending = site.data.publications | where_exp: "p", "p.status != 'published'" %}
{% assign published = site.data.publications | where_exp: "p", "p.status == 'published'" %}

{% if pending.size > 0 %}
<div class="pubsec">
<div class="pubyear">In Review and Preprints</div>
{% for p in pending %}{% include pubentry.html p=p %}{% endfor %}
</div>
{% endif %}

{% assign years = published | group_by: "year" %}
{% for y in years %}
<div class="pubsec">
<div class="pubyear">{{ y.name }}</div>
{% for p in y.items %}{% include pubentry.html p=p %}{% endfor %}
</div>
{% endfor %}

<div class="pubnote">
For the complete list including work before 2011, see
<a href="https://scholar.google.com/citations?user=6EErockAAAAJ&amp;hl=en">Google Scholar</a>.
</div>

<script>
(function () {
  var sel = { m: {}, b: {} },
      pubs = [].slice.call(document.querySelectorAll('.pub')),
      secs = [].slice.call(document.querySelectorAll('.pubsec')),
      chips = [].slice.call(document.querySelectorAll('.pubfilter .tg')),
      countEl = document.getElementById('pubcount'),
      clearEl = document.getElementById('pubclear');

  function keys(g) { return Object.keys(sel[g]); }

  // A paper is shown when it carries at least one selected tag from every
  // group that has a selection: OR within a group, AND across the two groups.
  function matches(el) {
    var g, ks, i, has, list;
    for (g in sel) {
      ks = keys(g);
      if (!ks.length) continue;
      list = (el.getAttribute(g === 'm' ? 'data-m' : 'data-b') || '').split(' ');
      has = false;
      for (i = 0; i < ks.length; i++) {
        if (list.indexOf(ks[i]) !== -1) { has = true; break; }
      }
      if (!has) return false;
    }
    return true;
  }

  function apply() {
    var shown = 0;
    pubs.forEach(function (el) {
      var ok = matches(el);
      el.classList.toggle('hide', !ok);
      if (ok) shown++;
    });
    secs.forEach(function (s) {
      s.classList.toggle('hide', !s.querySelector('.pub:not(.hide)'));
    });
    var active = keys('m').length + keys('b').length;
    countEl.textContent = active ? 'Showing ' + shown + ' publications' : '';
    clearEl.innerHTML = active
      ? ' &middot; <a id="pubclearlink">clear filters</a>' : '';
    var c = document.getElementById('pubclearlink');
    if (c) c.onclick = function () {
      sel = { m: {}, b: {} };
      chips.forEach(function (x) { x.classList.remove('on'); });
      apply();
    };
  }

  function toggle(g, k) {
    if (sel[g][k]) delete sel[g][k]; else sel[g][k] = 1;
    chips.forEach(function (x) {
      x.classList.toggle('on', !!sel[x.getAttribute('data-g')][x.getAttribute('data-k')]);
    });
    apply();
  }

  chips.forEach(function (x) {
    x.onclick = function () { toggle(x.getAttribute('data-g'), x.getAttribute('data-k')); };
  });

  // Tags printed under a paper are clickable too.
  document.querySelectorAll('.pub .tags .tg').forEach(function (x) {
    x.onclick = function () {
      toggle(x.getAttribute('data-g'), x.getAttribute('data-k'));
      var bar = document.querySelector('.pubfilter');
      if (bar.getBoundingClientRect().top < 0) bar.scrollIntoView();
    };
  });

  apply();
}());
</script>
