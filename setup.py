from setuptools import setup

setup(
    name='fpu_can_parser',
    version='0.1.0',
    description='Read and parse CAN data from a CAN Data Line',
    url='https://github.com/PheonixRacingUnofficial/CANDataParser',
    author='FPU Pheonix Racing CS Team',
    license='GPL-3.0',
    packages=['fpu_can_parser'],

    # modify this line to include the packages you want to install when you run `pip install fpu_can_parser`
    # if Colin can provide a list of packages, that would be great
    install_requires=['mpi4py>=2.0',
                      'numpy',
                      ],

    classifiers=[
        'WIP',
    ],
)