#!/usr/bin/env python
"""Wrapper to run setup.py using setuptools."""

import setuptools

################################################################################
# Call the setup.py script, injecting the setuptools-specific arguments.

extra_setuptools_args = dict(
                tests_require=['nose', 'coverage'],
                test_suite='nose.collector',
                zip_safe=False,
                entry_points = {
                    'console_scripts': [
                            'pyreport = pyreport.pyreport:commandline_call',
                        ],
                    }
                )

if __name__ == '__main__':
    execfile('setup.py', dict(__name__='__main__', 
                          extra_setuptools_args=extra_setuptools_args))


