import pathlib
from setuptools import setup
from setuptools import find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="PyRCD",
    version="1.0",
    description="Structural Design and Optimization of Reinforced Concrete Element",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/TabishIzhar/PyRCD.git",
    author="Tabish Izhar",
    author_email="tizhar@iul.ac.in",
    license="MIT License",
    classifiers=[
        "Programming Language :: Python :: 3.10.7",
    ],
    # packages=["PyRCD"],
    packages=find_packages(include=['PyRCD', 'PyRCD.*']),
    # package_dir={'': 'src/PyRCD'},
    
    include_package_data=False,
    install_requires=["numpy", "pandas", "plotly"]
)