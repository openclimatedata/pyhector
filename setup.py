from setuptools import setup, Extension
import glob

libpyhector = Extension(
    'libpyhector',
    include_dirs = [
        'hector-wrapper/include',
        'hector-wrapper/hector/headers'
    ],
    libraries = ['m', 'boost_system', 'boost_filesystem'],
    extra_compile_args=['-std=c++0x'],
    sources = [
        'src/main.cpp',
        'hector-wrapper/src/HectorWrapper.cpp',
    ] + glob.glob('hector-wrapper/hector/source/core/*.cpp')
    + glob.glob('hector-wrapper/hector/source/models/*.cpp')
    + glob.glob('hector-wrapper/hector/source/components/*.cpp')
    + glob.glob('hector-wrapper/hector/source/data/*.cpp')
)

setup(
    name='pyhector',
    version='0.1.0',
    description='Python-wrapper for the Hector model (https://github.com/JGCRI/hector)',
    url='https://github.com/swillner/pyhector',
    author='Sven Willner, Robert Gieseke',
    author_email='sven.willner@pik-potsdam.de, robert.gieseke@pik-potsdam.de',
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
    packages=['pyhector'],
    install_requires=['pandas', 'numpy', 'pytest'],
    ext_modules=[libpyhector]
)
