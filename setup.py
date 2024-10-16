from setuptools import setup, find_packages

with open('requirements.txt', encoding='utf-16') as f:
    requirements = f.read().splitlines()

setup(
    name='needlr',
    version='0.1.4',
    description='A package to help you work with Microsoft Fabric from Python',
    author='Tonio Lora',
    author_email='tonio.lora@outlook.com',
    url='https://github.com/microsoft/needlr',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',  # Choose the right status for your project
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # Or the license you use
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    python_requires='>=3.8',  # Specify the Python version requirement
    package_data={
        'needlr': ['needlr.png'],
    },
)
