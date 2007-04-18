"""
This module provides a CodeHasher object that groups raw code lines in
full code blocks ready for execution.
"""

import token
import tokenize
import re

from pyreport import parse_options


class Token(object):
    """ A token object"""

    def __init__(self, token_desc):
        """ Builds a token object from the output of
            tokenize.generate_tokens"""
        self.type = token.tok_name[token_desc[0]]
        self.content = token_desc[1]
        self.start_row = token_desc[2][0]
        self.start_col = token_desc[2][1]
        self.end_row = token_desc[3][0]
        self.end_col = token_desc[3][1]

    def __repr__(self):
        return str((self.type, self.content))


class CodeLine(object):
    """ An object representing a full logicial line of code """
    string = ""
    open_symbols = {'{':0, '(':0, '[':0}
    closing_symbols = {'}':'{', ')':'(', ']':'['} 
    brakets_balanced = True
    end_col = 0
    last_token_type = ""
    complete = False
    options = {}

    def __init__(self, start_row):
        self.start_row = start_row
        self.end_row = start_row
    
    def append(self, token):
        """ Appends a token to the line while keeping the integrity of
            the line, and checking if the logical line is complete.
        """
        # The token content does not include whitespace, so we need to pad it
        # adequately
        token_started_new_line = False
        if token.start_row > self.end_row:
            self.end_col = 0
            token_started_new_line = True
        self.string += (token.start_col - self.end_col) * " " + token.content
        self.end_row = token.end_row
        self.end_col = token.end_col
        self.last_token_type = token.type

        # Keep count of the open and closed brakets.
        if token.type == 'OP':
            if token.content in self.open_symbols:
                self.open_symbols[token.content] += 1
            elif token.content in self.closing_symbols:
                self.open_symbols[self.closing_symbols[token.content]] += -1
            self.brakets_balanced = ( self.open_symbols.values() == [0, 0, 0] ) 
        
        self.complete = ( self.brakets_balanced 
                          and ( token.type in ('NEWLINE', 'ENDMARKER')
                                or ( token_started_new_line
                                      and token.type == 'COMMENT' )
                              )
                        )
        if ( token.type == 'COMMENT' 
                    and token_started_new_line 
                    and token.content[:10] == "#pyreport " ):
            self.options.update(parse_options(line[10:].split(" "))[0])


    def isnewblock(self):
        """ This functions checks if the code line start a new block.
        """
        if re.match(r"\n*(elif|else|finally|except| |#)", self.string):
            return False
        else:
            return True        

    def __repr__(self):
        return repr(self.string)


class CodeBlock(object):
    """ Object that represents a full executable block """
    string = ""
    options = {}

    def __init__(self, start_row):
        self.start_row = start_row
        self.end_row = start_row

    def append(self, codeline):
        self.string += codeline.string
        self.options.update(codeline.options)

    def __repr__(self):
        return('<CodeBlock object, id %i, line %i, %s, options %s>'
                    % (id(self), self.start_row, repr(self.string),
                            repr(self.options) ) )


class CodeHasher(object):
    """ Implements a object that transforms a iterator of raw code lines
        in an iterator of code blocks.

        Input:
            self.xreadlines: iterator to raw lines of code, such as 
                                 file.xreadlines()

        Output: Generators :
            self.yieldcodeblocks
            self.yieldcodelines
            self.yieldtokens
    """

    def __init__(self, xreadlines):
        self.xreadlines = xreadlines

    def yieldcodeblocks(self):
        codeblock = CodeBlock(0)
        last_line_has_decorator = False
        for codeline in self.yieldcodelines():            
            if codeline.isnewblock() and not last_line_has_decorator :
                if codeblock.string:
                    yield codeblock
                codeblock = CodeBlock(codeline.start_row)
                codeblock.append(codeline)
                line_start = codeline.string.lstrip('\n')
                if line_start and line_start[0] == '@':
                        last_line_has_decorator = True
                        continue
                line_end = codeline.string.rstrip()
                if line_end and line_end == ':' : 
                    if codeblock.string:
                        yield codeblock
                    codeblock = CodeBlock(codeline.start_row)
            else:
                codeblock.append(codeline)
            last_line_has_decorator = False
        else:
            yield codeblock

    def yieldcodelines(self):
        codeline = CodeLine(0)
        for token in self.yieldtokens():
            codeline.append(token)
            if codeline.complete:
                yield codeline
                codeline = CodeLine(codeline.end_row + 1)
        if codeline.string:
            yield codeline

    def yieldtokens(self):
        for token_desc in tokenize.generate_tokens(self.xreadlines.next):
            yield Token(token_desc)


iterblocks = lambda xreadlines: CodeHasher(xreadlines).yieldcodeblocks()

