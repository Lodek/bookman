import setuptools

setuptools.setup(
    name='bookman',
    version='0.0.1',
    author='Lodek',
    description='Book manager',
    packages=setuptools.find_packages(),
    entrypoints={'console_scripts' : ['bookman = bookman.bookman:main'],
                 'gui_scripts' : ['bookman = bookman.bookman:main']})

