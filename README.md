[![Travis Build Status](https://travis-ci.org/googlefonts/fontbakery-cli.svg)](https://travis-ci.org/googlefonts/fontbakery-cli)
[![Coveralls.io Test Coverage Status](https://img.shields.io/coveralls/googlefonts/fontbakery-cli.svg)](https://coveralls.io/r/googlefonts/fontbakery-cli)

### How to setup travis deployment to push gh-pages

```
$ curl -u <username> \
  -d '{"scopes":["public_repo"],"note":"CI: <reponame>"}' \
  https://api.github.com/authorizations

# The Travis gem provides the travis command. Use the travis command
#  to encrypt the three environment variables listed above. Replace
#  <token> with your GitHub authentication token

$ gem install travis
$ travis login --github-token <token>
$ travis encrypt 'GIT_NAME="Your Name" \
    GIT_EMAIL=you@example.com GH_TOKEN=<token>' --add

```
