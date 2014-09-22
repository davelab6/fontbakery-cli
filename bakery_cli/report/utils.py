import json
import os.path as op
import os
import sys
import subprocess
import shutil
import six
from jinja2 import Environment, FileSystemLoader

try:
    import urllib.parse as urllib_parse
except ImportError:
    from urllib import urlencode as urllib_parse


GH = 'https://github.com'
GH_RAW = 'https://raw.githubusercontent.com/'
TEMPLATE_DIR = op.join(op.dirname(__file__), 'templates')
APP_DIR = op.join(op.dirname(__file__), 'app')
jinjaenv = Environment(loader=FileSystemLoader(TEMPLATE_DIR),
                       extensions=["jinja2.ext.do", ],)


def render_template(templatename, *args, **kwargs):
    template = jinjaenv.get_template(templatename)
    return template.render(*args, **kwargs).encode('utf8')


def _build_repo_url(base_url, *chunks, **kwargs):
    repo_slug = os.environ.get('TRAVIS_REPO_SLUG', 'fontdirectory/dummy')
    if kwargs:
        return '{}?{}'.format(op.join(base_url, repo_slug, *chunks), urllib_parse(kwargs))
    return op.join(base_url, repo_slug, *chunks)


def build_repo_url(*chunks, **kwargs):
    return _build_repo_url(GH, *chunks, **kwargs)


def build_raw_repo_url(*chunks, **kwargs):
    return _build_repo_url(GH_RAW, *chunks, **kwargs)


jinjaenv.globals['build_repo_url'] = build_repo_url
jinjaenv.globals['build_raw_repo_url'] = build_raw_repo_url


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


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class lazy_property(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        result = self.func(instance)
        setattr(instance, self.func.__name__, result)
        return result


class ReportApp(six.with_metaclass(Singleton, object)):
    def __init__(self, config, **kwargs):
        self.config = config
        self.source_dir = kwargs.get('source_dir', APP_DIR)
        self.target_dir = kwargs.get('target_dir', op.join(self.config['path'], 'app'))
        self.data_dir = kwargs.get('data_dir', op.join(self.target_dir, 'data'))
        self.static_dir = kwargs.get('static_dir', op.join(self.target_dir, 'static'))
        self.bower_components = kwargs.get('bower_components', ['angular-markdown-directive', 'angular-bootstrap'])
        self.make()
        print('Report Application created.')
        self.write_app_info()
        self.bower_install()

    def bower_install(self):
        #TODO dependency on bower is temporary
        #cdn is preferred, if js can't be on cdn, it will be in static data
        print('Installing components')
        params = ' '.join(self.bower_components)
        log = prun('bower install {}'.format(params), self.static_dir)
        print(log)

    def exists(self):
        return op.exists(self.target_dir)

    def clean(self):
        if self.exists():
            shutil.rmtree(self.target_dir)
    
    def make(self):
        self.clean()
        shutil.copytree(self.source_dir, self.target_dir)

    def copy_file(self, src, dst):
        try:
            print('Copying file: {} -> {}'.format(src, dst))
            shutil.copy(src, dst)
        except shutil.Error as e:
            print('Error: %s' % e)
        except IOError as e:
            print('Error: %s' % e.strerror)

    def move_file(self, src, dst):
        try:
            print('Moving file: {} -> {}'.format(src, dst))
            shutil.move(src, dst)
        except shutil.Error as e:
            print('Error: %s' % e)
        except IOError as e:
            print('Error: %s' % e.strerror)

    def copy_to_data(self, src):
        self.copy_file(src, self.data_dir)

    def move_to_data(self, src):
        self.move_file(src, self.data_dir)

    def dump_to_file(self, data, fname):
        print('Writing data to file: {}'.format(fname))
        with open(op.join(self.data_dir, fname), 'w') as outfile:
            json.dump(data, outfile)

    def write_app_info(self):
        self.dump_to_file(self.version, 'app.json')
        self.dump_to_file(self.repo, 'repo.json')

    @lazy_property
    def version(self):
        return git_info(self.config)

    @lazy_property
    def repo(self):
        repo_url = build_repo_url()
        repo_gh_pages = build_repo_url('tree', 'gh-pages')
        return dict(url=repo_url, gh_pages=repo_gh_pages)
