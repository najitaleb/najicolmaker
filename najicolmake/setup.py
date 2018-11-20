from setuptools import setup
pkg_subdir = "colmake6"

setup(name='najicolmake',
      version='0.1',
      description='aaaa',
      url='http://github.com/najitaleb/najicol1120',
      author='Naji',
      author_email='najitaleb@gmail.com',
      packages=find_packages(),
      install_requires=[
          'markdown',
		  'pandas',
		  'os',
		  'yaml',
		  'json',
		  'requests',
		  'bioblend',
		  

      ],
      zip_safe=False)