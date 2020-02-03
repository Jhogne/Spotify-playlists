from setuptools import setup, find_packages
setup(
    name="splist",
    version="0.1",
    packages=find_packages('splist'),
    entry_points = {
    'console_scripts': [
        'splist = splist.main:main'
    ]}
)