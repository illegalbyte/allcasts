from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()
VERSION = '0.1.0'

setup(
        name='allcasts',    # This is the name of your PyPI-package.
        version=VERSION,                          # Update the version number for new releases
        license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
        description='A simple command line tool to download all podcasts from a given RSS feed',   # Give a short description about your library
        long_description=README,
        long_description_content_type="text/markdown",
        url="https://github.com/illegalbyte/allcasts",   # Provide either the link to your github or to your website
        author="Lewis Gentle",
        install_requires=["pyinputplus", "wget", "xmltodict", "colorama", "urllib", "os"],
        classifiers=[
            # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',      # Define that your audience are developers
            'Topic :: Utilities', # Define the topic of your package
            'License :: OSI Approved :: MIT License',   # Again, pick a license
            'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
        packages=find_packages(exclude=['test']),
        include_package_data=True,
)

