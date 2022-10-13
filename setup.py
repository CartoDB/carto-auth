from os.path import join
from setuptools import find_packages, setup

version_ns = {}
with open(join("carto_auth", "_version.py")) as f:
    exec(f.read(), {}, version_ns)

setup(
    name="carto-auth",
    version=version_ns["__version__"],
    description="Python library to authenticate with CARTO",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords=["carto", "auth", "oauth", "carto-dw", "bigquery"],
    author="CARTO",
    author_email="jarroyo@carto.com",
    url="https://github.com/cartodb/carto-auth",
    license="BSD 3-Clause",
    packages=find_packages(exclude=["examples", "tests"]),
    python_requires=">=3.7",
    install_requires=[
        "requests",
    ],
    extras_require={"carto-dw": ["google-auth", "google-cloud-bigquery>=2.34.4"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    zip_safe=False,
)
