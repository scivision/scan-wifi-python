#!/usr/bin/env python
install_requires = ['pandas','requests']
tests_require = ['nose','coveralls']
# %%
from setuptools import setup,find_packages

setup(name='mozilla-location-python',
      packages=find_packages(),
      author='Michael Hirsch, Ph.D.',
      url='https://github.com/scivision/mozilla-location-python',
      long_description=open('README.md').read(),
      description='Using Mozilla Location services, log location vs. time using WiFi or convert to KML.',
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'tests':tests_require,
                      'kml':['simplekml']},
      python_requires='>=3.6',
	  )

