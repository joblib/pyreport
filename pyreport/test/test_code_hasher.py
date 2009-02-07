"""
Unit tests for the code hasher.
"""

from nose.tools import assert_equal

import pyreport.code_hasher as ch


def line_signature(line_object):
    return (line_object.string, line_object.end_row, line_object.options)


def line_list_signature(line_list):
    signature = [line_signature(line) for line in line_list]
    # This is unfortunately required because of a change in the token
    # module between python 2.4 and python 2.5
    if signature[-1][0] == '':
        signature.pop()
    return signature


########################################################################
# Test the separation in logical lines

def check_signature(in_string, signature):
    hasher = ch.CodeHasher(ch.xreadlines(in_string))
    code_line_list = [l for l in hasher.itercodelines()]
    signature2 = line_list_signature(code_line_list)
    assert_equal(signature, signature2)


def test_lines():
    check_signature('a\na', [('a\n', 1, {}), ('a\n', 2, {})])


def test_comments():
    check_signature('a\n#a\na', [('a\n', 1, {}), ('#a\na\n', 3, {})])


def test_options():
    check_signature('a\n#pyreport -n\na', 
                    [('a\n', 1, {}), ('#pyreport -n\na\n', 3, {})])


########################################################################
# Test the separation in code blocks

def is_single_block(string):
    codeblock = ch.CodeBlock(0)
    codeblock.string = ''.join(ch.xreadlines(string.expandtabs()))
    block_list = list( ch.iterblocks(ch.xreadlines(string)) )
    assert_equal(line_list_signature([codeblock]), 
                        line_list_signature(block_list))


def test_empty():
    is_single_block("a")


def test_comment_in_block():
    is_single_block("""
if 1:
    print "a"
    # foo

# foo

    print "b"
""")


def test_double_blank_line():
    is_single_block("""
if 1:
    a = (1, 
           4)
                        

    a""")


def test_indented_comment():
    is_single_block("""
if 1:

    # Comment

    a""")


def test_function_declaration():
    is_single_block("def foo():\n foo")


def test_tabbed_block():
    is_single_block("def foo():\n\tfoo")


def test_decorator():
    is_single_block("@staticmethod\ndef foo():\n foo")


def test_double_function():
    string = """
def f():
    pass

def g():
    pass
"""
    blocks = list(ch.iterblocks(ch.xreadlines(string)))
    # This should be made of three blocks, the last one of them
    # empty.
    assert_equal(len(blocks), 3)


def test_double_function_tabs():
    string = """
def f():
\tpass

def g():
\tpass
"""
    blocks = list(ch.iterblocks(ch.xreadlines(string)))
    # This should be made of three blocks, the last one of them
    # empty.
    assert_equal(len(blocks), 3)


def test_double_function_non_empty_line():
    string = """
def f():
\tpass
\t
def g():
\tpass
"""
    blocks = list(ch.iterblocks(ch.xreadlines(string)))
    # This should be made of three blocks, the last one of them
    # empty.
    assert_equal(len(blocks), 3)


########################################################################
# Test if the code is indeed kept similar by the hash

def is_same_code(codestring):
    out = ''.join([i.string
                for i in ch.iterblocks(ch.xreadlines(codestring))])
    assert_equal(codestring.expandtabs(), out)


def test_long_block():
    is_same_code("def f():\n\t1\n\t2\n")


########################################################################
if __name__ == "__main__" :
    import nose
    nose.runmodule()

