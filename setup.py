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
from setuptools import setup, Extension
from setuptools.command.test import test as TestCommand
import glob
import os
import sys
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


class get_pybind_include(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11

        return pybind11.get_include(self.user)


cmdclass = versioneer.get_cmdclass()
cmdclass.update({"test": PyTest})

libpyhector = Extension(
    "pyhector._binding",
    language="c++",
    include_dirs=[
        "include",
        "hector/headers",
        get_pybind_include(),
        get_pybind_include(user=True),
    ],
    libraries=["m", "boost_system", "boost_filesystem"],
    extra_compile_args=["-std=c++11"],
    sources=list(
        glob.glob("src/*.cpp")
        + glob.glob("hector/source/core/*.cpp")
        + glob.glob("hector/source/models/*.cpp")
        + glob.glob("hector/source/components/*.cpp")
        + glob.glob("hector/source/data/*.cpp")
    ),
    depends=list(glob.glob("include/*.h") + glob.glob("hector/headers/**/*.hpp")),
)

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
    author_email="sven.willner@pik-potsdam.de, robert.gieseke@pik-potsdam.de",
    license="GNU Affero General Public License v3",
    platforms="any",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="climate model climate change",
    package_data={"pyhector": ["rcp_default.ini", "emissions/*"]},
    include_package_data=True,
    packages=["pyhector"],
    install_requires=["numpy", "pandas", "pybind11>=2.2"],
    tests_require=["pytest>=4.0", "pytest-cov"],
    ext_modules=[libpyhector],
    zip_safe=False,
)
