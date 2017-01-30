from setuptools import setup, Extension
import glob

libpyhector = Extension(
    'libpyhector',
    include_dirs=[
        'hector-wrapper/include',
        'hector-wrapper/hector/headers'
    ],
    libraries=['m', 'boost_system', 'boost_filesystem'],
    extra_compile_args=['-std=c++0x'],
    sources=[
        'src/main.cpp',
        'hector-wrapper/src/HectorWrapper.cpp',
    ] + glob.glob('hector-wrapper/hector/source/core/*.cpp')
      + glob.glob('hector-wrapper/hector/source/models/*.cpp')
      + glob.glob('hector-wrapper/hector/source/components/*.cpp')
      + glob.glob('hector-wrapper/hector/source/data/*.cpp')
)

setup(
    name='pyhector',
    version='0.1.1',
    description='Python-wrapper for the Hector simple climate model',
    long_description=open('README.md').read(),
    url='https://github.com/swillner/pyhector',
    author='Sven Willner, Robert Gieseke',
    author_email='sven.willner@pik-potsdam.de, robert.gieseke@pik-potsdam.de',
    licence='GNU Affero General Public License v3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
        'Programming Language :: Python :: 3.6'
    ],
    keywords='',
    package_data={'pyhector': ['rcp_default.ini', 'emissions/*']},
    include_package_data=True,
    packages=['pyhector'],
    install_requires=['pandas', 'numpy', 'pytest'],
    ext_modules=[libpyhector]
)
