import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="canvas_parent_api",
    version="0.0.32",
    author="Me",
    description="",
    zip_safe = False,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=setuptools.find_packages(
        'src',
        exclude=['__pycache__','venv']
    ),
    package_dir={'':'src'},
    install_requires=[
        "aiohttp",
        "pydantic"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)