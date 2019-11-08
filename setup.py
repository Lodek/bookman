import setuptools

setuptools.setup(
    name='bookman',
    version='0.0.1',
    author='Bruno Gomes',
    description='Book manager',
    packages=setuptools.find_packages(),
    entrypoints={'console_scripts' : ['bookman = bookman.bookman:main']})
