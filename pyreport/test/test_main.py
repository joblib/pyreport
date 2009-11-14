"""
Unit tests for pyreports main functionnality.
"""

# Standard library imports
import pydoc
from cStringIO import StringIO as S
import unittest

from nose.tools import assert_equal

from pyreport import main
from pyreport.code_hasher import xreadlines


##############################################################################
def test_check_rst_block():
    assert_equal(main.check_rst_block(['textBlock','foo']),
                       ['rstBlock', 'foo'])
    assert_equal(main.check_rst_block(['textBlock','*fo**o']),
                        ['textBlock', '*fo**o'])



##############################################################################
class TestMain(unittest.TestCase):

    def setUp(self):
        self.outString = S()

    def test_empty_file(self):
        main.main(xreadlines(""), 
                overrides={'outfile':self.outString, 'outtype':'rst',
                            'quiet':True}),
        self.assertEqual(self.outString.getvalue(),
                '.. header:: Compiled with pyreport\n\n\n\n')

    def test_hello_world(self):
        main.main(xreadlines("print 'hello world'"), 
                overrides={'outfile':self.outString, 'outtype':'rst',
                            'quiet':True, 'noecho':True }),
        self.assertEqual(self.outString.getvalue(),
            ".. header:: Compiled with pyreport\n\n\n::\n\n    print 'hello world'\n    \n\n.. class:: answer\n\n  ::\n\n    hello world\n    \n    \n\n")


##############################################################################
def profile():
    """ Use hotshot to profile the calls to main """
    import hotshot, cStringIO
    Prof = hotshot.Profile("pyreport.stats")
    outString=cStringIO.StringIO()
    Prof.runcall(main.main,cStringIO.StringIO(""),
                    overrides={'outfile':outString, 'outtype':'rst'})
    import hotshot.stats
    stats = hotshot.stats.load("pyreport.stats")
    stats.print_stats(50)


def document():
    """ Use pydoc to generate documentation"""
    pydoc.writedoc('pyreport')


##############################################################################
if __name__ == '__main__':
    from nose import runmodule
    runmodule()
    document()
    #profile()
   
