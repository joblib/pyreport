#!/usr/bin/env python
# Small script to unit test pyreport !! One day this soft will be rock solid.
import pyreport
import options

import unittest, doctest
import pydoc
from cStringIO import StringIO as S
from code_hasher import xreadlines

testsuite = unittest.TestSuite()
testloader = unittest.TestLoader()
load_test = lambda t: testsuite.addTest(
               testloader.loadTestsFromTestCase(t))

##############################################################################
class TestOptionParsing(unittest.TestCase):

    def test_parse_options(self):
        self.assertEqual( pyreport.parse_options([]), ({}, []) )
        self.assertEqual( pyreport.parse_options(['foo']), ({}, ['foo']) )
        self.assertEqual( pyreport.parse_options(['-t','foo']), 
                                ({'outtype': 'foo'}, []) )

load_test(TestOptionParsing)

##############################################################################
class TestRstCompiler(unittest.TestCase):

    def test_check_rst_block(self):
        self.assertEqual(pyreport.check_rst_block(['textBlock','foo']),
                            ['rstBlock', 'foo'])
        self.assertEqual(pyreport.check_rst_block(['textBlock','*fo**o']),
                            ['textBlock', '*fo**o'])

load_test(TestRstCompiler)

##############################################################################
class TestMain(unittest.TestCase):

    def setUp(self):
        self.outString = S()

    def test_empty_file(self):
        pyreport.main(xreadlines(""), 
                overrides={'outfile':self.outString, 'outtype':'rst',
                            'quiet':True}),
        self.assertEqual(self.outString.getvalue(),
                '.. header:: Compiled with pyreport\n\n\n\n')

    def test_hello_world(self):
        pyreport.main(xreadlines("print 'hello world'"), 
                overrides={'outfile':self.outString, 'outtype':'rst',
                            'quiet':True, 'noecho':True }),
        self.assertEqual(self.outString.getvalue(),
            ".. header:: Compiled with pyreport\n\n\n::\n\n    print 'hello world'\n    \n\n.. class:: answer\n\n  ::\n\n    hello world\n    \n    \n\n")

load_test(TestMain)

# Add the sub module tests
testsuite.addTest( testloader.loadTestsFromName('test_code_hasher'))


# Now add the doctest tests:
testsuite.addTest(doctest.DocTestSuite(pyreport))
testsuite.addTest(doctest.DocTestSuite(options))

##############################################################################

runner = unittest.TextTestRunner()

def profile():
    """ Use hotshot to profile the calls to main """
    import hotshot
    Prof = hotshot.Profile("pyreport.stats")
    outString=cStringIO.StringIO()
    Prof.runcall(pyreport.main,cStringIO.StringIO(""),
                    overrides={'outfile':outString, 'outtype':'rst'})
    import hotshot.stats
    stats = hotshot.stats.load("pyreport.stats")
    stats.print_stats(50)

def document():
    """ Use pydoc to generate documentation"""
    pydoc.writedoc('pyreport')


if __name__ == '__main__':
    #unittest.main()
    runner.run(testsuite)
    document()
    #profile()
   
