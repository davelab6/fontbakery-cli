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
import os
import sys
from subprocess import Popen

from bakery_cli.utils import UpstreamDirectory


def shell(cmd):
    print('$ %s' % cmd)
    p = Popen(cmd, shell=True, cwd=os.path.join(os.environ['TRAVIS_BUILD_DIR'],
                                                'builds/build'))
    stdout, stderr = p.communicate()
    if stdout:
        print(stdout, end="\n")
    if stderr:
        print(stderr, end="\n")


def create_index_html():
    directory = os.path.join(os.environ['TRAVIS_BUILD_DIR'], 'builds/build')
    p = os.path.join(directory, 'index.html')

    upstream = UpstreamDirectory(directory)
    faces = []
    indexf = open(p, 'w')

    for k, font in enumerate(upstream.BIN):
        basename = os.path.basename(font)[:-4]
        face = ('<style>@font-face {font-family: {0}; src: url({1});}'
                '.face-{2} {font-family: {0};}</style>'
                '<div class="face-{2}">'
                'Grumpy wizards make toxic brew for the evil Queen and Jack'
                '</div>').format(basename, font, k)
        faces.append(face)

    print("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
    %s
</body>
</html>
""" % '\n'.join(faces), file=indexf)


if __name__ == '__main__':

    if os.environ['TRAVIS_PULL_REQUEST'].lower() == 'true':
        sys.exit(1)

    if 'GH_TOKEN' not in os.environ:
        sys.exit(1)

    repo = 'https://github.com/%s.git' % os.environ['TRAVIS_REPO_SLUG']

    deploy_branch = 'gh-pages'

    shell('git init')
    shell('git remote add origin %s' % repo)
    shell('git remote set-branches --add origin %s' % deploy_branch)

    shell("git config user.name '%s'" % os.environ['GIT_NAME'])
    shell("git config user.email '%s'" % os.environ['GIT_EMAIL'])
    shell('git config credential.helper "store --file=.git/credentials"')

    credentials_path = os.path.join(os.environ['TRAVIS_BUILD_DIR'],
                                    'builds/build/.git/credentials')
    with open(credentials_path, 'w') as filep:
        print("https://%s:@github.com" % os.environ['GH_TOKEN'],
              file=filep)

    shell('git add .')
    shell('git commit -a -m "Travis deploy"')

    shell('rm -rf %s' % os.path.join(os.environ['TRAVIS_BUILD_DIR'], '.git'))

    shell('rm -f .git/index.lock')
    shell('git push --force origin master:gh-pages')

    os.remove(credentials_path)
