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

import html5lib
import json
import magic
import os
import re
import requests

from bakery_lint.base import (BakeryTestCase as TestCase,
                              tags, dontRunIfNotExists)


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SCRAPE_DATAROOT = os.path.join(ROOT, 'bakery_cli', 'scrapes', 'json')
print SCRAPE_DATAROOT


class MetadataTest(TestCase):

    targets = ['metadata']
    tool = 'METADATA.json'
    path = '.'
    name = __name__

    rules = {
        'myfonts.com': {
            'url': 'http://www.myfonts.com/search/name:{}/fonts/',
            'checkText': 'I&rsquo;ve got nothing'
        },
        'daltonmaag.com': {
            'url': 'http://www.daltonmaag.com/search.html?term={}',
            'checkText': 'No product families matched your search term'
        },
        'fontsmith.com': {
            'url': 'http://www.fontsmith.com/support/search-results.cfm',
            'checkText': "Showing no search results for",
            'method': 'post',
            'keywordParam': 'search'
        },
        'fontbureau.com': {
            'url': 'http://www.fontbureau.com/search/?q={}',
            'checkText': '<h5>Font results</h5> <div class="rule"></div> '
                         '<span class="note">(No results)</span>'
        },
        'houseind.com': {
            'url': 'http://www.houseind.com/search/?search=Oswald',
            'checkText': '<ul id="related-fonts"> <li class="first">No results.</li> </ul>'
        }
    }

    def setUp(self):
        self.metadata = json.load(open(self.path))

    def test_family_is_listed_in_gwf(self):
        """ Fontfamily is listed in Google Font Directory """
        url = 'http://fonts.googleapis.com/css?family=%s' % self.metadata['name'].replace(' ', '+')
        fp = requests.get(url)
        self.assertTrue(fp.status_code == 200, 'No family found in GWF in %s' % url)
        self.assertEqual(self.metadata.get('visibility'), 'External')

    @tags('required')
    def test_metadata_designer_exists_in_profiles_csv(self):
        """ Designer exists in GWF profiles.csv """
        designer = self.metadata.get('designer', '')
        self.assertTrue(designer, 'Field "designer" MUST NOT be empty')
        import urllib
        import csv
        fp = urllib.urlopen('https://googlefontdirectory.googlecode.com/hg/designers/profiles.csv')
        try:
            designers = []
            for row in csv.reader(fp):
                if not row:
                    continue
                designers.append(row[0])
            self.assertTrue(designer in designers,
                            msg='Designer %s is not in profiles.csv' % designer)
        except Exception:
            self.assertTrue(False)

    def test_does_not_familyName_exist_in_myfonts_catalogue(self):
        """ MYFONTS.com """
        test_catalogue = self.rules['myfonts.com']
        self.check(test_catalogue)

    def test_does_not_familyName_exist_in_daltonmaag_catalogue(self):
        """ DALTONMAAG.com """
        test_catalogue = self.rules['daltonmaag.com']
        self.check(test_catalogue)

    def test_does_not_familyName_exist_in_fontsmith_catalogue(self):
        """ FONTSMITH.com """
        test_catalogue = self.rules['fontsmith.com']
        self.check(test_catalogue)

    def test_does_not_familyName_exist_in_fontbureau_catalogue(self):
        """ FONTBUREAU.com """
        test_catalogue = self.rules['fontbureau.com']
        self.check(test_catalogue)

    def test_does_not_familyName_exist_in_houseind_catalogue(self):
        """ HOUSEIND.com """
        test_catalogue = self.rules['houseind.com']
        self.check(test_catalogue)

    @dontRunIfNotExists(os.path.join(SCRAPE_DATAROOT, 'terminaldesign.json'))
    def test_does_not_familyName_exist_in_terminaldesign_catalogue(self):
        """ TERMINALDESIGN.com """
        try:
            datafile = open(os.path.join(SCRAPE_DATAROOT, 'terminaldesign.json'))
            catalogue = json.load(datafile)
            self.assertFalse(self.metadata['name'].lower() in map(lambda x: x['title'].lower(), catalogue))
        except (OSError, IOError):
            assert False, 'Run `make crawl` to get latest data'

    @dontRunIfNotExists(os.path.join(SCRAPE_DATAROOT, 'typography.json'))
    def test_does_not_familyName_exist_in_typography_catalogue(self):
        """ TYPOGRAPHY.com """
        try:
            datafile = open(os.path.join(SCRAPE_DATAROOT, 'typography.json'))
            catalogue = json.load(datafile)
            self.assertFalse(self.metadata['name'].lower() in map(lambda x: x['title'].lower(), catalogue))
        except (OSError, IOError):
            assert False, 'Run `make crawl` to get latest data'

    @dontRunIfNotExists(os.path.join(SCRAPE_DATAROOT, 'europatype.json'))
    def test_does_not_familyName_exist_in_europatype_catalogue(self):
        """ EUROPATYPE.com """
        try:
            datafile = open(os.path.join(SCRAPE_DATAROOT, 'europatype.json'))
            catalogue = json.load(datafile)
            self.assertFalse(self.metadata['name'].lower() in map(lambda x: x['title'].lower(), catalogue))
        except (OSError, IOError):
            assert False, 'Run `make crawl` to get latest data'

    @dontRunIfNotExists(os.path.join(SCRAPE_DATAROOT, 'boldmonday.json'))
    def test_does_not_familyName_exist_in_boldmonday_catalogue(self):
        """ BOLDMONDAY.com """
        try:
            datafile = open(os.path.join(SCRAPE_DATAROOT, 'boldmonday.json'))
            catalogue = json.load(datafile)
            self.assertFalse(self.metadata['name'].lower() in map(lambda x: x['title'].lower(), catalogue))
        except (OSError, IOError):
            assert False, 'Run `make crawl` to get latest data'

    @dontRunIfNotExists(os.path.join(SCRAPE_DATAROOT, 'commercialtype.json'))
    def test_does_not_familyName_exist_in_commercialtype_catalogue(self):
        """ COMMERCIALTYPE.com """
        try:
            datafile = open(os.path.join(SCRAPE_DATAROOT, 'commercialtype.json'))
            catalogue = json.load(datafile)
            self.assertFalse(self.metadata['name'].lower() in map(lambda x: x['title'].lower(), catalogue))
        except (OSError, IOError):
            assert False, 'Run `make crawl` to get latest data'

    @dontRunIfNotExists(os.path.join(SCRAPE_DATAROOT, 'swisstypefaces.json'))
    def test_does_not_familyName_exist_in_swisstypefaces_catalogue(self):
        """ SWISSTYPEFACES.com """
        try:
            datafile = open(os.path.join(SCRAPE_DATAROOT, 'swisstypefaces.json'))
            catalogue = json.load(datafile)
            self.assertFalse(self.metadata['name'].lower() in map(lambda x: x['title'].lower(), catalogue))
        except (OSError, IOError):
            assert False, 'Run `make crawl` to get latest data'

    @dontRunIfNotExists(os.path.join(SCRAPE_DATAROOT, 'grillitype.json'))
    def test_does_not_familyName_exist_in_grillitype_catalogue(self):
        """ GRILLITYPE.com """
        try:
            datafile = open(os.path.join(SCRAPE_DATAROOT, 'grillitype.json'))
            catalogue = json.load(datafile)
            self.assertFalse(self.metadata['name'].lower() in map(lambda x: x['title'].lower(), catalogue))
        except (OSError, IOError):
            assert False, 'Run `make crawl` to get latest data'

    @dontRunIfNotExists(os.path.join(SCRAPE_DATAROOT, 'letterror.json'))
    def test_does_not_familyName_exist_in_letterror_catalogue(self):
        """ LETTERROR.com """
        try:
            datafile = open(os.path.join(SCRAPE_DATAROOT, 'letterror.json'))
            catalogue = json.load(datafile)
            self.assertFalse(self.metadata['name'].lower() in map(lambda x: x['title'].lower(), catalogue))
        except (OSError, IOError):
            assert False, 'Run `make crawl` to get latest data'

    @dontRunIfNotExists(os.path.join(SCRAPE_DATAROOT, 'teff.json'))
    def test_does_not_familyName_exist_in_teff_catalogue(self):
        """ TEFF.nl """
        try:
            datafile = open(os.path.join(SCRAPE_DATAROOT, 'teff.json'))
            catalogue = json.load(datafile)
            self.assertFalse(self.metadata['name'].lower() in map(lambda x: x['title'].lower(), catalogue))
        except (OSError, IOError):
            assert False, 'Run `make crawl` to get latest data'

    @dontRunIfNotExists(os.path.join(SCRAPE_DATAROOT, 'nouvellenoire.json'))
    def test_does_not_familyName_exist_in_nouvellenoire_catalogue(self):
        """ NOUVELLENOIRE.ch """
        try:
            datafile = open(os.path.join(SCRAPE_DATAROOT, 'nouvellenoire.json'))
            catalogue = json.load(datafile)
            self.assertFalse(self.metadata['name'].lower() in map(lambda x: x['title'].lower(), catalogue))
        except (OSError, IOError):
            assert False, 'Run `make crawl` to get latest data'

    @dontRunIfNotExists(os.path.join(SCRAPE_DATAROOT, 'typedifferent.json'))
    def test_does_not_familyName_exist_in_typedifferent_catalogue(self):
        """ TYPEDIFFERENT.com """
        try:
            datafile = open(os.path.join(SCRAPE_DATAROOT, 'typedifferent.json'))
            catalogue = json.load(datafile)
            self.assertFalse(self.metadata['name'].lower() in map(lambda x: x['title'].lower(), catalogue))
        except (OSError, IOError):
            assert False, 'Run `make crawl` to get latest data'

    @dontRunIfNotExists(os.path.join(SCRAPE_DATAROOT, 'optimo.json'))
    def test_does_not_familyName_exist_in_optimo_catalogue(self):
        """ OPTIMO.ch """
        try:
            datafile = open(os.path.join(SCRAPE_DATAROOT, 'optimo.json'))
            catalogue = json.load(datafile)
            self.assertFalse(self.metadata['name'].lower() in map(lambda x: x['title'].lower(), catalogue))
        except (OSError, IOError):
            assert False, 'Run `make crawl` to get latest data'

    def test_does_not_familyName_exist_in_veer_catalogue(self):
        """ VEER.com """
        url = 'http://search.veer.com/json/?keyword={}&producttype=TYP&segment=DEF'.format(self.metadata['name'])
        try:
            response = requests.get(url, timeout=0.2)
            if response.status_code == 200:
                self.assertFalse(bool(response.json()['TotalCount']['type']))
            else:
                self.assertTrue(False)
        except requests.exceptions.Timeout:
            self.assertTrue(False)

    def test_does_not_familyName_exist_in_fontscom_catalogue(self):
        """ FONTS.com """
        url = 'http://www.fonts.com/browse/font-lists?part={}'.format(self.metadata['name'][0])
        try:
            response = requests.get(url, timeout=0.2)
        except requests.exceptions.Timeout:
            self.assertTrue(False)
        if response.status_code == 200:
            tree = html5lib.treebuilders.getTreeBuilder("lxml")
            parser = html5lib.HTMLParser(tree=tree,
                                         namespaceHTMLElements=False)
            doc = parser.parse(response.text)
            f = doc.xpath('//ul/li/a[@class="product productpopper"]/text()')
            self.assertFalse(self.metadata['name'] in map(lambda x: unicode(x).lower(), list(f)))
        else:
            self.assertTrue(False)

    def test_does_not_familyName_exist_in_fontshop_catalogue(self):
        """ FONTSHOP.com """
        url = 'http://www.fontshop.com/service/familiesService.php?dataType=json&searchltr={}'.format(self.metadata['name'][0])
        try:
            response = requests.get(url, timeout=0.2)
        except requests.exceptions.Timeout:
            self.assertTrue(False)
        if response.status_code == 200:
            jsondata = response.json()
            self.assertFalse(self.metadata['name'].lower() in map(lambda x: x['name'].lower(), jsondata))
        else:
            self.assertTrue(False)

    def check(self, test_catalogue):
        url = test_catalogue['url'].format(self.metadata['name'])

        if test_catalogue.get('method') == 'post':
            data = {test_catalogue['keywordParam']: self.metadata['name']}
            response = requests.post(url, allow_redirects=False,
                                     data=data)
        else:
            try:
                response = requests.get(url, allow_redirects=False, timeout=0.2)
            except requests.exceptions.Timeout:
                self.assertTrue(False)
        if response.status_code == 200:
            regex = re.compile('\s+')
            self.assertTrue(test_catalogue['checkText'] in regex.sub(' ', response.text))
        elif response.status_code == 302:  # 302 Moved Temporarily
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_metadata_fonts_no_dupes(self):
        """ METADATA.json fonts propery only should have uniq values """
        fonts = {}
        for x in self.metadata.get('fonts', None):
            self.assertFalse(x.get('fullName', '') in fonts)
            fonts[x.get('fullName', '')] = x

        self.assertEqual(len(set(fonts.keys())),
                         len(self.metadata.get('fonts', None)))

    @tags('required')
    def test_metadata_keys(self):
        """ METADATA.json should have top keys: ["name", "designer",
            "license", "visibility", "category", "size", "dateAdded",
            "fonts", "subsets"] """

        top_keys = ["name", "designer", "license", "visibility", "category",
                    "size", "dateAdded", "fonts", "subsets"]

        for x in top_keys:
            self.assertIn(x, self.metadata, msg="Missing %s key" % x)

    @tags('required')
    def test_metadata_fonts_key_list(self):
        """ METADATA.json font key should be list """
        self.assertEqual(type(self.metadata.get('fonts', '')), type([]))

    @tags('required')
    def test_metadata_subsets_key_list(self):
        """ METADATA.json subsets key should be list """
        self.assertEqual(type(self.metadata.get('subsets', '')), type([]))

    @tags('required')
    def test_subsets_files_is_font(self):
        """ Subset file is a TrueType format """
        for font in self.metadata.get('fonts', []):
            for subset in self.metadata.get('subsets', []) + ['menu']:
                path = os.path.join(os.path.dirname(self.path),
                                    font.get('filename')[:-3] + subset)
                if not os.path.exists(path):
                    self.fail('%s subset file does not exist' % subset)

                if magic.from_file(path) != 'TrueType font data':
                    _ = '%s does not seem to be truetype font data'
                    self.fail(_ % subset)

    @tags('required')
    def test_metadata_fonts_items_dicts(self):
        """ METADATA.json fonts key items are dicts """
        for x in self.metadata.get('fonts', None):
            self.assertEqual(type(x), type({}), msg="type(%s) is not dict" % x)

    @tags('required')
    def test_metadata_top_keys_types(self):
        """ METADATA.json should have proper top keys types """
        self.assertEqual(type(self.metadata.get("name", None)),
                         type(""), msg="name key type invalid")
        self.assertEqual(type(self.metadata.get("designer", None)),
                         type(""), msg="designer key type invalid")
        self.assertEqual(type(self.metadata.get("license", None)),
                         type(""), msg="license key type invalid")
        self.assertEqual(type(self.metadata.get("visibility", None)),
                         type(""), msg="visibility key type invalid")
        self.assertEqual(type(self.metadata.get("category", None)),
                         type(""), msg="category key type invalid")
        self.assertEqual(type(self.metadata.get("size", None)),
                         type(0), msg="size key type invalid")
        self.assertEqual(type(self.metadata.get("dateAdded", None)),
                         type(""), msg="dateAdded key type invalid")

    @tags('required')
    def test_metadata_no_unknown_top_keys(self):
        """ METADATA.json don't have unknown top keys """
        top_keys = ["name", "designer", "license", "visibility", "category",
                    "size", "dateAdded", "fonts", "subsets"]
        for x in self.metadata.keys():
            self.assertIn(x, top_keys, msg="%s found unknown top key" % x)

    @tags('required')
    def test_metadata_atleast_latin_menu_subsets_exist(self):
        """ METADATA.json subsets should have at least 'menu' and 'latin' """
        self.assertIn('menu', self.metadata.get('subsets', []),
                      msg="Subsets missing menu")
        self.assertIn('latin', self.metadata.get('subsets', []),
                      msg="Subsets missing latin")

    @tags('required')
    def test_metadata_license(self):
        """ METADATA.json license is 'Apache2', 'UFL' or 'OFL' """
        licenses = ['Apache2', 'OFL', 'UFL']
        self.assertIn(self.metadata.get('license', ''), licenses)

    @tags('required')
    def test_metadata_has_unique_style_weight_pairs(self):
        """ METADATA.json only contains unique style:weight pairs """
        pairs = []
        for fontdata in self.metadata.get('fonts', []):
            styleweight = '%s:%s' % (fontdata['style'],
                                     fontdata.get('weight', 0))
            self.assertNotIn(styleweight, pairs)
            pairs.append(styleweight)
