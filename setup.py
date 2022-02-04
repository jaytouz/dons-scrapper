from setuptools import setup, find_packages


setup(
    name="quebec-donations-scrapper",
    version="0.0.1",
    python_requires=">=3.6",
    packages=find_packages(where='src', exclude=[
                           "tests", "*.tests", "*.tests.*", "tests.*"]),
    package_dir={'': 'scrapper'},
    install_requires=[
        "selenium>=4.0.0",
    ]
)
