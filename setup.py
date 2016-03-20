import codecs
from setuptools import setup


def long_description():
    with codecs.open('README.rst', encoding='utf8') as f:
        return f.read()


setup(
    name='httpie',
    version='0.0.1',
    description='',
    long_description=long_description(),
    url='https://github.com/socketubs/shelter',
    author='Geoffrey Lehée',
    author_email='hello@socketubs.org',
    license='MIT',
    packages=['shelter'],
    entry_points={
        'console_scripts': [
            'shelter = shelter.__main__:main',
        ],
    },
    install_requires=['click==6.3'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development',
    ]
)
