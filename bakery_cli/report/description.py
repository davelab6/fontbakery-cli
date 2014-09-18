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
import re

from markdown import markdown
from tidylib import tidy_document
import lxml.etree as etree

from bakery_cli.report import utils as report_utils


TAB = 'Description'
TEMPLATE_DIR = op.join(op.dirname(__file__), 'templates')

t = lambda templatefile: op.join(TEMPLATE_DIR, templatefile)


def reformat_contents(path):
    doc = etree.fromstring(open(path).read(), parser=etree.HTMLParser())

    for node in doc.xpath('//*'):
        if not node.text:
            continue

        node.text = '\n'.join(re.findall(r'(.+?[.]+)', node.text.strip()))
        print(node.text.strip())

    doc = etree.tostring(doc, pretty_print=True)
    doc, _ = tidy_document(doc, {'show-body-only': True})
    return doc


def generate(config, outfile='description.html'):
    source_file = op.join(config['path'], 'DESCRIPTION.en_us.html')
    if not op.exists(source_file):
        return
    data = open(source_file).read()

    print(reformat_contents(source_file), file=open(source_file, 'w'))

    destfile = open(op.join(config['path'], outfile), 'w')

    app_version = report_utils.git_info(config)
    print(report_utils.render_template(outfile,
        app_version=app_version, data=data, current_page=outfile,
        build_repo_url=report_utils.build_repo_url,
        markdown=markdown), file=destfile)
