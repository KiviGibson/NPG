from setuptools import setup

with open("requirements.txt") as file:
    requirements = file.read().splitlines()

setup(
    name="NPG",
    version="0.1",
    packages=["NPG"],
    install_requires=requirements,
)
