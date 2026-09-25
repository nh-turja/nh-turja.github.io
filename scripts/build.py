#!/usr/bin/env python3
"""Build the portfolio with Python's standard library: python3 scripts/build.py."""
from html import escape
import json
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]
BASE = Template((ROOT / 'templates/base.html').read_text())

def load(name):
    return json.loads((ROOT / 'content' / f'{name}.json').read_text())

P = load('profile')
PUBS = sorted(load('publications'), key=lambda p: p['year'], reverse=True)
PROJECTS = load('projects')
UPDATES = sorted(load('updates'), key=lambda u: u['date'], reverse=True)
CV = load('cv')
NAV = [('Research', 'research.html'), ('Publications', 'publications.html'),
       ('Projects', 'projects.html'), ('CV', 'cv.html'), ('Contact', 'contact.html')]

def e(value):
    return escape(str(value), quote=True)

def anchor(label, url, attrs=''):
    if not (url.startswith(('https://', 'mailto:', '#')) or ':' not in url):
        raise ValueError(f'Unsupported link: {url}')
    return f'<a href="{e(url)}"{attrs}>{e(label)}</a>'

def links(items, label=None):
    aria = f' aria-label="{e(label)}"' if label else ''
    return f'<div class="link-row"{aria}>' + ''.join(anchor(x['label'], x['url']) for x in items) + '</div>'

def page(filename, title, description, content):
    nav = ''.join(anchor(label, url, ' aria-current="page"' if url == filename else '') for label, url in NAV)
    html = BASE.substitute(title=e(f'{title} · {P["name"]}' if filename != 'index.html' else P['name']),
                           description=e(description), navigation=nav, content=content,
                           socials=links(P['socials']), updated=e(P['updated']), tagline=e(P['tagline']))
    (ROOT / filename).write_text(html)
    print(f'Built {filename}')

def heading(kicker, title, description, extra=''):
    return f'<header class="page-head"><p class="eyebrow">{e(kicker)}</p><h1>{e(title)}</h1><p class="lead">{e(description)}</p>{extra}</header>'

def section_heading(title, label, url):
    return f'<div class="section-heading"><h2>{e(title)}</h2>{anchor(label + " →", url)}</div>'

def bibtex(p):
    kind = {'Conference paper': 'inproceedings', 'Journal article': 'article', 'Master’s thesis': 'mastersthesis'}.get(p['type'], 'techreport')
    fields = {'title': p['title'], 'author': ' and '.join(p['authors']), 'year': p['year']}
    if kind == 'inproceedings': fields['booktitle'] = p['venue']
    if kind == 'article': fields['journal'] = p['venue']
    if kind == 'mastersthesis': fields['school'] = p['school']
    if kind == 'techreport' and p.get('institution'): fields['institution'] = p['institution']
    if p['type'] == 'Master’s project': fields['type'] = 'Master\u2019s project report'
    if p['links']: fields['url'] = p['links'][0]['url']
    return '@' + kind + '{' + p['id'] + ',\n' + ',\n'.join('  ' + k + ' = {' + str(v) + '}' for k,v in fields.items()) + '\n}'

def publication(p, detailed=False):
    authors = ', '.join(f'<strong>{e(a)}</strong>' if a == P['name'] else e(a) for a in p['authors'])
    title = anchor(p['title'], p['links'][0]['url']) if p['links'] else e(p['title'])
    citation = f'<details class="citation"><summary>BibTeX citation<span class="sr-only"> for {e(p["title"])}</span></summary><pre>{e(bibtex(p))}</pre></details>' if detailed else ''
    return f'''<article class="publication" id="{e(p['id'])}" aria-labelledby="{e(p['id'])}-title">
      <div class="publication-year">{e(p['year'])}</div><div>
      <h3 id="{e(p['id'])}-title">{title}</h3><p class="authors">{authors}.</p>
      <p class="venue">{e(p['venue'])} · {e(p['year'])}</p>
      <p class="publication-summary">{e(p['summary'])}</p>{links(p['links'])}{citation}</div></article>'''

def project(p):
    fields = [('Problem', 'problem'), ('My contribution', 'contribution'), ('Methods', 'methods'),
              ('Current status' if p['status'] == 'Ongoing' else 'Outcome', 'result')]
    details = ''.join(f'<div><dt>{label}</dt><dd>{e(p[key])}</dd></div>' for label,key in fields if p.get(key))
    ongoing = p['status'] == 'Ongoing'
    return f'''<article class="project{' ongoing' if ongoing else ''}" id="{e(p['id'])}" aria-labelledby="{e(p['id'])}-title">
      <div class="status">{'<span class="status-dot" aria-hidden="true"></span>' if ongoing else ''}{e(p['status'])}</div>
      <h3 id="{e(p['id'])}-title">{e(p['title'])}</h3><p class="summary">{e(p['summary'])}</p>
      <dl>{details}</dl>{links(p['links']) if p['links'] else ''}</article>'''

