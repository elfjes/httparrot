from setuptools import setup, find_packages

setup(
    name="httparrot",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["tornado"],
    extras_require={"develop": ["pytest", "pytest-tornado"]},
    entry_points={"console_scripts": ["parrot=httparrot:main"]},
)
