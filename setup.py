from setuptools import setup, find_namespace_packages

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

with open("VERSION", "r", encoding="utf-8") as version_file:
    version = version_file.read()

setup(
    name="CatDataSchema",
    version=version,
    author="Emma Li",
    description="A package facilitating the extraction, transformation, and loading of cat litterbox time data into the database.",
    url="https://github.com/emma-jinger/CatWatcher/tree/main/CatDataSchema",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(include=["CatDataSchema", "CatDataSchema.*"]),
    include_package_data=True,
    install_requires=open("requirements.txt", encoding="utf-8").read().splitlines(),
    entry_points={
        "console_scripts": [
            "cat_data_watcher=CatDataSchema.cli:cat_data_watcher",
            "cat_data_migrate=CatDataSchema.cli:migrate",
        ]
    },
    package_data={"CatDataSchema": []},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Database",
    ],
)
