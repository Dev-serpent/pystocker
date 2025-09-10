from setuptools import setup, find_packages

setup(
    name='pystocker',
    version='0.1.0',
    description='Lightweight Moneycontrol stock data fetcher and analyzer',
    author='You',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pandas',
        'matplotlib',
        'numpy'
    ],
    python_requires='>=3.8'
)
