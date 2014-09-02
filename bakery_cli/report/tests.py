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

from bakery_cli.utils import weighted_dict_sort


TAB = 'Tests'
TEMPLATE_DIR = op.join(op.dirname(__file__), 'templates')

t = lambda templatefile: op.join(TEMPLATE_DIR, templatefile)


def sort(data):
    data = weighted_dict_sort(data)

    a = set([])
    for d in data:
        if 'required' in data[d]['tags']:
            a.add(d)

    for d in data:
        if 'note' in data[d]['tags'] and 'required' not in data[d]['tags']:
            a.add(d)

    for d in data:
        if 'note' not in data[d]['tags'] and 'required' not in data[d]['tags']:
            a.add(d)

    return a

def generate(config):
    from jinja2 import Template

    data = yaml.load(open(op.join(config['path'], '.tests.yaml')))

    tests = {}

    for font in data:

        for test in data[font]['success']:
            methodname = test['methodName']
            if methodname not in tests:
                tests[methodname] = {
                    'methodDoc': test['methodDoc'],
                    'methodName': test['methodName'],
                    'name': test['name'],
                    'tags': test['tags'],
                    'targets': test['targets'],
                    'tool': test['tool'],
                    'fonts': []
                }

            tests[methodname]['fonts'].append({
                'name': font,
                'status': 'OK'
                })

        for test in data[font]['error']:
            methodname = test['methodName']
            if methodname not in tests:
                tests[methodname] = {
                    'methodDoc': test['methodDoc'],
                    'methodName': test['methodName'],
                    'name': test['name'],
                    'tags': test['tags'],
                    'targets': test['targets'],
                    'tool': test['tool'],
                    'fonts': []
                }

            tests[methodname]['fonts'].append({
                'name': font,
                'status': 'ERROR',
                'err_msg': test['err_msg']
                })

        for test in data[font]['failure']:
            methodname = test['methodName']
            if methodname not in tests:
                tests[methodname] = {
                    'methodDoc': test['methodDoc'],
                    'methodName': test['methodName'],
                    'name': test['name'],
                    'tags': test['tags'],
                    'targets': test['targets'],
                    'tool': test['tool'],
                    'fonts': []
                }

            tests[methodname]['fonts'].append({
                'name': font,
                'status': 'FAIL',
                'err_msg': test['err_msg']
                })

        for test in data[font]['fixed']:
            methodname = test['methodName']
            if methodname not in tests:
                tests[methodname] = {
                    'methodDoc': test['methodDoc'],
                    'methodName': test['methodName'],
                    'name': test['name'],
                    'tags': test['tags'],
                    'targets': test['targets'],
                    'tool': test['tool'],
                    'fonts': []
                }

            tests[methodname]['fonts'].append({
                'name': font,
                'status': 'FIXED',
                'err_msg': test['err_msg']
                })

    template = Template(open(t('tests.html')).read())

    destfile = open(op.join(config['path'], 'tests.html'), 'w')

    print(template.render(tests=tests, sort=sort).encode('utf8'),
          file=destfile)
