code-formatting:
	black better_test_tool -S -l 119
	isort better_test_tool -rc

run-tests:
	py.test --cov=better_test_tool tests -v
