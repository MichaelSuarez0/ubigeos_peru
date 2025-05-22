from setuptools import setup, find_packages

setup(
    name='ubigeos_peru',
    version='0.1.1',
    author='Michael Suárez',
    author_email='michael-salvador@hotmail.com',
    description='Librería de Python ligera especializada para consultas a partir del código de ubigeo para obtener el nombre del departamento, provincia o distrito, y viceversa, además de información suplementaria.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MichaelSuarez0/ubigeos_peru',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
