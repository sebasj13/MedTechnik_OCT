import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="medizintechnik_oct",
    version="1.0.2",
    author="Sebastian Schäfer",
    author_email="sebastian.schaefer@student.uni-halle.de",
    description="Steuersoftware zum Versuch 'OCT' im Medizintechnik-Praktikum der MLU Halle-Wittenberg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sebasj13/MedTechnik_OCT",
    project_urls={"Bug Tracker": "https://github.com/sebasj13/MedTechnik_OCT/issues",},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["Pillow", "pylablib", "pyusb", "matplotlib", "numpy", "tqdm"],
    packages=[
        "medizintechnik_oct",
        "medizintechnik_oct.src",
        "medizintechnik_oct.src.classes",
    ],
    scripts=["medizintechnik_oct/OCT_GUI.py"],
    entry_points={"console_scripts": ["oct_gui=medizintechnik_oct.OCT_GUI:run"],},
    keywords=["MLU", "Medizintechnik", "OCT", "Oszilloskop"],
    python_requires=">=3.8",
)
