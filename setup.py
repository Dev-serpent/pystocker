from setuptools import setup, find_packages

setup(
    name="pystocker",
    version="0.1.0",
    author="Wakanda Gamasis - Dev Serpent Team DIV-A",
    author_email="devserpent.org@gmail.com",
    description="A stock data mining and analysis library (Moneycontrol scraper)",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Dev-serpent/pystocker",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "pandas",
        "matplotlib",
        "mplfinance",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
