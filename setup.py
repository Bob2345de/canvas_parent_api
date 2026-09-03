import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="canvas_parent_api",
    version="0.0.26",
    author="Jacob Schwartz",
    author_email="jake@schwartzpub.com",
    description="",
    zip_safe = False,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/schwartzpub/canvas_parent_api",
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