import setuptools

with open('README.md', mode='r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()


setuptools.setup(
    name="git_index_parser",
    version="1.0.0",
    author="Florian Wahl",
    author_email="florian.wahl.developer@gmail.com",
    description="A package to parse the index file of a git repository",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wahlflo/GitIndexFileParser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
