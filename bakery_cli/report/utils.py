import os.path as op

TEMPLATE_DIR = op.join(op.dirname(__file__), 'templates')


def render_template(templatename, *args, **kwargs):
    from jinja2 import Template
    template = Template(open(op.join(TEMPLATE_DIR, templatename)).read())
    return template.render(*args, **kwargs).encode('utf8')
