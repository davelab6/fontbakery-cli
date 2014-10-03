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

from setuptools import setup

setup(
    name="FontBakery-cli",
    version='0.0.2',
    url='https://github.com/googlefonts/fontbakery-cli/',
    description='fontbakery-cli',
    author='Vitaliy Volkov',
    author_email='hash3g@gmail.com',
    packages=["bakery_cli",
              "bakery_cli.pipe",
              "bakery_cli.scripts",
              "bakery_lint",
              "bakery_lint.tests",
              "bakery_lint.tests.downstream",
              "bakery_lint.tests.upstream",
              "bakery_cli.report",
              "bakery_cli.scrapes",
              "bakery_cli.scrapes.familynames",
              "bakery_cli.scrapes.familynames.familynames",
              "bakery_cli.scrapes.familynames.familynames.spiders"],
    scripts=['tools/fontbakery-build.py',
             'tools/fontbakery-build-font2ttf.py',
             'tools/fontbakery-build-metadata.py',
             'tools/fontbakery-fix-ascii-fontmetadata.py',
             'tools/fontbakery-fix-fstype.py',
             'tools/fontbakery-fix-nbsp.py',
             'tools/fontbakery-fix-style-names.py',
             'tools/fontbakery-fix-opentype-names.py',
             'tools/fontbakery-fix-vertical-metrics.py',
             'tools/fontbakery-check.py',
             'tools/fontbakery-travis-deploy.py',
             'tools/fontbakery-report.py',
             'tools/fontbakery-fix-gasp.py',
             'tools/fontbakery-fix-dsig.py',
             'tools/fontbakery-fix-glyph-private-encoding.py',
             'tools/collection-management/fontbakery-travis-secure.sh'],
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    package_data={
        '': [
            'defaults.yaml',
            'scrapes/familynames/scrapy.cfg',
            'tests/upstream/diacritics.txt',
            'tests/*.txt',
            'tests/*.mkd',
            'report/templates/*.html',
            'report/templates/css/*.*',
        ]
    },
    install_requires=[
        'lxml',
        'requests',
        'pyyaml',
        'robofab',
        'fontaine',
        'html5lib',
        'python-magic',
        'markdown'
    ],
    setup_requires=['nose', 'mock', 'coverage'],
    dependency_links=['https://github.com/behdad/fontTools/tarball/master#egg=fonttools-2.4'],
    test_suite='nose.collector'
)
