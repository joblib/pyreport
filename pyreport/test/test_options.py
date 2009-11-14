"""
Unit tests for pyreport's options functionnality.
"""

from nose.tools import assert_equal

from pyreport import options

##############################################################################
def test_parse_options():
    assert_equal(options.parse_options([]), ({}, []) )
    assert_equal(options.parse_options(['foo']), ({}, ['foo']) )
    assert_equal(options.parse_options(['-t','foo']), 
                            ({'outtype': 'foo'}, []) )

  
