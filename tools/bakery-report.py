#!/usr/bin/python
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
import argparse
import os

from bakery_cli.report import (tests, index, buildlog, checks, metadata,
                               bakery, description, review)


if __name__ == '__main__':
    try:
        import jinja2
    except IndexError:
        print(('Bakery report script uses jinja2 template engine.'
               ' Please install jinja2 before using'))

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--result', type=int, default=0)
    parser.add_argument('path')

    args = parser.parse_args()
    if int(args.result) == 0:
        conf = {'path': args.path}
        tests.generate(conf)
        index.generate(conf)
        metadata.generate(conf)
        description.generate(conf)
        checks.generate(conf)
        review.generate(conf)
        bakery.generate(conf)
        buildlog.generate(conf)
    else:
        conf = {'path': args.path, 'failed': True}
        index.generate(conf)

