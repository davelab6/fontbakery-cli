import json
import os.path as op
import os
import sys
import subprocess

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


def prun(command, cwd, log=None):
    """
    Wrapper for subprocess.Popen that capture output and return as result

        :param command: shell command to run
        :param cwd: current working dir
        :param log: loggin object with .write() method

    """
    # print the command on the worker console
    print("[%s]:%s" % (cwd, command))
    env = os.environ.copy()
    env.update({'PYTHONPATH': os.pathsep.join(sys.path)})
    process = subprocess.Popen(command, shell=True, cwd=cwd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               close_fds=True, env=env)
    if log:
        log.write('$ %s\n' % command)

    stdout = ''
    for line in iter(process.stdout.readline, ''):
        if log:
            log.write(line)
        stdout += line
        process.stdout.flush()
    return stdout


def git_info(config):
    """ If application is under git then return commit's hash
        and timestamp of the version running.

        Return None if application is not under git."""
    params = "git log -n1"
    fmt = """ --pretty=format:'{"hash":"%h", "commit":"%H","date":"%cd"}'"""
    log = prun(params + fmt, cwd=config['path'])
    try:
        return json.loads(log)
    except ValueError:
        return None