# Home: identity, current work, research, selected publications, and dated updates.
research_cards = ''.join(f'''<article class="research-card"><span class="index" aria-hidden="true">0{i}</span>
    <h3>{e(r['title'])}</h3><p>{e(r['summary'])}</p>{anchor('Explore this area →', 'research.html#'+r['id'], ' class="text-link"')}</article>'''
    for i,r in enumerate((r for r in P['research'] if r.get('featured', True)),1))
updates = ''.join(f'<li><time datetime="{e(u["date"])}">{e(u["display_date"])}</time><p>{e(u["text"])} ' +
                  (anchor(u['link']['label']+' →',u['link']['url']) if u.get('link') else '') + '</p></li>' for u in UPDATES[:4])
home = f'''<section class="hero" aria-labelledby="intro-title"><div>
    <p class="eyebrow">{e(P['focus'])} · PhD research</p><h1 id="intro-title">{e(P['name'])}</h1>
    <p class="hero-affiliation">PhD student at the {e(P['institution'])}</p>
    <p class="intro">{e(P['intro'])}</p><p class="bio">{e(P['bio'])}</p>
    {links(P['socials'])}<div class="link-row hero-actions">{anchor('Explore my research →','research.html',' class="button"')}{anchor('Download CV (PDF)',P['cv'])}</div>
    </div><aside class="hero-aside" aria-label="Affiliation">
    <img class="portrait" src="assets/portrait.jpg" width="320" height="433" alt="Portrait of Nazmul Haque Turja" fetchpriority="high">
    <div class="affiliation"><strong>{e(P['institution'])}</strong><span class="muted">Electrical &amp; Computer Engineering</span></div></aside></section>
    <aside class="now" aria-label="Current work"><p class="eyebrow">Currently</p><p>{e(P['now'])}</p>{anchor('RTL Medic →','projects.html#rtl-medic')}</aside>
    <section class="section" aria-label="Research areas">{section_heading('Research areas','Research overview','research.html')}<div class="research-grid">{research_cards}</div></section>
    <section class="section" aria-label="Selected publications">{section_heading('Selected publications','All publications','publications.html')}<div>{''.join(publication(p) for p in PUBS if p.get('featured'))}</div></section>
    <section class="section" aria-labelledby="updates-title"><h2 id="updates-title">Recent updates</h2><ul class="updates">{updates}</ul></section>'''
page('index.html',P['name'],f"PhD student at the {P['institution']}. {P['bio']}",home)

research = heading('Research','Hardware security & verification.','My PhD at the University of Delaware focuses on hardware security, informed by experience in hardware verification and computer architecture.')
for i,r in enumerate(P['research'],1):
    research += f'<section class="research-detail" id="{e(r["id"])}"><span class="index" aria-hidden="true">0{i}</span><h2>{e(r["title"])}</h2><div><p>{e(r["body"])}</p>{links(r["links"])}</div></section>'
research += '<section class="page-section"><h2>Ongoing work</h2>'+project(next(p for p in PROJECTS if p['id']=='rtl-medic'))+'</section>'
page('research.html','Research','Hardware security research at the University of Delaware, with ongoing work in AI-assisted hardware design and verification.',research)

pubs = heading('Publications','Papers & reports.','Research on GPU performance prediction, CPU bottleneck analysis, and secure connected systems.',links([P['socials'][1],{'label':'Download citations (.bib)','url':'publications.bib'}]))
for year in sorted({p['year'] for p in PUBS},reverse=True):
    pubs += f'<section class="pub-section" aria-labelledby="year-{year}"><h2 class="eyebrow" id="year-{year}">{year}</h2>'+''.join(publication(p,True) for p in PUBS if p['year']==year)+'</section>'
page('publications.html','Publications','Publications by Nazmul Haque Turja, with paper links and BibTeX citations.',pubs)
(ROOT/'publications.bib').write_text('\n\n'.join(bibtex(p) for p in PUBS)+'\n')

categories=[('ongoing','Ongoing work'),('research','Research projects'),('engineering','Computer engineering'),('iot','Connected systems')]
projects = heading('Projects','From models to working systems.','Selected research, engineering, and collaborative projects. Each entry describes my contribution and the outcome of the work.')
projects += '<nav class="section-nav" aria-label="Project categories">'+''.join(anchor(label,'#'+key) for key,label in categories)+'</nav>'
for key,label in categories:
    projects += f'<section class="page-section" id="{key}"><h2>{label}</h2><div class="project-grid">'+''.join(project(p) for p in PROJECTS if p['category']==key)+'</div></section>'
page('projects.html','Projects','Research and engineering projects, including ongoing RTL Medic, GPU performance modeling, and IoT systems.',projects)

