from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="GOandUISP",
    version="2024.11.3",
    description="Suite di utilities per GoAndSwim.",
    long_description=readme,
    author="Gregorio Berselli",
    url="https://github.com/Grufoony/GOandUISP",
    license=license,
    packages=find_packages(exclude=("test", "races")),
)
