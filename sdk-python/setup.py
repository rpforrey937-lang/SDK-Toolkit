from setuptools import setup, find_packages

setup(
    name="agentic-sdk",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Agentic Commerce",
    description="SDK for enabling AI agents to perform secure autonomous purchases",
    long_description="Python client for interacting with the Agentic Commerce Gateway",
    python_requires=">=3.7",
)
