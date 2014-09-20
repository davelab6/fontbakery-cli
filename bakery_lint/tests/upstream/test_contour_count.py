import robofab.world

from bakery_lint.base import BakeryTestCase


class TestContourCount(BakeryTestCase):

    targets = ['upstream']
    tool = 'lint'
    name = __name__

    def test_contour_count(self):
        """ In font there shouldn't be too many overlapping contours """
        font = robofab.world.OpenFont(self.operator.path)

        for glyphname in font.keys():

            glyph = font[glyphname]
            count = len(glyph)

            test = glyph.copy()
            test.removeOverlap()
            if count - len(test) > 2:
                msg = "{} has a unusally high number of overlapping contours."
                self.fail(msg.format(glyph.name))
