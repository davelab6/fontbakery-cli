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

from bakery_cli.report import utils as report_utils


TAB = 'Bakery'


def generate(config, outfile='bakery-yaml.html'):
    if not op.exists(op.join(config['path'], 'bakery.yaml')):
        return

    destfile = open(op.join(config['path'], outfile), 'w')

    data = open(op.join(config['path'], 'bakery.yaml')).read()
    app_version = report_utils.git_info(config)

    report_app = report_utils.ReportApp(config)
    report_app.bakeryyaml_page.copy_file(op.join(config['path'], 'bakery.yaml'))

    print(report_utils.render_template(
        outfile, data=data, app_version=app_version, current_page=outfile,
        build_repo_url=report_utils.build_repo_url,).encode('utf8'), file=destfile)
