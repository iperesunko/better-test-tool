code-formatting:
	black better_test_tool -S -l 119
	isort better_test_tool -rc

run-tests:
	pytest -v tests

show-coverage:
	py.test --cov=bds_test_tool tests/