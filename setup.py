from setuptools import setup, find_packages

setup(
    name='p8n-importer',
    version='1.0.0',
    description='A tool to import various dataset formats and upload them to the PropulsionAI platform.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='PropulsionAI',
    author_email='hello@propulsionhq.com',
    url='https://www.propulsionhq.com/',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "tqdm==4.65.0",
        "requests==2.31.0",
        "Pillow==9.3.0",
        "tqdm==4.65.0",
        "pyarrow",
        "pandas",
        "pyyaml",
        "openpyxl"
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'p8n-importer=P8nImporter.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
