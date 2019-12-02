import setuptools

with open('requirements.txt', 'r') as f_req:
  REQUIREMENTS = [req.strip() for req in f_req.readlines()]

# TODO: add a README file.
setuptools.setup(
    name='SimStrategies',
    version='0.1.0',
    author='Zhou Wang',
    author_email='wangzhou666666@gmail.com',
    description='A package to back-test trading strategies.',
    url='https://github.com/wangzhou666/simstrategies',
    license='MIT',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'simstrategies=simstrategies.run:main',
        ],
    },
    python_requires='>=3.6',
    install_requires=REQUIREMENTS,
)
