build:
	@(rm -rfv dist)
	@(python3 setup.py sdist)

clean:
	@(rm -rfv halcon.egg-info dist build)
	@(find . -type d -name "__pycache__" -exec rm -rfv {} \;)
