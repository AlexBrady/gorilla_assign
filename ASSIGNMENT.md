# Test assignment for Gorilla backend engineers

You've been assigned to build the backend described in the [README](README.md).
This repository serves as a starting point. It contains a skeleton
[Python package](metr/) and [tests directory](tests/), a
[pyproject.toml](pyproject.toml) and a [Makefile](Makefile). While the end
result would run serverless in AWS Lambda, you don't have to worry about
deployment. The integration tests should prove that everything works as expected.

## Getting started

To get started you'll need Python 3.11 (we recommend installing it via
[pyenv](https://github.com/pyenv/pyenv)), and the
[Poetry](https://python-poetry.org/docs/#installation) package manager.

Install this project's development dependencies as follows:

```console
$ make install
```

Next, try running the tests to verify that everything was installed correctly:

```console
$ make test
```

We use the [Black code style](https://github.com/psf/black). Run `make lint` to
check linting and formatting, and use `make format` to format all files (or
configure your editor to run `isort` and `black` on save).

## Assignment

You'll be implementing the 5 endpoints described in the [README](README.md), for
which scaffolding is in place in [api.py](metr/api.py). This test will make use
of a [SQLite](https://www.sqlite.org/index.html) database, which you can
communicate with through the [SQLAlchemy](https://docs.sqlalchemy.org/en/14/index.html)
library. The data model is already set up in [models.py](metr/models.py), and
the tests run against a database with randomized data already present.
So what's left for you to do?

- Respond with respect for HTTP, REST and the end user: Return responses with
  appropriate status codes, common content types and clear structure.
- Validation: Ensuring that incoming data is valid according to the data model,
  and ensuring that clear error messages are in place.
- Data layer: fetching appropriate data from the database and storing incoming
  data.


There are already some integration tests in place that test the bare minimum
of these requirements. If those pass, you're off to a good start, but we expect
you to add some unit tests of your own and either make the existing integration
tests more specific or add some new ones.


Does that sound too easy and/or want to wow us? Here are some extra challenges
in no specific order:

- Filtering: On the `GET /meters` endpoint, allow filtering the response based
  on any field through query parameters.
- Pagination: On the `GET /meters` endpoint, send back a subset of the results,
  with a hyperlink to fetch the next page.
- Content Negotiation: Instead of limiting the response to a single content
  type, allow the client to specify one of multiple supported content types and
  respond with that type.
- Partial updates: Implement a `PATCH /meters/{meter_id}` call that allows to
  update specific fields of a meter, without completely replacing the resource.


## Guidelines

The exact specifications are explicitly left vague and/or incomplete, use your
experience and knowledge of common standards to fill in the gaps. Feel free to
use comments to indicate what your assumptions are, why you're making decisions,
or what you'd improve if you had more time.

You're allowed to add dependencies to the project, but please add a comment
saying why you're doing so. And please don't add an entire web framework such as
Django/Flask/FastAPI/... We're still building a serverless service here.

Some points we will look at when reviewing your code:

- Is the code organized cleanly, is it easily readable, extendable and
  maintainable?
- Is the resulting API RESTful, performant, and pleasant to use?
- For which code were tests added? Was reasonable test coverage achieved?
- How does the Git history look? Are commits logical and clearly described?
