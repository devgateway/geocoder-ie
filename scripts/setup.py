from setuptools import setup, find_packages
#todo add nltk download
setup(
    name='autogeocoder',
    version='1.0',
    description='Awesome auto geocode tool',
    author='Sebastian Dimunzio',
    author_email='sdimunzio@developmentgateway.org',
    package_dir={'': 'src'},
    packages=find_packages(),
    install_requires=[
        'nltk',
        'psycopg2'
    ])
