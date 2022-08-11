prepare:
	@(python3 -m pip install build twine)

build:
	@(rm -rfv dist)
	@(python3 -m build)

clean:
	@(rm -rfv halcon.egg-info dist build)
	@(find . -type d -name "__pycache__" -exec rm -rfv {} \;)

twine-check:
	@(twine check dist/*)

twine-test-upload:
	@(twine upload --verbose -r testpypi dist/*)

twine-upload:
	@(twine upload --verbose dist/*)
