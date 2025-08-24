from setuptools import setup, find_packages

try:
    with open("README.md", "r", encoding="utf-8") as f:
        md_description = f.read()
except IOError:
    md_description = ""

setup(
    name="webhtml",
    version="0.1.0",
    packages=find_packages(),
    description="A pythonic HTML & CSS engine",
    long_description=md_description,
    long_description_content_type="text/markdown",
    author="LOLIPO1233PI",
    author_email="gttyeio@gmail.com",
)
