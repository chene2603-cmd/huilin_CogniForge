from setuptools import setup, find_packages

setup(
    name="coastal-console",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "coastal=coastal.cli:main",
        ]
    },
)