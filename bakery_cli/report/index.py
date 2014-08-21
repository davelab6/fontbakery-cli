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


from bakery_cli.utils import UpstreamDirectory


TAB = 'Index'
TEMPLATE_DIR = op.join(op.dirname(__file__), 'templates')

t = lambda templatefile: op.join(TEMPLATE_DIR, templatefile)


def generate(config):
    from jinja2 import Template
    upstream = UpstreamDirectory(config['path'])

    faces = []

    for font in upstream.BIN:
        if 'static/' in font:
            continue
        basename = op.basename(font)[:-4]
        faces.append({'basename': basename, 'path': font})

    template = Template(open(t('index.html')).read())

    destfile = open(op.join(config['path'], 'index.html'), 'w')
    print(template.render(fonts=faces).encode('utf8'), file=destfile)