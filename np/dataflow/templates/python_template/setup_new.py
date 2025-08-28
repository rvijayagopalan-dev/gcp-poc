# setup.py
from setuptools import setup, find_packages

setup(
    name='pos_utils_new',
    version='0.1',
    packages=find_packages(),
    install_requires=['apache-beam[gcp]',
                      'pymysql',
                      'sqlalchemy',
                      'cloud-sql-python-connector[pymysql]']
)
