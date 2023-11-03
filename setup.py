# Source: https://packaging.python.org/guides/distributing-packages-using-setuptools/

from os import path
from setuptools import find_packages, setup


run_requirements = [
    "fastapi==0.104.0",
    "loguru==0.7.2",
    "urllib3==2.0.7",
    "uvicorn==0.23.2",
    "black==23.10.0",
    "gunicorn==21.2.0",
    "psycopg2-binary==2.9.9",
    "pydantic==2.4.2",
    "alembic==1.12.1",
    "python-dotenv==1.0.0",
    "pydantic-settings==2.0.3",
    "fastapi-pagination==0.12.12",
    "Sphinx==7.2.6",
]

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="Product Inventory Api",
    version="0.1.1",
    author="Kevin de Santana Araujo",
    author_email="kevin_santana.araujo@hotmail.com",
    packages=find_packages(exclude=["docs", "tests"]),
    url="https://github.com/kevinsantana/rather-labs-coding-challenge",
    description="REST Api for a product inventory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=run_requirements,
    python_requires=">=3.10.8",
)
