from os.path import dirname, join
from setuptools import setup, find_packages

setup(
    name='udger-v4',
    version='5.0.1',
    license='BSD',
    author='The Udger Team',
    author_email='info@udger.com',
    description="Fast and reliable User Agent parser and IP classifier for Python",
    long_description_content_type='text/markdown',
    url='https://github.com/udger/udger-python-v4',
    packages=['udger'],
    platforms='any',
    zip_safe=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
    ],
)
