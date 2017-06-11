from setuptools import setup, find_packages

version = '0.1.0'

setup(
    name="helga-whodat",
    version=version,
    description=('who dat?'),
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='irc bot whodat',
    author='Justin Caratzas',
    author_email='bigjust@lambdaphil.es',
    license='LICENSE',
    packages=find_packages(),
    include_package_data=True,
    install_requires = (
        'boto3==1.4.4',
        'requests',
    ),
    py_modules=['helga_whodat'],
    zip_safe=True,
    entry_points = dict(
        helga_plugins = [
            'whodat = helga_whodat:whodat',
        ],
    ),
)
