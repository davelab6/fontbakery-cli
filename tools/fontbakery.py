#!/usr/bin/env python
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
import argparse
from multiprocessing import Pool
import os
import sys
import yaml

from bakery_cli import pipe
from bakery_cli.bakery import Bakery, BAKERY_CONFIGURATION_DEFAULTS
from bakery_cli.utils import UpstreamDirectory


def run_bakery(sourcedir, config=None):

    try:
        if config:
            config = yaml.safe_load(open(config, 'r'))
        else:
            config = yaml.safe_load(open(BAKERY_CONFIGURATION_DEFAULTS))

        if 'process_files' not in config:
            directory = UpstreamDirectory(sourcedir)
            config['process_files'] = directory.get_fonts()

        bakeryyaml = os.path.abspath(os.path.join(sourcedir, '.bakery.yaml'))
        l = open(bakeryyaml, 'w')
        l.write(yaml.safe_dump(config))
        l.close()

        b = Bakery('', sourcedir, 'builds', 'build')

        b.pipes = [
            pipe.Copy,
            pipe.Build,
            pipe.Rename,
            pipe.PyFtSubset,
            pipe.Metadata,
            pipe.FontLint,
            pipe.Optimize,
            pipe.AutoFix,
            pipe.CopyLicense,
            pipe.CopyFontLog,
            pipe.CopyDescription,
            pipe.CopyMetadata,
            pipe.CopyTxtFiles,
            pipe.TTFAutoHint,
            pipe.PyFontaine
        ]

        config = os.path.join(sourcedir, '.bakery.yaml')
        b.load_config(config)

        b.run()
    except Exception, ex:
        print >> sys.stderr, 'FAILED: %s' % sourcedir
        print >> sys.stderr, ex
        raise
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('projectpath', nargs='+',
                        help=("Path to directory with UFO, SFD, TTX, TTF or OTF files"))
    parser.add_argument('--config', type=str, default='')
    args = parser.parse_args()

    # for p in args.projectpath:
    #     run_bakery(p)

    pool = Pool(4)

    pool.map(run_bakery, args.projectpath)
    pool.close()

    pool.join()
