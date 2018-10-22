run-tests:
	pytest -v tests

show-coverage:
	py.test --cov=bds_test_tool tests/