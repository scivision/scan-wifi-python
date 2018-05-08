#!/usr/bin/env python
install_requires = ['pandas','requests']
tests_require = ['nose','coveralls']
# %%
from setuptools import setup,find_packages

setup(name='mozilla-location-python',
      packages=find_packages(),
      author='Michael Hirsch, Ph.D.',
      version='0.5.1',
      url='https://github.com/scivision/mozilla-location-wifi-python',
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      description='Using Mozilla Location services, log location vs. time using WiFi or convert to KML.',
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'tests':tests_require,
                      'kml':['simplekml']},
      python_requires='>=3.6',
	  )

