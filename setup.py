from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='prisma',
      version=version,
      description="Prisma is a Python debugger that produces UML diagrams by inspecting running programs.",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='prisma  uml agil',
      author='Gustavo Rezende',
      author_email='nsigustavo@gmail.com',
      url='nsigustavo.blogspot.com',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      package_data={'':['*.pic']},
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

