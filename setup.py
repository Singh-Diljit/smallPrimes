from setuptools import setup, find_packages

setup(
    name='smallPrimes',                    
    version='0.1.0',                        
    author='Diljit Singh',                  
    author_email='diljitsingh22 @Googles email service',
    description='Generation and classification for primes under 10**8',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Singh-Diljit/smallPrimes',
    packages=find_packages(),                
    classifiers=[                           
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',                
    install_requires=[
        ],
    )
