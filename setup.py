from setuptools import setup, find_namespace_packages

setup(
    name='exRates',
    version='1',
    url='http://github.com/dummy_user/useful',
    author='Roman Siusiailo',
    packages=find_namespace_packages(),
    include_package_data=True,
    install_requires=['aiohttp'],
    entry_points={'console_scripts': ['exRate = HW_M5.main:con_main']}
)