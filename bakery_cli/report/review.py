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

from bakery_cli.report.utils import render_template
from bakery_cli.report.utils import build_repo_url
from bakery_cli.utils import UpstreamDirectory

from fontaine.cmap import Library
from fontaine.font import FontFactory


TAB = 'Review'
TEMPLATE_DIR = op.join(op.dirname(__file__), 'templates')

t = lambda templatefile: op.join(TEMPLATE_DIR, templatefile)


def get_orthography(fontaineFonts):
    library = Library(collections=['subsets'])
    result = []
    for font, fontaine in fontaineFonts:
        for f1, f2, f3, f4 in fontaine.get_orthographies(_library=library):
            result.append([font, f1, f2, f3, f4])
    return sorted(result, key=lambda x: x[3], reverse=True)


def generate(config, outfile='review.html'):
    directory = UpstreamDirectory(config['path'])
    fonts = [(path, FontFactory.openfont(op.join(config['path'], path)))
             for path in directory.BIN]
    faces = []
    for font in directory.BIN:
        if 'static/' in font:
            continue
        basename = op.basename(font)[:-4]
        faces.append({'name': font, 'basename': basename, 'path': font})
    destfile = open(op.join(config['path'], 'review.html'), 'w')
    print(render_template(outfile, fonts=faces, markdown=markdown,
                          build_repo_url=build_repo_url,
                          get_orthography=get_orthography, fontaineFonts=fonts),
          file=destfile)
