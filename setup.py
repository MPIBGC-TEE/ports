#!/usr/bin/env python3
# vim:set ff=unix expandtab ts=4 sw=4:

from setuptools import setup,find_packages
def readme():
    with open('README.md') as f:
        return f.read()
    
setup(name='ports',
        version='0.1',
        #test_suite="example_package.tests",#http://pythonhosted.org/setuptools/setuptools.html#test
        description='Common reference for forwarded ports on antakya and matagorda',
        long_description=readme(),#avoid duplication 
        author='Markus',
        author_email='markus.mueller.1.g@gmail.com',
        url='https://github.com/MPIBGC-TEE/ports.git',
        packages=find_packages('src'), #find all packages (multifile modules) recursively
        package_dir={'': 'src'},
        #py_modules=['external_module'], # external_module.py is a module living outside this dir as an example how to iclude something not 
        classifiers = [
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: matagorda/antakya users",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Education "
        ],
        entry_points={
        'console_scripts': [
                'jupyter_forwarding=ports.client_helpers:jupyter_forwarding',
                ]
        },
        install_requires=[],
        include_package_data=True,
        #zip_safe=False
     )

 
 
 
