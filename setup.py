import setuptools

setuptools.setup(
    name="mnca_app",
    version="0.0.0",
    author="Kevin Duff",
    author_email="kduff@enthought.com",
    description="TODO",
    long_description="## TODO",
    long_description_content_type="text/markdown",
    url="https://github.com/k2bd/mnca",
    packages=setuptools.find_packages(),
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    #     "Development Status :: 3 - Alpha",
    #     "Intended Audience :: Developers",
    #     "Topic :: Software Development",
    # ],
    license="MIT",
    install_requires=["PyQt5==5.6.2", "pyface", "traits", "traitsui", "numpy", "scipy"],
    entry_points={'console_scripts': ['mnca_app = mnca_app.mnca_view:main']},
    python_requires='>=3.6',
)
