from setuptools import setup, find_packages

setup(
    name="better_test_tool",
    version="0.5",
    author="Ihor Peresunko",
    author_email="ihor.peresunko@gmail.com",
    description="Utility for simple testing projects",
    url="https://github.com/iperesunko/better-test-tool",
    packages=find_packages(exclude=['tests', 'file-fixtures']),
    entry_points={
        'console_scripts': ['btt=better_test_tool.main:main'],
    },
    install_requires=['pyperclip'])
