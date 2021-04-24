# import packages
import io
import os
import sys
from shutil import rmtree
from setuptools import find_packages, setup, Command

# import custom packages

# define static variables
name = 'fanduel-api'
description = 'Package for scraping and executing real-time trading'
url = 'https://github.com/ribeiro11075/fanduel-api'
author_email = 'ribeiro11075@gmail.com'
author = 'David Ribeiro'
requires_python = '>=3.6.0'
version = '0.0.0'
install_requires = ['pandas', 'selenium', 'bs4']
extras_require = {}
include_package_data = True
exclude = ['config']
license = 'MIT'
classifiers = ['License :: OSI Approved :: MIT License', 'Programming Language :: Python :: 3']

# define dynamic variables
here = os.path.abspath(os.path.dirname(__file__))

try:
	with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
		long_description = '\n' + f.read()
		long_description_content_type = 'text/markdown'
except FileNotFoundError:
		long_description = description
		long_description_content_type = 'text'


class UploadCommand(Command):

	@staticmethod
	def status(s):
		print('\033[1m{0}\033[0m'.format(s))


	def initialize_options(self):
		pass


	def finalize_options(self):
		pass


	def run(self):

		try:
			self.status('Removing previous builds…')
			rmtree(os.path.join(here, 'dist'))
		except OSError:
			pass

		self.status('Building Source and Wheel (universal) distribution…')
		os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

		self.status('Uploading the package to PyPI via Twine…')
		os.system('twine upload dist/*')

		self.status('Pushing git tags…')
		os.system('git tag v{0}'.format(about['__version__']))
		os.system('git push --tags')

		sys.exit()


setup(
		name=name,
		version=version,
		description=description,
		long_description=long_description,
		long_description_content_type=long_description_content_type,
		author=author,
		author_email=author_email,
		python_requires=requires_python,
		url=url,
		packages=find_packages(exclude=exclude),
		install_requires=install_requires,
		extras_require=extras_require,
		include_package_data=include_package_data,
		license=license,
		classifiers=classifiers,
		cmdclass = {'upload': UploadCommand}
	)
