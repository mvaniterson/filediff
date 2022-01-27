from setuptools import setup, find_packages

setup(
    name='file-differ',
    description='check if two files are identical',
    packages=find_packages(),
    author='Maarten van Iterson',
    entry_points="""
    [console_scripts]
    file-differ=filediffer:filediffer
    """,
    install_requires = ['click==8.0.3',
                        'numpy>1.9.0',
                        'pandas>1.2.5',
                        'pylint==2.12.2',
                        'pytest==6.2.5',
                        'pytest-cov==3.0.0'],
    version = '0.0.1',
    url = 'https://github.com/mvaniterson/filediff.git'
)