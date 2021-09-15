import sys

import setuptools

if sys.version_info < (3, 8):
    raise RuntimeError("bolsa requires Python 3.8+")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bolsa",
    version="0.1.0",
    packages=setuptools.find_packages(),
    python_requires=">=3.8.*",
    author="MuriloScarpaSitonio",
    author_email="muriloscarpa@gmail.com",
    description=(
        "Biblioteca em python para obtenção de seus dados de investimentos "
        "na bolsa de valores (B3/CEI)."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MuriloScarpaSitonio/python-cei-crawler",
    install_requires=["aiohttp==3.7.4", "beautifulsoup4==4.10.0"],
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ],
)
