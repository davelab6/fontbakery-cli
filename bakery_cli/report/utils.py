import os.path as op
import os

GH = 'https://github.com'
TEMPLATE_DIR = op.join(op.dirname(__file__), 'templates')


def render_template(templatename, *args, **kwargs):
    from jinja2 import Template
    template = Template(open(op.join(TEMPLATE_DIR, templatename)).read())
    return template.render(*args, **kwargs).encode('utf8')


def build_repo_url(*chunks):
    repo_slug = os.environ.get('TRAVIS_REPO_SLUG', None)
    if not repo_slug:
        raise ValueError('"TRAVIS_REPO_SLUG" is nod defined in environment')
    return op.join(GH, repo_slug, *chunks)
