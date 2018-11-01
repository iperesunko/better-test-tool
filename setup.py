from setuptools import setup, find_packages

setup(
    name="better_test_tool",
    version="0.4",
    author="Ihor Peresunko",
    author_email="ihor.peresunko@genesys.com",
    description="A tool for better testing python projects",
    url="https://gitlab.com/curious22/tools",
    packages=find_packages(exclude=['tests', 'file-fixtures']),
    entry_points={
        'console_scripts': ['btt=better_test_tool.main:main'],
    })
