"""
pyhector
--------

Python wrapper for the `Hector simple climate model
<https://github.com/JGCRI/hector>`_.

**Install** using ::

    pip install pyhector

Find **usage** instructions in the `repository
<https://github.com/openclimatedata/pyhector>`_.

"""

import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

from pybind11.setup_helpers import Pybind11Extension

import versioneer

path = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        sys.exit(pytest.main(self.test_args))


cmdclass = versioneer.get_cmdclass()
cmdclass.update({"test": PyTest})

ext_modules = [
    Pybind11Extension(
        "pyhector._binding",
        [
            "hector/src/bc_component.cpp",
            "hector/src/carbon-cycle-model.cpp",
            "hector/src/carbon-cycle-solver.cpp",
            "hector/src/ch4_component.cpp",
            "hector/src/core.cpp",
            "hector/src/csv_outputstream_visitor.cpp",
            "hector/src/csv_table_reader.cpp",
            "hector/src/csv_tracking_visitor.cpp",
            "hector/src/dependency_finder.cpp",
            "hector/src/dummy_model_component.cpp",
            "hector/src/forcing_component.cpp",
            "hector/src/halocarbon_component.cpp",
            "hector/src/h_interpolator.cpp",
            # "hector/src/h_reader.cpp",
            "hector/src/h_util.cpp",
            # "hector/src/INIReader.cpp",
            # "hector/src/ini_to_core_reader.cpp",
            "hector/src/logger.cpp",
            # "hector/src/main.cpp",
            "hector/src/n2o_component.cpp",
            "hector/src/nh3_component.cpp",
            "hector/src/o3_component.cpp",
            "hector/src/oc_component.cpp",
            "hector/src/oceanbox.cpp",
            "hector/src/ocean_component.cpp",
            "hector/src/ocean_csys.cpp",
            "hector/src/oh_component.cpp",
            # "hector/src/rcpp_constants.cpp",
            # "hector/src/RcppExports.cpp",
            # "hector/src/rcpp_hector.cpp",
            "hector/src/simpleNbox.cpp",
            "hector/src/simpleNbox-runtime.cpp",
            "hector/src/slr_component.cpp",
            "hector/src/so2_component.cpp",
            "hector/src/spline_forsythe.cpp",
            "hector/src/temperature_component.cpp",
            "hector/src/unitval.cpp",
            "src/Hector.cpp",
            "src/main.cpp",
            "src/Observable.cpp",
        ],
        include_dirs=[
            "include",
            "hector/inst/include",
        ],
        cxx_std="17",
    )
]

with open(os.path.join(path, "README.rst"), "r") as f:
    readme = f.read()

setup(
    name="pyhector",
    version=versioneer.get_version(),
    cmdclass=cmdclass,
    description="Python wrapper for the Hector simple climate model",
    long_description=readme,
    long_description_content_type="text/x-rst",
    url="https://github.com/openclimatedata/pyhector",
    author="Sven Willner, Robert Gieseke",
    author_email="sven.willner@pik-potsdam.de, rob.g@web.de",
    license="GNU Affero General Public License v3",
    platforms="any",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="climate model climate change",
    package_data={"pyhector": ["rcp_default.ini", "emissions/*"]},
    include_package_data=True,
    packages=["pyhector"],
    extras_require={
        "docs": ["sphinx>=1.8", "sphinx_rtd_theme"],
        "tests": ["codecov", "pytest", "pytest-cov"],
    },
    setup_requires=["pybind11>=2.2"],
    install_requires=["numpy", "pandas", "pyarrow", "pybind11>=2.2"],
    tests_require=["pytest>=4.0", "pytest-cov"],
    ext_modules=ext_modules,
    zip_safe=False,
)
