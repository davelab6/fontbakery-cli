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
from markdown import markdown
import yaml
import json

from bakery_cli.report import utils as report_utils

TAB = 'METADATA.json'
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


def generate(config, outfile='metadata.html'):
    if not op.exists(op.join(config['path'], 'METADATA.json')):
        return

    try:
        data = yaml.load(open(op.join(config['path'], 'METADATA.yaml')))
    except IOError:
        data = {}

    tests_summary_filepath = op.join(config['path'], 'tests.json')
    if op.exists(tests_summary_filepath):
        tests_summary = json.load(open(tests_summary_filepath))

    summary = {
        'success': len(data.get('METADATA.json', {}).get('success', [])),
        'error': len(data.get('METADATA.json', {}).get('error', [])),
        'failure': len(data.get('METADATA.json', {}).get('failure', []))
    }
    tests_summary.update({'METADATA.json': summary})
    json.dump(tests_summary, open(tests_summary_filepath, 'w'))

    destfile = open(op.join(config['path'], outfile), 'w')

    metadata = open(op.join(config['path'], 'METADATA.json')).read()

    try:
        metadata_new = open(op.join(config['path'], 'METADATA.json.new')).read()
    except (IOError, OSError):
        metadata_new = ''
    app_version = report_utils.git_info(config)
    print(report_utils.render_template(
        outfile, metadata=metadata, tests=data, sort=sort,
        app_version=app_version, build_repo_url=report_utils.build_repo_url,
        current_page=outfile, metadata_new=metadata_new,
        markdown=markdown), file=destfile)
