Setup
-----

Setup a venv

	python3 -m venv ./venv-bwp
	. ./venv-bwp/bin/activate

	pip install -e .



Notes:
https://discuss.python.org/t/where-to-get-started-with-pyproject-toml/4906/15
https://snarky.ca/what-the-heck-is-pyproject-toml/
http://ivory.idyll.org/blog/2021-transition-to-pyproject.toml-example.html


Deploy
------

boss-test:

	zypper in python3-virtualenv python3-wheel


	virtualenv ./venv-bwp --no-setuptools --no-wheel
	. venv-bwp/bin/activate
	pip install -e .
	
