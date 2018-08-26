from setuptools import setup, find_packages

setup(
    name="bds_test_tool",
    version="0.0.1",
    author="Ihor Peresunko",
    author_email="ihor.peresunko@genesys.com",
    description="A tool for easy testing the Billing Data Server",
    url="https://gitlab.com/curious22/tools",
    packages=find_packages(exclude=['*.tests.*', 'file-fixtures']),
    include_package_data=True,
    entry_points={
        'console_scripts': ['btt=bds_test_tool.main:main'],
    },
    install_requires=['fire>=0.1.3'],
)
