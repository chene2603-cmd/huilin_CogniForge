#!/usr/bin/env python3
"""兼容性 setup 文件，主配置在 pyproject.toml"""

from setuptools import setup

# 读取版本
with open("VERSION", "r", encoding="utf-8") as f:
    VERSION = f.read().strip()

# 简单读取依赖
def get_requirements():
    try:
        with open("requirements-minimal.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return []

if __name__ == "__main__":
    setup(
        name="coastal-console",
        version=VERSION,
        packages=["coastal"],
        install_requires=get_requirements(),
    )