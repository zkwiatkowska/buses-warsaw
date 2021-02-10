"""Library setup."""
import setuptools
from setuptools import setup

setup(
    name='bwaw',
    version='0.1.0',
    description='Processing and analyzing data from UW Warsaw API.',
    url='https://github.com/zkwiatkowska/bwaw',
    author='Zuzanna Kwiatkowska',
    license='MIT License',
    packages=setuptools.find_packages(),
    install_requires=['jupyter==1.0.0',
                      'numpy==1.19.5',
                      'pandas==1.2.0',
                      'tqdm==4.56.0',
                      'pytest==6.2.2',
                      'mock==4.0.3'
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License ',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8'
    ],
)
