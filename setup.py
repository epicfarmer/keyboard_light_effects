import setuptools

with open("README.md","r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="kfx",
  version = "0.0.dev1",
  author = "Joshua Kaminsky",
  author_email = "jkaminsky@jhu.edu",
  description = "Control a strand of lights using a midi keyboard",
  long_description=long_description,
  url="https://github.com/jkaminsk7/kfx",
  packages = setuptools.find_packages(),
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Indended Audience :: Hobbyists",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: Raspbian"
  ],
)
