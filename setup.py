from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="abandoned_property_restoration",
    version="1.0.0",
    description="Application for identifying, restoring, preserving, and managing abandoned properties",
    author="Abandoned Property Restoration Team",
    packages=find_packages(include=["abandoned_property_restoration*"]),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.10",
)
