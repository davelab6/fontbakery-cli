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

from collections import defaultdict, Counter, namedtuple
import os.path as op
import yaml
import json

from bakery_cli.report import utils as report_utils
from bakery_cli.utils import UpstreamDirectory

TAB = 'Tests'
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

    # Fonts may have different tables!!!

    # across all fonts calculate sum of each table
    table_sizes_sums = sum(
        (Counter(v) for k, v in fonts_dict.iteritems()), Counter()
    )

    # count amount of each table across all fonts
    tables_counts = sum(
        (Counter(v.keys()) for k, v in fonts_dict.iteritems()), Counter()
    )

    # count average for each table, take value from 'table_sizes_sums'
    # and divide by corresponding value from  'tables_counts',
    # eg table_sizes_sums['glyf'] / tables_counts['glyf']
    tables_mean_dict = {
        k: table_sizes_sums[k]/tables_counts[k] for k in table_sizes_sums
    }

    # calculate deviation (delta) from an average
    # for each font and each table in font find delta
    tables_delta_dict = {}
    for font, tables in fonts_dict.iteritems():
        tables_delta_dict[font] = {
            k: tables_mean_dict[k]-v for k, v in tables.iteritems()
        }

    # gather all existent tables from all fonts
    all_possible_tables = set()
    for font, tables in tables_delta_dict.items():
        for table in tables:
            if table not in all_possible_tables:
                all_possible_tables.add(table)

    # if some font does not have a table that others have,
    # just set the deviation to 0
    for font, tables in tables_delta_dict.items():
        for item in all_possible_tables:
            tables.setdefault(item, 0)
        tables_delta_dict[font] = tables

    # make the deviation dict ready for google chart as array
    tables_delta_dict_for_google_array = {}
    for font, props in tables_delta_dict.iteritems():
        tables_delta_dict_for_google_array.setdefault('fonts', []).append(font)
        for k, v in props.iteritems():
            tables_delta_dict_for_google_array.setdefault(k, []).append(v)

    # prepare all tables dict as array for google chart
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
            new_item.append(0)
        new_items.append(new_item)
    grouped_dict["tables"] = new_items

    ftable = namedtuple('FontTable', ['mean', 'grouped', 'delta'])
    return ftable(tables_mean_dict, grouped_dict, delta_dict)


def generate(config, outfile='tests.html'):
    directory = UpstreamDirectory(config['path'])

    tests = {}

    data = {}
    for fp in directory.BIN:
        path = op.join(config['path'], '{}.yaml'.format(fp[:-4]))
        if op.exists(path):
            data[fp] = yaml.load(open(path))
            tests[fp] = {'success': len(data[fp].get('success', [])),
                         'error': len(data[fp].get('error', [])),
                         'failure': len(data[fp].get('failure', []))}

    if not data:
        return

    tests_summary = {}
    tests_summary_filepath = op.join(config['path'], 'tests.json')
    if op.exists(tests_summary_filepath):
        tests_summary = json.load(open(tests_summary_filepath))
    tests_summary.update(tests)

    json.dump(tests_summary, open(tests_summary_filepath, 'w'))

    destfile = open(op.join(config['path'], outfile), 'w')
    fontpaths = [op.join(config['path'], path) for path in directory.BIN]
    ftables_data = get_fonts_table_sizes_grouped(fontpaths)
    app_version = report_utils.git_info(config)
    print(report_utils.render_template(outfile,
        ttftablesizes_grouped=ftables_data.grouped,
        tests=data, sort=sort, current_page=outfile, app_version=app_version,
        build_repo_url=report_utils.build_repo_url), file=destfile)
