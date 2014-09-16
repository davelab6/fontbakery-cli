# coding: utf-8
# Copyright 2013 The Font Bakery Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# See AUTHORS.txt for the list of Authors and LICENSE.txt for the License.
from __future__ import print_function
import os.path as op
import yaml

from bakery_cli.report import utils as report_utils
from bakery_cli.utils import UpstreamDirectory


TAB = 'Upstream'
TEMPLATE_DIR = op.join(op.dirname(__file__), 'templates')

t = lambda templatefile: op.join(TEMPLATE_DIR, templatefile)


def sort(data):
    a = []
    for d in data:
        if 'required' in d['tags']:
            a.append(d)

    for d in data:
        if 'note' in d['tags'] and 'required' not in d['tags']:
            a.append(d)

    for d in data:
        if 'note' not in d['tags'] and 'required' not in d['tags']:
            a.append(d)

    return a


def generate(config, outfile='checks.html'):
    upstreamdatafile = op.join(config['path'], 'upstream.yaml')
    if not op.exists(upstreamdatafile):
        return

    from jinja2 import Template

    template = Template(open(t(outfile)).read())

    destfile = open(op.join(config['path'], outfile), 'w')

    upstream = yaml.load(open(upstreamdatafile))
    app_version = report_utils.git_info(config)
    print(template.render(
        sort=sort, tests=upstream, current_page=outfile, app_version=app_version,
        build_repo_url=report_utils.build_repo_url).encode('utf8'), file=destfile)
