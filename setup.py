from setuptools import setup, find_packages

with open("requirements.txt") as file:
    requirements = file.read().splitlines()

setup(
    name="NPG",
    version="0.0",
    packeges = find_packages(),
    install_requires=requirements,
)

