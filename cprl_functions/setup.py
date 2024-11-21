from setuptools import setup, find_packages

VERSION = '0.0.7' 
DESCRIPTION = 'cprl_functions'
LONG_DESCRIPTION = 'Functions used for managing and migrating data into cprl'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="cprl_functions", 
        version=VERSION,
        author="Chrsitian Lutz",
        author_email="<clutz@hunt-institute.org>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(where='.', include=['cprl_functions*']),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)