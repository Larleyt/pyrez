from setuptools import setup, find_packages

setup(
  name='pyrez',
  version='0.0.1',
  packages=find_packages(),
  install_requires=[
    'Click',
    'sqlalchemy'
  ],
  entry_points='''
    [console_scripts]
    pyrez=pyrez:cli
  ''',
  url="https://songbee.net/",
  license="GPL",
  author="Ale",
  author_email="ale@songbee.net",
)