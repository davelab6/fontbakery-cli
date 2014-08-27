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
from bakery_lint.base import BakeryTestCase as TestCase, tags, autofix
from bakery_cli.ttfont import Font


class CheckNbspWidthMatchesSpWidth(TestCase):

    targets = ['result']
    path = '.'
    tool = 'lint'
    name = __name__

    def read_metadata_contents(self):
        return open(self.path).read()

    @tags('required')
    @autofix('bakery_cli.pipe.autofix.fix_nbsp')
    def test_check_nbsp_width_matches_sp_width(self):
        """ Check NO-BREAK SPACE advanceWidth is the same as SPACE """
        tf = Font.get_ttfont(self.path)
        space_advance_width = tf.advance_width('space')
        nbsp_advance_width = tf.advance_width('uni00A0')

        _ = "Font does not contain a sp glyph"
        self.assertTrue(space_advance_width, _)
        _ = "Font does not contain a nbsp glyph"
        self.assertTrue(nbsp_advance_width, _)

        _ = ("The nbsp advance width does not match "
             "the sp advance width")
        self.assertEqual(space_advance_width, nbsp_advance_width, _)
