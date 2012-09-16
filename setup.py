from setuptools import setup, find_packages
import os

version = 'dev'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(name='lfs-theme-bootstrap',
      version=version,
      description='The Twitter Bootstrap demo theme for LFS',
      long_description=README,
      classifiers=[
          'Environment :: Web Environment',
          'Framework :: Django',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
      ],
      keywords='django e-commerce online-shop',
      author='Thomas Jetzinger',
      author_email='thomas@jetzinger.com',
      url='https://github.com/tjetzinger/lfs-theme-bootstrap',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
      ],
      )
