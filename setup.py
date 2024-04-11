from setuptools import setup, find_packages

setup(
    name='TACOS',
    version='1.0.0',
    packages=find_packages(where='Python'),
    package_dir={'': 'Python'},
    description='Transform source atlas t-statistics to target atlas t-statistics',
    long_description=open('README.md').read(),
    author='Qingyuan Liu',
    author_email='yongbin.wei@bupt.edu.cn',
    install_requires=[
        'numpy',
        'matplotlib',
    ],
    package_data={
        'TACOS': [
            'resources/coefficient/*.mat',
            'resources/overlap/*.txt',
            'resources/threshold/*.txt',
            'resources/default_variance/*.csv',
            'resources/region_order/*.txt',
        ],
    },
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International",
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
