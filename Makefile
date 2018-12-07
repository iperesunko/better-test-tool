format:
	black better_test_tool tests -S -l 119
	isort better_test_tool tests -rc

test:
	py.test --cov=better_test_tool tests -v

clean:
	rm -rf better_test_tool.egg-info
	rm -rf build
	rm -rf dist
	rm -rf .pytest_cache