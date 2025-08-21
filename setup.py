from setuptools import setup, find_packages

try:
    with open("README.md", "r", encoding="utf-8") as f:
        md_description = f.read()
except IOError:
    md_description = ""

setup(
    name="web",
    version="0.1",
    description="A pythonic HTML & CSS engine",
    long_description=md_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LOLIPO1233PI/",
    author="VOID",
    author_email="gttyeio@gmail.com",
    project_urls={"Source": "https://github.com/LOLIPO1233PI/web"},
    packages=find_packages(),
)
