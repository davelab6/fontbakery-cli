[![Travis Build Status](https://travis-ci.org/googlefonts/fontbakery-cli.svg)](https://travis-ci.org/googlefonts/fontbakery-cli)
[![Coveralls.io Test Coverage Status](https://img.shields.io/coveralls/googlefonts/fontbakery-cli.svg)](https://coveralls.io/r/googlefonts/fontbakery-cli)

# FontBakery CLI

FontBakery CLI can build UFO, SFD, or TTX font projects. You can set it up with Travis and Github Pages so that each update to your Github repo is built and tested, and the binary font files and test results are available on the web. 

1. Enable your repo in Travis
2. Generate a `$token` so travis can push the builds back to Github, replacing `$githubUserName` and `$githubRepoName`:
```sh
$ curl -u $githubUserName \
   -d '{"scopes":["public_repo"],"note":"CI: $githubRepoName"}' \
   https://api.github.com/authorizations
```
3. Install the `travis` command with gem and use it to convert the `$token` into a `$key`:
```
$ gem install travis
$ travis login --github-token $token
$ travis encrypt 'GIT_NAME="Your Name" \
    GIT_EMAIL=you@example.com GH_TOKEN=$token' --add
```
4. Make a `.travis.yml` as follows
```
language: python
before_install:
- sudo add-apt-repository --yes ppa:fontforge/fontforge
- sudo apt-get update -qq
- sudo apt-get install python-fontforge
- cp /usr/lib/python2.7/dist-packages/fontforge.* "$HOME/virtualenv/python2.7.8/lib/python2.7/site-packages"
install:
- pip install git+https://github.com/behdad/fontTools.git
- pip install git+https://github.com/googlefonts/fontbakery-cli.git
- pip install jinja2
script: PATH=/home/travis/virtualenv/python2.7.8/bin/:$PATH fontbakery.py .
branches:
  only:
  - master
after_script:
- rm -rf builds/build/sources builds/build/build.state.yaml
- PATH=/home/travis/virtualenv/python2.7.8/bin/:$PATH bakery-report.py builds/build
- PATH=/home/travis/virtualenv/python2.7.8/bin/:$PATH travis-deploy.py
env:
  global:
    secure: $key
```
