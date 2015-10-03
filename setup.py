from setuptools import setup

def readme():
    with open('README.rst') as readme_file:
        return readme_file.read()

configuration = {
    'name' : 'hypergraph',
    'version' : '0.1',
    'description' : 'Hypergraph tools and algorithms',
    'long_description' : readme(),
    'classifiers' : [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    'keywords' : 'hypergraph graph network community pomset',
    'url' : 'http://github.com/lmcinnes/hdbscan',
    'maintainer' : 'Leland McInnes',
    'maintainer_email' : 'leland.mcinnes@gmail.com',
    'license' : 'BSD',
    'packages' : ['hdbscan'],
    'install_requires' : ['numpy>=1.5],
    'ext_modules' : [],
    'cmdclass' : {'build_ext' : build_ext},
    'test_suite' : 'nose.collector',
    'tests_require' : ['nose'],
    }

setup(**configuration)
