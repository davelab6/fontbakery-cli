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
from lxml import etree
from cStringIO import StringIO


TAB = 'Description'
TEMPLATE_DIR = op.join(op.dirname(__file__), 'templates')

t = lambda templatefile: op.join(TEMPLATE_DIR, templatefile)


def generate(config, outfile='description.html'):
    from jinja2 import Template

    template = Template(open(t(outfile)).read())

    destfile = open(op.join(config['path'], outfile), 'w')

    data = open(op.join(config['path'], 'DESCRIPTION.en_US.html')).read()
    # t = etree.parse(StringIO(data))

    print(template.render(data=data,
                          markdown=markdown).encode('utf8'), file=destfile)
