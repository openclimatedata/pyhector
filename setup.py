from setuptools import setup, Extension

libpyhector = Extension(
    'libpyhector',
    include_dirs = ['src/hector/headers'],
    libraries = ['m', 'boost_system', 'boost_filesystem'],
    sources = [
        'src/main.cpp',
        'src/hector/source/core/carbon-cycle-solver.cpp',
        'src/hector/source/core/core.cpp',
        'src/hector/source/core/logger.cpp',
        'src/hector/source/core/dependency_finder.cpp',
        'src/hector/source/models/carbon-cycle-model.cpp',
        'src/hector/source/models/simpleNbox.cpp',
        'src/hector/source/models/ocean_csys.cpp',
        'src/hector/source/models/oceanbox.cpp',
        'src/hector/source/components/n2o_component.cpp',
        'src/hector/source/components/slr_component.cpp',
        'src/hector/source/components/onelineocean_component.cpp',
        'src/hector/source/components/ocean_component.cpp',
        'src/hector/source/components/bc_component.cpp',
        'src/hector/source/components/oh_component.cpp',
        'src/hector/source/components/ch4_component.cpp',
        'src/hector/source/components/o3_component.cpp',
        'src/hector/source/components/dummy_model_component.cpp',
        'src/hector/source/components/oc_component.cpp',
        'src/hector/source/components/so2_component.cpp',
        'src/hector/source/components/halocarbon_component.cpp',
        'src/hector/source/components/forcing_component.cpp',
        'src/hector/source/components/temperature_component.cpp',
        'src/hector/source/visitors/csv_outputstream_visitor.cpp',
        'src/hector/source/visitors/csv_output_visitor.cpp',
        'src/hector/source/data/h_interpolator.cpp',
        'src/hector/source/data/unitval.cpp',
        'src/hector/source/data/spline_forsythe.cpp',
    ]
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
    install_requires=['pandas', 'numpy', 'configparser'],
    ext_modules=[libpyhector]
)
