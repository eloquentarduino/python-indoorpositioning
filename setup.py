from distutils.core import setup

packages = [
  "indoorpositioning",
  "indoorpositioning.scanner",
  "indoorpositioning.tests",
]

setup(
  name="indoorpositioning",
  packages=packages,
  version="0.0.1",
  license="MIT",
  description="Hardware-independent indoor positioning using Access points",
  author="Simone Salerno",
  author_email="eloquentarduino@gmail.com",
  url="https://github.com/eloquentarduino/python-indoorpositioning",
  download_url="https://github.com/eloquentarduino/python-indoorpositioning/raw/master/dist/indoorpositioning-0.0.1.tar.gz",
  keywords=[
    "indoor positioning"
  ],
  install_requires=[],
  classifiers=[
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
  ],
)
