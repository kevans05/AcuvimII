import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="accuvimII_modbusTCP", # Replace with your own username
    version="0.0.1",
    author="Kyle Evans",
    author_email="evans.kyle@protonmail.com",
    description="A package to read a accuvimII threw modbusTCP",
    url="https://github.com/kevans05/AcuvimII_Python",
    project_urls={
        "Bug Tracker": "https://github.com/kevans05/AcuvimII_Python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["pyModbusTCP","datetime"],
    package_data={'modbusmap' : ['map.json']}
)

