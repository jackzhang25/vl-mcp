#!/usr/bin/env python3
"""
Setup script for Visual Layer MCP Server
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        requirements = [
            line.strip() for line in f if line.strip() and not line.startswith("#")
        ]

setup(
    name="visual-layer-mcp-server",
    version="1.0.2,
    author="Visual Layer",
    author_email="support@visual-layer.com",
    description="MCP Server for Visual Layer SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/visual-layer/vl-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "visual-layer-mcp=mcp_server.server:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
