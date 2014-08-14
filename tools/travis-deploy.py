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


def shell(cmd):
    p = Popen(cmd, shell=True, cwd=os.path.join(os.environ['TRAVIS_BUILD_DIR'],
                                                'builds/build'))
    p.communicate()


if __name__ == '__main__':

    if os.environ['TRAVIS_PULL_REQUEST'].lower() == 'true':
        sys.exit(1)

    if 'GH_TOKEN' not in os.environ:
        sys.exit(1)

    repo = 'https://github.com/%s.git' % os.environ['TRAVIS_REPO_SLUG']
    deploy_branch = 'gh-pages'

    shell('git init')
    shell('git remote set-url --push origin %s' % repo)
    shell('git remote set-branches --add origin %s' % deploy_branch)
    shell('git fetch -q')

    shell("git config user.name '%s'" % os.environ['GIT_NAME'])
    shell("git config user.email '%s'" % os.environ['GIT_EMAIL'])
    shell('git config credential.helper "store --file=.git/credentials"')

    print("https://%s:@github.com" % os.environ['GH_TOKEN'],
          file=open('.git/credentials', 'w'))
    shell("git branch {0} origin/{0}" % deploy_branch)

    shell('git add .')
    shell('git commit -a ""')
    shell('git push --force --quiet origin master:gh-pages > /dev/null 2>&1')

    os.delete('.git/credentials')
