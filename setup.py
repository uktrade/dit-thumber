import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-thumber',
    version='3.0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A Django app to solicit user feedback on various views/pages via a simple widget.',
    long_description=README,
    url='https://github.com/uktrade/dit-thumber',
    author='David Downes',
    author_email='david@downes.co.uk',
    test_suite='run_tests.run',
    install_requires=[
        'django>=1.11,<=4.2',
    ],
    extras_require={
        'test': [
            'setuptools>=45.2.0,<50.0.0',
            'twine==4.0.2',
            'wheel>=0.34.2,<1.0.0',
            'black==20.8b1',
            'blacken-docs==1.6.0',
            'isort==5.6.4',
            'flake8==3.8.4',
            'pre-commit-hooks==3.3.0',
            'six==1.16.0',
        ]
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
