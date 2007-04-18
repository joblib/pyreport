"""
Defines the unit tests for the code hasher.
"""
import code_hasher as C
import unittest
import StringIO

testsuite = unittest.TestSuite()
testloader = unittest.TestLoader()
load_test = lambda t: testsuite.addTest(
               testloader.loadTestsFromTestCase(t))

def xreadlines(s):
    if not s or not s[-1]=="\n":
        s += "\n"
    return (line for line in StringIO.StringIO(s))

def block_signature(code_block):
    return (code_block.string, code_block.end_row)

def block_list_signature(block_list):
    return [block_signature(block) for block in block_list]

class TestCodeHasher(unittest.TestCase):

    def is_single_block(self, string):
        codeblock = C.CodeBlock(0)
        codeblock.string = ''.join(xreadlines(string))
        block_list = list( C.iterblocks(xreadlines(string)) )
        self.assertEqual(block_list_signature([codeblock]), 
                         block_list_signature(block_list))

    def test_empty(self):
        self.is_single_block("a")
    
    def test_comment_in_block(self):
        self.is_single_block("""
if 1:
    print "a"
    # foo

# foo

    print "b"
""")

    def test_double_blank_line(self):
        self.is_single_block("""
if 1:
    a = (1, 
           4)
                        

    a""")


    def test_indented_comment(self):
        self.is_single_block("""
if 1:

    # Comment

    a""")

    def test_decorator(self):
        self.is_single_block("@staticmethod\ndef foo()")

load_test(TestCodeHasher)

if __name__ == "__main__" :
    unittest.TextTestRunner().run(testsuite)

################"
#
#c = C.CodeHasher()
#f = file('plot.py')
#c.yield_rawlines = f.xreadlines()
#for t in c.yield_tokens():
#    print t
#
#c = C.CodeHasher()
#f = file('plot.py')
#c.yield_rawlines = f.xreadlines()
#for l in c.yield_codelines():
#    print repr(l.string), l.is_new_block()
#
#print '___________'
#
#c = C.CodeHasher()
#f = file('plot.py')
#c.yield_rawlines = f.xreadlines()
#for b in c.yield_codeblocks():
#    print repr(b.string)
#

