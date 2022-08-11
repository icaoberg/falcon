build:
	@(rm -rfv dist)
	@(python3 setup.py sdist)

clean:
	@(find . -type d -name "__pycache__" -exec rm -rfv {} \;)
