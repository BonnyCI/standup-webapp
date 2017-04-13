from setuptools import setup, find_packages

setup(name='standup_webapp',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'flask',
      ],
      version='0.1')
