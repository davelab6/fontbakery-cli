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
from collections import defaultdict, Counter, namedtuple, OrderedDict
import os.path as op
import yaml

from bakery_cli.scripts.vmet import metricview, get_metric_view
from bakery_cli.utils import UpstreamDirectory
from bakery_cli.report.utils import render_template
from bakery_cli.report.utils import build_repo_url

from fontaine.cmap import Library
from fontaine.font import FontFactory


TAB = 'Index'
TEMPLATE_DIR = op.join(op.dirname(__file__), 'templates')

t = lambda templatefile: op.join(TEMPLATE_DIR, templatefile)


def sort(data):
    a = []
    for grouped_dict in data:
        if 'required' in grouped_dict['tags']:
            a.append(grouped_dict)

    for grouped_dict in data:
        if 'note' in grouped_dict['tags'] and 'required' not in grouped_dict['tags']:
            a.append(grouped_dict)

    for grouped_dict in data:
        if 'note' not in grouped_dict['tags'] and 'required' not in grouped_dict['tags']:
            a.append(grouped_dict)

    return a


def filter_with_tag(fonttestdata, tag):
    tests = fonttestdata['failure'] + fonttestdata['error']
    return [test for test in tests if tag in test['tags']]


def filter_by_results_with_tag(fonttestdata, tag, *results):
    tests = []
    for res in results:
        tests = tests + fonttestdata.get(res)
    return [test for test in tests if tag in test.get('tags')]


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


def get_fonts_table_sizes_grouped(fonts_list):
    _, fonts = get_fonts_table_sizes(fonts_list)
    fonts_dict = defaultdict(dict, fonts)

    # fonts may have different tables
    table_sizes_sums = sum(
        (Counter(v) for k, v in fonts_dict.iteritems()), Counter()
    )
    tables_counts = sum(
        (Counter(v.keys()) for k, v in fonts_dict.iteritems()), Counter()
    )
    tables_mean_dict = {
        k: table_sizes_sums[k]/tables_counts[k] for k in table_sizes_sums
    }

    tables_delta_dict = {}
    for font, tables in fonts_dict.iteritems():
        tables_delta_dict[font] = {
            k: tables_mean_dict[k]-v for k, v in tables.iteritems()
        }

    tables_delta_dict_for_google_array = {}
    for font, props in tables_delta_dict.iteritems():
        tables_delta_dict_for_google_array.setdefault('fonts', []).append(font)
        for k, v in props.iteritems():
            tables_delta_dict_for_google_array.setdefault(k, []).append(v)
    
    tables_dict_for_google_array = {}
    for font, props in fonts.iteritems():
        tables_dict_for_google_array.setdefault('fonts', []).append(font)
        for k, v in props.iteritems():
            tables_dict_for_google_array.setdefault(k, []).append(v)
    
    grouped_dict = {
        'fonts': tables_dict_for_google_array.pop('fonts'),
        'tables': [
            [k, tables_mean_dict[k]] + v for k, v in tables_dict_for_google_array.items()
        ]
    }

    delta_dict = {
        'fonts': tables_delta_dict_for_google_array.pop('fonts'),
        'tables': [
            [k, ] + v for k, v in tables_delta_dict_for_google_array.items()
        ]
    }

    # make all arrays to have same len
    max_len = len(max(grouped_dict['tables'], key=len))
    new_items = []
    for item in grouped_dict["tables"]:
        new_item = item[:]
        while len(new_item) < max_len:
            new_item.append(-1)
        new_items.append(new_item)
    grouped_dict["tables"] = new_items

    ftable = namedtuple('FontTable', ['mean', 'grouped', 'delta'])
    return ftable(tables_mean_dict, grouped_dict, delta_dict)


def get_orthography(fontaineFonts):
    fonts_dict = defaultdict(list)
    library = Library(collections=['subsets'])
    fonts_names = []
    for font, fontaine in fontaineFonts:
        fonts_names.append(font)
        for charmap, support, coverage, missing_chars in fontaine.get_orthographies(_library=library):
            font_info = dict(name=font, support=support,
                             coverage=coverage, missing_chars=missing_chars)
            fonts_dict[charmap.common_name].append(font_info)
    averages = {}
    for subset, fonts in fonts_dict.items():
        averages[subset] = sum([font['coverage'] for font in fonts]) / len(fonts)
    return sorted(fonts_names), averages, OrderedDict(sorted(fonts_dict.items()))


def to_google_data_list(tdict, haxis=0):
    return sorted([[x, tdict[x] - haxis] for x in tdict])


def font_table_to_google_data_list(tdict):
    return sorted([list(item) for item in tdict.items()])


def average_table_size(tdict):
    return sum(tdict.values()) / len(tdict)


def generate(config):
    directory = UpstreamDirectory(config['path'])

    faces = []

    for font in directory.BIN:
        if 'static/' in font:
            continue
        basename = op.basename(font)[:-4]
        faces.append({'name': font, 'basename': basename, 'path': font})

    destfile = open(op.join(config['path'], 'index.html'), 'w')
    data = yaml.load(open(op.join(config['path'], 'METADATA.yaml')))
    basenames = [op.basename(font['path']) for font in faces]

    fontpaths = [op.join(config['path'], path)
                 for path in directory.BIN]
    ttftablesizes = get_fonts_table_sizes(fontpaths)

    ftables_data = get_fonts_table_sizes_grouped(fontpaths)
    ttftablesizes_mean = sorted(
        [list(item) for item in ftables_data.mean.items()]
    )
    ttftablesizes_grouped = ftables_data.grouped
    ttftablesizes_delta = ftables_data.delta

    buildstate = yaml.load(open(op.join(config['path'], 'build.state.yaml')))
    autohint_sizes = buildstate.get('autohinting_sizes', [])
    vmet = get_metric_view(fontpaths)

    fonts = [(path, FontFactory.openfont(op.join(config['path'], path)))
             for path in directory.BIN]

    print(render_template('index.html', fonts=faces, tests=data,
                          basenames=basenames,
                          filter_with_tag=filter_with_tag,
                          filter_by_results_with_tag=filter_by_results_with_tag,
                          vmet=vmet._its_metrics,
                          vhead=vmet._its_metrics_header,
                          autohinting_sizes=autohint_sizes,
                          ttftablesizes=ttftablesizes,
                          fontaineFonts=fonts,
                          get_orthography=get_orthography,
                          to_google_data_list=to_google_data_list,
                          font_table_to_google_data_list=font_table_to_google_data_list,
                          ttftablesizes_mean=ttftablesizes_mean,
                          ttftablesizes_grouped=ttftablesizes_grouped,
                          ttftablesizes_delta=ttftablesizes_delta,
                          average_table_size=average_table_size,
                          build_repo_url=build_repo_url,
                          hex=hex, sort=sort),
          file=destfile)
