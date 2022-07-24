unittest:
	pytest test/

coverage:
	coverage erase
	coverage run -m pytest test/
	coverage report -m

lint:
	flake8 dsutil/ test/