from setuptools import setup, find_packages

setup(
    name='bike_share_analysis',
    version='0.1',
    author='Maximilian Schlund',
    license='MIT',
    packages=find_packages(['bike_share']),
    description='A collection of functions to analyze the Toronto bike share dataset.'
)