import tomllib

PROJECT = """
[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"
[project]
name = "serverlab-course-demo"
version = "0.1.0"
requires-python = ">=3.14"
[project.scripts]
serverlab-demo = "serverlab_demo:main"
[tool.setuptools]
py-modules = ["serverlab_demo"]
"""

def test_metadata():
    config = tomllib.loads(PROJECT)
    assert config['project']['scripts']['serverlab-demo'] == 'serverlab_demo:main'

if __name__ == '__main__':
    test_metadata()
    print(PROJECT)
