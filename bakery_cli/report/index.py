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

from bakery_cli.scripts.vmet import metricview
from bakery_cli.utils import UpstreamDirectory
from bakery_cli.report.utils import render_template

from fontaine.cmap import Library
from fontaine.font import FontFactory


TAB = 'Index'
TEMPLATE_DIR = op.join(op.dirname(__file__), 'templates')

t = lambda templatefile: op.join(TEMPLATE_DIR, templatefile)


def filter_with_tag(fonttestdata, tag):
    tests = fonttestdata['failure'] + fonttestdata['error']
    return [test for test in tests if tag in test['tags']]


def get_fonts_table_sizes(fonts):
    """ Returns tuple with available tables from all fonts and their length """
    from fontTools.ttLib import sfnt
    _fonts = {}
    tables = []
    for font in fonts:
        _fonts[op.basename(font)] = {}
        with open(font) as fp_font:
            sf = sfnt.SFNTReader(fp_font)
            for t in sf.tables:
                if t not in tables:
                    tables.append(t)
                _fonts[op.basename(font)][t] = sf.tables[t].length
    return tables, _fonts


def get_orthography(fontaineFonts):
    library = Library(collections=['subsets'])
    result = []
    for font, fontaine in fontaineFonts:
        for f1, f2, f3, f4 in fontaine.get_orthographies(_library=library):
            result.append([font, f1, f2, f3, f4])
    return sorted(result, key=lambda x: x[3], reverse=True)


def to_google_data_list(tdict, haxis=0):
    return sorted([[x, tdict[x] - haxis] for x in tdict])


def average_table_size(tdict):
    return sum([x for x in tdict.values()]) / len(tdict)


def generate(config):
    directory = UpstreamDirectory(config['path'])

    faces = []

    for font in directory.BIN:
        if 'static/' in font:
            continue
        basename = op.basename(font)[:-4]
        faces.append({'basename': basename, 'path': font})

    destfile = open(op.join(config['path'], 'index.html'), 'w')
    data = yaml.load(open(op.join(config['path'], 'METADATA.yaml')))
    basenames = [op.basename(font['path']) for font in faces]

    fontpaths = [op.join(config['path'], path)
                 for path in directory.BIN]
    ttftablesizes = get_fonts_table_sizes(fontpaths)

    buildstate = yaml.load(open(op.join(config['path'],
                                'build.state.yaml')))
    autohint_sizes = buildstate.get('autohinting_sizes', [])
    vmet = metricview(fontpaths)

    fonts = [(path, FontFactory.openfont(op.join(config['path'], path)))
             for path in directory.BIN]

    print(render_template('index.html', fonts=faces, tests=data,
                          basenames=basenames,
                          filter_with_tag=filter_with_tag,
                          vmet=vmet,
                          autohinting_sizes=autohint_sizes,
                          ttftablesizes=ttftablesizes,
                          fontaineFonts=fonts,
                          get_orthography=get_orthography,
                          to_google_data_list=to_google_data_list,
                          average_table_size=average_table_size,
                          hex=hex),
          file=destfile)
