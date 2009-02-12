#!/usr/bin/env python

from distutils.core import setup
import sys

import pyreport


# For some commands, use setuptools
if len(set(('develop', 'sdist', 'release', 'bdist_egg', 'bdist_rpm',
           'bdist', 'bdist_dumb', 'bdist_wininst', 'install_egg_info',
           'build_sphinx', 'egg_info', 'easy_install',
            )).intersection(sys.argv)) > 0:
    from setupegg import extra_setuptools_args

# extra_setuptools_args is injected by the setupegg.py script, for
# running the setup with setuptools.
if not 'extra_setuptools_args' in globals():
    extra_setuptools_args = dict()


setup(name='pyreport',
      version=pyreport.__version__,
      summary='generates notes from a python script',
      author=pyreport.__author__,
      author_email='gael.varoquaux@normalesup.org',
      url='http://gael-varoquaux.info/computers/pyreport/',
      description="""
Pyreport makes notes out of a python script. It can run the script in a sandbox and capture its output. It allows for embedding RestructuredText or LaTeX comments in the code for literate programming and generates a report made of the literate comments, the code, pretty printed, and the output of the script (pyreport can capture pylab figures). This is useful for documentations, making tutorials, but also for sharing python-based calculations with colleagues.
""",
      license=pyreport.__license__,
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Education',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering',
          'Topic :: Utilities',
      ],
      platforms='any',
#      package_data={'pyreport': ['pyreport/examples/*'],},
      packages=['pyreport'],
      **extra_setuptools_args)

