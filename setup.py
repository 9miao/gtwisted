from setuptools import setup, find_packages
import sys, os

version = '0.2.0'

setup(name='gtwisted',
      version=version,
      description="Achieve twisted based on gevent",
      long_description="""Achieve twisted based on gevent""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='gevent twisted pb',
      author='lanjinmin',
      author_email='zhuiming.mu@gmail.com',
      url='http://www.9miao.com/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	  scripts = [],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
		  "twisted",
		  "gevent",
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
