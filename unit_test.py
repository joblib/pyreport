#!/usr/bin/env python
# Small script to unit test pyreport !! One day this soft will be rock solid.
import pyreport

import unittest, doctest
import cStringIO
import pydoc

testsuite = unittest.TestSuite()
testloader = unittest.TestLoader()
load_test = lambda t: testsuite.addTest(
               testloader.loadTestsFromTestCase(t))

class TestOptionParsing(unittest.TestCase):

    def test_parse_options(self):
        self.assertEqual( pyreport.parse_options([]), ({}, []) )
        self.assertEqual( pyreport.parse_options(['foo']), ({}, ['foo']) )
        self.assertEqual( pyreport.parse_options(['-t','foo']), 
                                ({'outtype': 'foo'}, []) )

load_test(TestOptionParsing)

class TestCondenser(unittest.TestCase):

    def setUp(self):
        self.block_list =  [["foo\n", 0], 
                            [" bar\n", 1], 
                            ["#comment\n", 2],
                            ["\n baz\n", 3],
                            ["new statement\n",4],
                            ]

    def test_pop_statement(self):
        " Test pop_statement two times, to check it does indeed pop."
        self.assertEqual( pyreport.pop_statement_block(self.block_list),
                ['new statement\n\n baz\n#comment\n bar\n', 4])
        self.assertEqual( pyreport.pop_statement_block(self.block_list),
                ["foo\n", 0])

    def test_condense_block(self):
        self.assertEqual( pyreport.condense_blocks(self.block_list),
                [["foo\n bar\n#comment\n\n baz\n", 0], ["new statement\n", 4]])

load_test(TestCondenser)

class TestParser(unittest.TestCase):

    def test_code2blocks_empty(self):
        # First with an empty file: 
        self.assertEqual( pyreport.code2blocks(cStringIO.StringIO(), 
                                    pyreport.default_options), ([["", 1]], {}))

    def test_code2blocks_1(self):
        testfile = cStringIO.StringIO("""
if 1:
    print "a"
    # foo

# foo

    print "b"
""") 

        self.assertEqual( pyreport.code2blocks(testfile, 
            pyreport.default_options), 
            ([['\nif 1:\n    print "a"\n    # foo\n\n# foo\n\n    print "b"\n',
            1]], {} ))

    def test_code2blocks_2(self):
        testfile = cStringIO.StringIO("""print 1
print 2

# 

print 3
""") 

        self.assertEqual( pyreport.code2blocks(testfile, 
            pyreport.default_options), ([['print 1\n', 1], ['print 2\n\n# \n\n',
            2], ['print 3\n', 6]], {})
            )

load_test(TestParser)

class TestRstCompiler(unittest.TestCase):

    def test_check_rst_block(self):
        self.assertEqual(pyreport.check_rst_block(['textBlock','foo']),
                            ['rstBlock', 'foo'])
        self.assertEqual(pyreport.check_rst_block(['textBlock','*fo**o']),
                            ['textBlock', '*fo**o'])

load_test(TestRstCompiler)

class TestMain(unittest.TestCase):

    def setUp(self):
        self.outString = cStringIO.StringIO()

    def test_empty_file(self):
        pyreport.main(cStringIO.StringIO(""), 
                overrides={'outfile':self.outString, 'outtype':'rst',
                            'quiet':True}),
        self.assertEqual(self.outString.getvalue(),
                '.. header:: Compiled with pyreport\n\n\n\n')

    def test_hello_world(self):
        pyreport.main(cStringIO.StringIO("print 'hello world'"), 
                overrides={'outfile':self.outString, 'outtype':'rst',
                            'quiet':True, 'noecho':True }),
        self.assertEqual(self.outString.getvalue(),
                ".. header:: Compiled with pyreport\n\n\n::\n\n    print 'hello world'\n\n.. class:: answer\n\n  ::\n\n    hello world\n    \n    \n\n")

load_test(TestMain)

# Now add the doctest tests:
testsuite.addTest(doctest.DocTestSuite(pyreport))
doctest.DocTestSuite(pyreport)

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
    profile()
   
