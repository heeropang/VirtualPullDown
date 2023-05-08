import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="virtualpulldown",
    version="0.0.1",
    author="Heewhan Shin",
    author_email="hshin40@gmail.com",
    description="A package for virtual pulldown",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/heeropang/VirtualPullDown/scripts",
    keywords = ['PDB', 'structure biology', 'protein', 'analysis', 'ColabFold', 'AlphaFold'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
