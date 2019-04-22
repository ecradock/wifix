from setuptools import setup, find_packages

setup(
    name="Wifi-x",
    version="0.0.1a",
    description="Exfiltrates data through the use of wifi beacons",
    author="Ed Cradock",
    license="MIT",
    packages=find_packages(),
    install_requires=["scapy"],
    entry_points={
        "console_scripts": [
            "wifix-send=wifix:send",
            "wifix-recv=wifix:recv"
        ]
    }
)
