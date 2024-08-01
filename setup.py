from setuptools import setup

setup(
    name='pywttk',
    version='0.1.0',    
    description='Python Wavetable Toolkit',
    url='https://github.com/ath-r/pywttk',
    author='ath',
    author_email='korglp380@yandex.ru',
    license='MIT',
    packages=['pywttk'],
    install_requires=['numpy', 
                      'soundfile'                    
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License', 
        'Programming Language :: Python :: 3'
    ],
)