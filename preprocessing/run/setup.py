import setuptools

with open("README.md", "r") as f:
    long_description=f.read()

setuptools.setup(
    name="run",
    version="1.0.0",
    author="Heewhan",
    author_email="hshin40@gmail.com",
    description="preprocessing input files for multimer predictions using localcolabfold",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/heeropang/run",
    keywords=['Recombinase', 'prophage', 'alphafold'],
    packages=setuptools.find_packages(),
    classifiers=[
         "Programming Langguage :: Python :: 3",
         "License :: OSI Approved :: MIT Lincense",
         "Operating System :: OS",
    ],
    python_requires='>=3.6',
)
