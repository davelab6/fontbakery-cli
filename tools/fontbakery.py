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
from __future__ import print_function
import argparse
import multiprocessing
import multiprocessing.pool
import os
import sys
import yaml

from bakery_cli import pipe
from bakery_cli.bakery import Bakery, BAKERY_CONFIGURATION_DEFAULTS
from bakery_cli.utils import UpstreamDirectory


class DualLog(object):

    def write(self, msg, prefix=u''):
        if prefix:
            msg = prefix + msg
        print(msg.encode('utf8'))


def run_bakery(sourcedir, config=None):
    sourcedir = os.path.realpath(sourcedir)
    try:
        if config:
            bakeryyaml = open(os.path.join(sourcedir, "bakery.yaml"), 'r')
            config = yaml.safe_load(bakeryyaml)
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
            pipe.PyFontaine,
            pipe.UpstreamLint,
            pipe.Build,
            pipe.PyFtSubset,
            pipe.Metadata,
            pipe.FontLint,
            pipe.Optimize,
            pipe.MetadataLint,
            pipe.CopyTxtFiles,
            pipe.TTFAutoHint,
            pipe.FontCrunch
        ]

        buildlog_path = os.path.join(sourcedir, 'builds', 'build', 'build.log')
        if not os.path.exists(os.path.join(sourcedir, 'builds', 'build')):
            os.makedirs(os.path.join(sourcedir, 'builds', 'build'))

        config = os.path.join(sourcedir, '.bakery.yaml')
        b.load_config(config)

        b.run()
    except Exception, ex:
        print('FAILED: %s' % sourcedir, file=sys.stderr)
        print(ex, file=sys.stderr)
        raise


class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)


# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class Pool(multiprocessing.pool.Pool):

    Process = NoDaemonProcess


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('projectpath', nargs='+',
                        help=("Path to directory with UFO, SFD, TTX, TTF or OTF files"))
    args = parser.parse_args()

    for p in args.projectpath:
        run_bakery(p)

    # pool = Pool(4)

    # pool.map(run_bakery, args.projectpath)
    # pool.close()

    # pool.join()