cvsections=[('education','Education'),('experience','Experience'),('technical_skills','Technical skills'),('selected_coursework','Selected coursework'),('awards','Awards'),('publications','Publications'),('projects','Selected projects')]
cv_download = '<div class="link-row">' + anchor('Download CV · September 2026 (PDF)', P['cv'], ' class="button"') + '</div>'
cv = heading('Curriculum vitae','Education & experience.','PhD research in hardware security at the University of Delaware, building on experience in GPU verification and computer architecture.',cv_download)
cv += '<div class="print-heading"><h1>' + e(P['name']) + '</h1><p>' + e(P['email']) + ' · ' + e(P['location']) + '</p></div>'
cv += '<div class="cv-layout"><nav class="cv-nav" aria-label="CV sections">'+''.join(anchor(label,'#'+key) for key,label in cvsections)+'</nav><div>'
for key,label in cvsections:
    cv += f'<section class="cv-section" id="{key}"><h2>{label}</h2>'
    if key == 'publications':
        for pub in PUBS:
            cv += '<div class="cv-entry"><p>' + e(', '.join(pub['authors'])) + '. ' + anchor(pub['title'], pub['links'][0]['url']) + '. ' + e(pub['venue']) + ', ' + str(pub['year']) + '.</p></div>'
    elif key == 'projects':
        for proj in PROJECTS:
            if proj['id'] in ('rtl-medic','asmd','cache','mips','sap','shift-register','wearable'):
                cv += '<div class="cv-entry"><h3>' + e(proj['title']) + '</h3><p>' + e(proj['summary']) + ' ' + e(proj['result']) + '</p></div>'
    for item in CV.get(key, []):
        cv += '<div class="cv-entry">'
        if item.get('title'):
            cv += '<h3>'+e(item['title'])+'</h3><p class="cv-org">'+e(item['organization'])+'</p><p class="cv-meta">'+e(item['location'])+' · '+e(item['period'])+'</p>'
        if item.get('text'): cv += '<p>'+e(item['text'])+'</p>'
        if item['bullets']: cv += '<ul>'+''.join('<li>'+e(b)+'</li>' for b in item['bullets'])+'</ul>'
        cv += '</div>'
    cv += '</section>'
cv += '</div></div>'
page('cv.html','CV','Education, experience, technical skills, and awards. Download the September 2026 CV.',cv)

contact = heading('Contact','Let’s connect.','I’m always open to conversations about hardware security, hardware design, and verification research using LLMs and agentic AI. Feel free to email me.')
contact += f'''<div class="contact-grid"><section><p class="eyebrow">Email</p>{anchor(P['email'],'mailto:'+P['email'],' class="email-link"')}<p class="muted" style="margin-top:1.5rem">{e(P['location'])}</p><p class="small">{e(P['role'])}<br>{e(P['institution'])}</p></section>
    <section><h2>Elsewhere</h2><ul class="contact-list">{''.join('<li>'+anchor(s['label']+' ↗',s['url'])+'</li>' for s in P['socials'] if s['label']!='Email')}</ul>{anchor('View my CV →','cv.html',' class="text-link"')}</section></div>'''
page('contact.html','Contact','Contact Nazmul Haque Turja by email, GitHub, Google Scholar, or LinkedIn.',contact)

teaching = heading('Teaching','Teaching & mentorship.','Supporting learning through theory, lab work, and hands-on engineering projects.')
for title,text in [
 ('New Mexico State University · 2023','As a Graduate Assistant in the Department of ET and SE (January–May 2023), I instructed Communication Systems I (ET 314), including theory and lab sessions, weekly assignments, and projects.'),
 ('New Mexico State University · 2021–2022','As a Graduate Research and Teaching Assistant in ECE (August 2021–May 2022), I taught electronics, digital circuit design, and VHDL to more than 50 students.'),
 ('BRAC University · 2021','As Adjunct Faculty in CSE (February–September 2021), I taught VLSI Design (CSE 460) and Digital Electronics and Pulse Techniques (CSE 350), with labs using Proteus, Quartus II, Microwind, and ModelSim.')]:
    teaching += f'<section class="page-section"><h2>{e(title)}</h2><p>{e(text)}</p></section>'
teaching += '<section class="page-section"><h2>Learning resources</h2>'+anchor('Electrodynamics lecture notes →','Sp20.html',' class="text-link"')+'</section>'
page('teaching.html','Teaching','Teaching experience at NMSU and BRAC University, and electrodynamics lecture resources.',teaching)

resources=heading('Teaching resources','Electrodynamics notes.','Lecture materials from the portfolio archive.')
resources+='<section class="page-section"><h2>Lecture notes</h2><ol class="resource-list">'
for name in sorted((ROOT/'electrodynamics').glob('*.pdf'),key=lambda p:int(p.name.split('_')[0])):
    label=name.stem.split('_',1)[1].replace('_',' ').replace('Anennas','Antennas')
    resources+='<li>'+anchor(label+' (PDF)','electrodynamics/'+name.name)+'</li>'
resources+='</ol></section>'
page('Sp20.html','Teaching resources','Archived electrodynamics lecture notes.',resources)

# Retire template pages belonging to the original site author, keeping old URLs usable.
for name,target in [('Fa19.html','teaching.html'),('MENU.html','index.html'),('blogs.html','index.html'),('jemdoc.py.html','index.html')]:
    title='Page moved'
    (ROOT/name).write_text(f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url={target}"><title>{title}</title></head><body><main><h1>{title}</h1><p>{anchor("Continue to the portfolio",target)}</p></main></body></html>\n')
