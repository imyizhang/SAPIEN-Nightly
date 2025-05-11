import sys

from setuptools import setup

version_tag = f"cp{sys.version_info.major}{sys.version_info.minor}"

wheel_url = (
    f"https://github.com/haosulab/SAPIEN/releases/download/nightly/"
    f"sapien-3.0.0.dev20250303+291f6a77-{version_tag}-{version_tag}-macosx_12_0_universal2.whl"
)


setup(
    name="sapien-nightly",
    version="0.0.1",
    description="Installer for SAPIEN Nightly Release",
    readme="README.md",
    license="MIT",
    author="Yi Zhang",
    author_email="yizhang.dev@gmail.com",
    platforms=["macOS"],
    python_requires=">=3.10",
    install_requires=[f"sapien @ {wheel_url}"],
    # packages=["sapien_nightly"],
    # entry_points={
    #     "console_scripts": [
    #         "sapien-nightly=sapien_nightly.__main__:main",
    #     ],
    # },
)
