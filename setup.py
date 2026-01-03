"""Setup script for open-python-skills."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="open-python-skills",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="CLI tool to install Python Backend Pro Max skill to AI assistants",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/agent_email",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "open-python-skills=open_python_skills.cli:main_entry",
        ],
    },
    install_requires=[],
)
