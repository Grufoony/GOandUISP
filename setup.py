"""
Setup file for the GOandUISP package.
"""

from setuptools import setup, find_packages


with open("README.md", encoding="utf-8") as f:
    readme_file = f.read()

with open("LICENSE", encoding="utf-8") as f:
    license_file = f.read()

setup(
    name="GOandUISP",
    version="2024.12.8",
    description="Suite di utilities per GoAndSwim.",
    long_description=readme_file,
    author="Gregorio Berselli",
    url="https://github.com/Grufoony/GOandUISP",
    license=license_file,
    packages=find_packages(exclude=("test", "races")),
)
