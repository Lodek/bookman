import setuptools

setuptools.setup(
    name='bookman',
    version='0.0.1',
    author='Lodek',
    description='Book manager',
    packages=['bookman'],
    entry_points={
        'console_scripts' : ['bookman = bookman.bookman:main'],
        }
    )

