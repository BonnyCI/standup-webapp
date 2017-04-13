from setuptools import setup, find_packages

setup(name='standup_webapp',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['Flask'],
      zip_safe=False,
      version='0.1')
