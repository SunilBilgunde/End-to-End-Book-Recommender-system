from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f: 
    long_description = f.read()


## edit below variables as per your requirements - 
REPO_NAME = 'ML Based book recommendation system'
AUTHOR_USER_NAME = "Sunil Bilgunde"
SRC_REPO = "books-recommender"
LIST_OF_REQUIREMENTS = []


setup(
    name=SRC_REPO,
    version='0.0.1',
    author="Sunil Bilgunde",
    description="A small local packages for ML based books recommendations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SunilBilgunde/End-to-End-Book-Recommender-system",
    author_email="Sunilbilgunde1996@gmail.com",
    packages=find_packages(),
    license="MIT",
    python_requires=">=3.7",
    install_requires=LIST_OF_REQUIREMENTS
)