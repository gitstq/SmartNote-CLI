"""
Setup script for SmartNote-CLI
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smartnote-cli",
    version="1.0.0",
    author="SmartNote Team",
    author_email="smartnote@example.com",
    description="AI-Powered Smart Markdown Note Manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/SmartNote-CLI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Text Processing :: Markup",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
        "textual>=0.50.0",
        "markdown>=3.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "smartnote=smartnote.cli:main",
            "sn=smartnote.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
