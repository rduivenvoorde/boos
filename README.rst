Boos library and cli
====================


A python library and cli for the `Bose SoundTouch (R) API <http://products.bose.com/api-developer/index.html>`_.

To be able to use my Bose Soundtouch 10 from the command line.

And to be able to use it as library for Home-Assistant https://home-assistant.io/

And to be 'my first pip' package :-)



Installation
------------

To install boos python library, simply:

.. code-block:: shell

    pip install boos


``boos`` requires Python >= 3.4.


Quick Start
-----------

Connect to your Bose SoundTouch (R) device and activate preset 3

To work in python:

.. code-block:: python

    from boos import Boos

    booz = Boos("http://boos.fritz.box:8090")
    booz.preset(3)
    booz.vol()
    booz.vol(30)


Or if you can run python 3 code for example on Linux:

.. code-block:: bash

    # create a symbolic link to the cli.py
    # and (for now) be sure in cli.py you have the right url defined
    sudo ln -s ./boos/cli.py /usr/local/bin/boos
    # run
    boos
    boos set 3
    boos vol
    boos vol 30

Or create a virtualenv and create some bash file::
    virtualenv -p python3 boos
    cd boos
    pip install boos

    # and a bash file like:

    #!/bin/bash

    source /home/richard/venv/boos/bin/activate
    /home/richard/dev/boos/boos/cli.py "$@"


Links
-----

- As an alternative have a look at https://github.com/chassing/badtouch
- Bose SoundTouch (R) API http://products.bose.com/api-developer/index.html
- Home Assistant https://home-assistant.io/

Packaging
---------

All from https://python-packaging-user-guide.readthedocs.org/en/latest/distributing/#source-distributions


.. code-block:: bash

    # source dist
    python3 setup.py sdist
    # creating a universal wheel?
    python3 setup.py bdist_wheel

    # now setup a local webserver to test
    cd dist
    python -m SimpleHTTPServer 9000

    # and in another terminal
    # create a python 3 virtual environment venv (all as usual)
    virtualenv -p python3 venv
    cd venv
    source bin/activate
    # now in python
    python3
    >>> from boos import Boos
    >>> booz = Boos("http://boos.fritz.box:8090")
    >>> booz.preset(3)            # setting to preset 3
    >>> print(booz.now_playing()) # should show current playing song/source

    # https://packaging.python.org/en/latest/distributing/#uploading-your-project-to-pypi
    #
    # create a .pypirc file in home dir
    [distutils]
    index-servers=
        pypi
        testpypi

    [testpypi]
    repository = https://testpypi.python.org/pypi
    username = <your user name goes here>
    password = <your password goes here>

    [pypi]
    repository = https://pypi.python.org/pypi
    username = <your user name goes here>
    password = <your password goes here>
    #
    # to upload it to testpypi (https://wiki.python.org/moin/TestPyPI)
    # first register the project
    python setup.py register -r https://testpypi.python.org/pypi
    # preferred (given you have username and testpypi as key in .pypirc:
    twine upload -r testpypi dist/*
    # or
    python setup.py sdist upload -r https://testpypi.python.org/pypi
    # after upload install via
    # search
    pip search --index https://testpypi.python.org/pypi boos
    # install
    pip install -i https://testpypi.python.org/pypi boos

    # or to pypi
    # preferred:
    # first register project
    python setup.py register
    # preferred (given you have username and testpypi as key in .pypirc:
    twine upload -r pypi dist/*
    # or
    python setup.py sdist upload -r https://pypi.python.org/pypi
    # and install
    pip install boos


