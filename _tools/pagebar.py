"""Insert a sticky page bar (title + section shortcuts) under the site nav on every converter page.
Re-runnable: replaces the block between <!-- pagebar:start/end -->.  Usage (from the repo root): python _tools/pagebar.py
"""
import sys, re, glob, os, html

SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS = """<script>
document.addEventListener('DOMContentLoaded', function () {
  var bar = document.getElementById('page-bar'); if (!bar) return;
  var links = [].slice.call(bar.querySelectorAll('.pb-link'));
  var secs = links.map(function (a) { return document.querySelector(a.getAttribute('href')); });
  var head = document.querySelector('.page-header'), box = bar.querySelector('.pb-links');
  function update() {

    var edge = bar.getBoundingClientRect().bottom;
    if (head) bar.classList.toggle('show-title', head.getBoundingClientRect().bottom < edge);
    var cur = -1;
    secs.forEach(function (s, i) { if (s && s.getBoundingClientRect().top <= edge + 40) cur = i; });
    if (window.scrollY > 0 && window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) cur = secs.length - 1;
    links.forEach(function (a, i) { a.classList.toggle('active', i === cur); });
    if (cur < 0) { box.scrollLeft = 0; return; }
    var a = links[cur];  // keep the active shortcut in view on narrow screens
    if (a.offsetLeft < box.scrollLeft || a.offsetLeft + a.offsetWidth > box.scrollLeft + box.clientWidth) box.scrollLeft = a.offsetLeft - 12;
  }
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  window.addEventListener('load', update);
  update();
});
</script>"""

for path in sorted(glob.glob(os.path.join(SITE, '*.html'))):
    name = os.path.basename(path)[:-5]
    if name in ('index', '404'): continue
    s = open(path, encoding='utf-8').read()
    old = re.search(r'<!-- pagebar:start -->.*?<!-- pagebar:end -->\n', s, flags=re.S)
    old_links = re.findall(r'<a class="pb-link" href="(#[^"]+)">(.*?)</a>', old.group(0)) if old else []
    if old: s = s.replace(old.group(0), '')

    eyebrow = re.search(r'<span class="eyebrow">(.*?)</span>', s).group(1)
    emoji = eyebrow.split()[0]
    h1 = re.sub(r'<[^>]+>', '', re.search(r'<h1>(.*?)</h1>', s, re.S).group(1)).strip()

    if name == 'refrigeration':
        jump = re.search(r'\n\s*<nav class="tabs jump[^"]*"[^>]*>(.*?)</nav>\n', s, re.S)
        if jump:
            links = re.findall(r'<a class="tab" href="(#[^"]+)">(.*?)</a>', jump.group(1))
            s = s.replace(jump.group(0), '\n')
        else:  # already converted on an earlier run
            links = old_links
        if len(links) < 6:
            links = [('#capacity', 'Capacity'), ('#pt', 'PT Chart'), ('#shsc', 'Superheat / Subcooling'), ('#efficiency', 'COP · EER'),
                     ('#load', 'Heat Load'), ('#refrigerants', 'Refrigerants')]
        if ('#faq', 'FAQ') not in links: links.append(('#faq', 'FAQ'))
    else:
        # anchor the converter card (first card in <main>)
        if 'id="converter"' not in s:
            main_at = s.index('<main')
            m = re.compile(r'<(div|section) class="card').search(s, main_at)
            s = s[:m.start()] + f'<{m.group(1)} id="converter" class="card' + s[m.end():]
        links = [('#converter', 'Converter'), ('#guide', 'Guide'), ('#tables', 'Tables'), ('#faq', 'FAQ')]
        for href, _ in links: assert f'id="{href[1:]}"' in s, (name, href)

    items = ''.join(f'<a class="pb-link" href="{h}">{t}</a>' for h, t in links)
    block = (f'<!-- pagebar:start -->\n<div class="page-bar" id="page-bar"><div class="pb-inner">'
             f'<span class="pb-title">{emoji} {html.escape(h1)}</span>'
             f'<nav class="pb-links" aria-label="On this page">{items}</nav></div></div>\n{JS}\n<!-- pagebar:end -->\n')
    nav_end = s.index('</nav>') + len('</nav>\n')   # first </nav> = site navigation
    s = s[:nav_end] + block + s[nav_end:]
    open(path, 'w', encoding='utf-8', newline='\n').write(s)
    print(f'{name}: {emoji} {h1} -> {", ".join(t for _, t in links)}')
