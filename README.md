[![Travis Build Status](https://travis-ci.org/googlefonts/fontbakery-cli.svg)](https://travis-ci.org/googlefonts/fontbakery-cli)
[![Coveralls.io Test Coverage Status](https://img.shields.io/coveralls/googlefonts/fontbakery-cli.svg)](https://coveralls.io/r/googlefonts/fontbakery-cli)

# FontBakery CLI

FontBakery CLI can build UFO, SFD, or TTX font projects. You can set it up with Travis and Github Pages so that each update to your Github repo is built and tested, and the binary font files and test results are available on the web.

1. Enable your repo in Travis

2. Make a `.travis.yml` as follows

```
language: python
before_install:
- sudo add-apt-repository --yes ppa:fontforge/fontforge
- sudo apt-get update -qq
- sudo apt-get install python-fontforge
- cp /usr/lib/python2.7/dist-packages/fontforge.* "$HOME/virtualenv/python2.7.8/lib/python2.7/site-packages"
install:
- pip install git+https://github.com/behdad/fontTools.git
- pip install git+https://github.com/googlefonts/fontcrunch.git
- pip install git+https://github.com/googlefonts/fontbakery-cli.git
- pip install jinja2
before_script:
- mkdir -p builds/build
script: PATH=/home/travis/virtualenv/python2.7.8/bin/:$PATH fontbakery.py . | tee builds/build/buildlog.txt
branches:
  only:
  - master
after_script:
- PATH=/home/travis/virtualenv/python2.7.8/bin/:$PATH bakery-report.py builds/build
- rm -rf builds/build/sources
- rm -rf builds/build/build.state.yaml
- PATH=/home/travis/virtualenv/python2.7.8/bin/:$PATH travis-deploy.py
```

3. Run `travis-secure.sh` command from `fontbakery-cli`:

```
$ gem install travis  # first install travis
$ travis-secure.sh -u guthubusername -e your@email
```

DO NOT USE `travis-secure.sh` WITHOUT `--token` FOR `git submodule foreach`

It will ask you every time to enter password. I suggest you to use additional
 argument `--token`. That will avoid authentication for github and travis.

```
$ git submodule foreach "travis-secure.sh -u guthubusername -e your@email -t TOKEN"
```
