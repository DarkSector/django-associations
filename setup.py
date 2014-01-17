import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-associations',
    version='0.1.6',
    packages=['associations'],
    include_package_data=True,
    license='MIT License',  # example license
    description='A simple Django app to show url associations between installed apps.',
    long_description=README,
    install_requires = [
        'django >= 1.5',
    ],
    url='https://github.com/DarkSector/django-associations',
    author='Pronoy Chopra',
    author_email='contact@pronoy.in',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)