import re

from bakery_lint.base import BakeryTestCase, tags
from fontTools.agl import AGL2UV
from fontTools.ttLib import TTFont
import robofab.world


uniNamePattern = re.compile(
    "uni"
    "([0-9A-Fa-f]{4})"
    "$"
)


def get_first_cmap_table(ttfont, variants):
    for table in ttfont['cmap'].tables:
        if (table.platformID, table.platEncID) in variants:
            return table


class UnicodeValueShouldAppearOnlyOnce(BakeryTestCase):

    targets = ['upstream']
    name = __name__
    tool = 'lint'

    @tags('note')
    def testUnicodeValue(self):
        """ A Unicode value should appear only once per font """

        font = robofab.world.OpenFont(self.operator.path)

        for glyphname in font.keys():
            glyph = font[glyphname]

            uni = glyph.unicode
            name = glyph.name

            # test for uniXXXX name
            m = uniNamePattern.match(name)
            if m is not None:
                uniFromName = m.group(1)
                uniFromName = int(uniFromName, 16)
                if uni != uniFromName:
                    self.fail("The Unicode value for {} does not match its name.".format(name))
            # test against AGLFN
            else:
                expectedUni = AGL2UV.get(name)
                if expectedUni != uni:
                    self.fail("The Unicode value for {} may not be correct.".format(name))

            # look for duplicates
            if uni is not None:
                duplicates = []
                for name in sorted(font.keys()):
                    if name == glyph.name:
                        continue
                    other = font[name]
                    if other.unicode == uni:
                        duplicates.append(name)

                if duplicates:
                    self.fail("The Unicode for {0} is also used by: {1}.".format(glyph.name, " ".join(duplicates)))
