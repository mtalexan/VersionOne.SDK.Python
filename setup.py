# To upload to PyPi, find the directions here https://packaging.python.org/tutorials/packaging-projects/


import sys
from setuptools import setup

install_requires = [
    'future',
    'testtools',
    'unittest2'
]

if (sys.version_info < (3,0)):
    # has a different name if supporting Python3
    install_requires.append('python-ntlm')
    install_requires.append("repoze.lru")
else:
    install_requires.append('python-ntlm3')

# get our long description from the README.md
with open("README.md", "r") as f:
    long_description = f.read()

setup(
  name = "v1pysdk",
  version = "0.6.2",
  description = "VersionOne API client",
  author = "Joe Koberg (VersionOne, Inc.)",
  author_email = "Joe.Koberg@versionone.com",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  license = "MIT/BSD",
  keywords = "versionone v1 api sdk",
  url = "http://github.com/mtalexan/VersionOne.SDK.Python.git",
  project_urls={
      'Documentation': 'http://github.com/mtalexan/VersionOne.SDK.Python.git',
      'Source' : 'http://github.com/mtalexan/VersionOne.SDK.Python.git',
      'Tracker' : 'http://github.com/mtalexan/VersionOne.SDK.Python.git/issues',
      },

  packages = [
    'v1pysdk',
    ],
  include_package_data=True,
  install_requires = install_requires,

  classifiers=(
      "Development Status :: 4 - Beta",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: MIT License",
      "License :: OSI Approved :: BSD License",
      "Operating System :: OS Independent",
      "Programming Language :: Python :: 2",
      "Programming Language :: Python :: 2.7",
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.5",
      "Topic :: Software Development :: Bug Tracking",
      ),

  # it may work on others, but this is what has had basic testing
  python_requires='>=2.5, <4',

  tests_require = [
      'testtools',
      'repoze.lru',
      'unittest2' # so testtools tests are auto-discovered
  ],
  test_suite = "tests",
)
