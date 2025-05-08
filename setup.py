from setuptools import setup, find_packages

setup(
    name="virtual_devices_IOT",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flask",
        "paho-mqtt",
        "python-dotenv",
    ],
) 