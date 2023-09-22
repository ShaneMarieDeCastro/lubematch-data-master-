from setuptools import setup, find_packages

setup(
    name='ses-cli',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pandas',
        'cx-Oracle',
        'xlrd',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        ses-cli=main:cli
    ''',
)
