============
Contributing
============

.. _guide-contributing-start:

Contributions to PyPop are welcome, and they are greatly appreciated!
Every little bit helps, and credit will always be given.

Reporting and requesting
========================

.. _guide-contributing-bug-report:

Did you find a bug?
-------------------

When `reporting a bug
<https://github.com/alexlancaster/pypop/issues>`_ please use one of
the provided issue templates if applicable, otherwise just start a
blank issue and describe your situation.

* Ensure the bug was not already reported by searching on GitHub under
  `Issues <https://github.com/alexlancaster/pypop/issues>`_.

* If you're unable to find an open issue addressing the problem, open
  a new one. Be sure to include a title and clear description, as much
  relevant information as possible, and a code sample or an executable
  test case demonstrating the expected behavior that is not occurring.

* If possible, use the relevant bug report templates to create the issue.

* When reporting bugs, especially during installation, please run the
  following and include the output:

  .. code:: shell

     echo $CPATH
     echo $LIBRARY_PATH
     echo $PATH
     which python

  If you are running on MacOS, and you used the MacPorts installation
  method, please also run and include the output of:

  ::

    port installed

  
Documentation improvements
--------------------------

**pypop** could always use more documentation, whether as part of the
official docs, in docstrings, or even on the web in blog posts,
articles, and such. Write us a `documentation issue
<https://github.com/alexlancaster/pypop/issues/new>`_ describing what
you would like to see improved in here.

If you are able to contribute directly (e.g., via a pull request), please read
our `website contribution guide <Making a documentation or website contribution_>`_.

Feature requests and feedback
-----------------------------

The best way to send feedback is to file an issue using the `feature
template
<https://github.com/alexlancaster/pypop/issues/new?assignees=&labels=&projects=&template=feature_request.md>`_.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that code contributions are welcome 

Making a code contribution
==========================

To contribute new code that implement a feature, or fix a bug, this
section provides a step-by-step guide to getting you set-up.  The main
steps are:

1. forking the repository (or "repo")
2. cloning the main repo on to your local machine
3. making a new branch
4. `installing a development version <Installation for developers_>`_ on your machine
5. updating your branch when "upstream" (the main repository) has changes to include those changes in your local branch
6. updating the changelog in ``NEWS.rst``
7. checking unit tests pass
8. making a pull request


Fork this repository
--------------------

`Fork this repository before contributing`_. Forks creates a cleaner representation of the `contributions to the
project`_.

Clone the main repository
-------------------------

Next, clone the main repository to your local machine:

.. code-block:: shell

    git clone https://github.com/alexlancaster/pypop.git
    cd pypop

Add your fork as an upstream repository:

.. code-block:: shell

    git remote add myfork git://github.com/YOUR-USERNAME/pypop.git
    git fetch myfork

Make a new branch
-----------------

From the ``main`` branch create a new branch where to develop the new code.

.. code-block:: shell

    git checkout main
    git checkout -b new_branch


**Note** the ``main`` branch is from the main repository.

Build locally and make your changes
-----------------------------------

Now you are ready to make your changes.  First, you need to build
``pypop`` locally on your machine, and ensure it works, see the
separate section on `building and installing a development version
<Installation for developers_>`_.

Once you have done the installation and have verified that it works,
you can start to develop the feature, or make the bug fix, and keep
regular pushes to your fork with comprehensible commit messages.

.. code-block:: shell

    git status
    git add # (the files you want)
    git commit # (add a nice commit message)
    git push myfork new_branch

While you are developing, you can execute ``pytest`` as needed to run
your unit tests. See `run unit tests with pytest`_.

Keep your branch in sync with upstream
--------------------------------------

You should keep your branch in sync with the upstream ``main``
branch. For that:

.. code-block:: shell

    git checkout main  # return to the main branch
    git pull  # retrieve the latest source from the main repository
    git checkout new_branch  # return to your devel branch
    git merge --no-ff main  # merge the new code to your branch

At this point you may need to solve merge conflicts if they exist. If you don't
know how to do this, I suggest you start by reading the `official docs
<https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-on-github>`_

You can push to your fork now if you wish:

.. code-block:: shell

    git push myfork new_branch

And, continue doing your developments are previously discussed.

Update ``NEWS.rst``
-------------------

Update the changelog file under :code:`NEWS.rst` with an explanatory
bullet list of your contribution. Add that list under the "Notes
towards the next release" under the appropriate category, e.g. for a
new feature you would add something like:

.. code-block:: text

    Notes towards next release
    --------------------------
    (unreleased)

    New features
    ^^^^^^^^^^^^
    
    * here goes my new additions
    * explain them shortly and well


Also add your name to the authors list at :code:`website/docs/AUTHORS.rst`.

Run unit tests with ``pytest``
------------------------------

Once you have done your initial installation, you should first check
that the build worked, by running the test suite, via ``pytest``:

.. code-block:: shell

   pytest tests

If ``pytest`` is not already installed, you can install via:

.. code-block:: shell

    pip install pytest
   
If you run into errors during your initial installationg, please first
carefully repeat and/or check your installation. If you still get
errors, file a bug, and include the output of ``pytest`` run in
verbose mode and capturing the output

.. code-block:: shell

   pytest -s -v tests
   
   
You should also continuously run ``pytest`` as you are developing your
code, to ensure that you don't inadvertently break anything.

Also before creating a Pull Request from your branch, check that all
the tests pass correctly, using the above.

These are exactly the same tests that will be performed online via
Github Actions continuous integration (CI).  This project follows CI
good practices (let us know if something can be improved).

Make a Pull Request
-------------------

Once you are finished, you can create a pull request to the main
repository and engage with the developers.  If you need some code
review or feedback while you're developing the code just make a pull
request.

**However, before submitting a Pull Request, verify your development branch passes all
tests as** `described above <run unit tests with pytest_>`_ **. If you are
developing new code you should also implement new test cases.**

**Pull Request checklist**

Before requesting a finale merge, you should:

1. Make sure your PR passes all ``pytest`` tests.
2. Add unit tests if you are developing new features
3. Update documentation when there's new API, functionality etc.
4. Add a note to ``NEWS.rst`` about the changes.
5. Add yourself to ``website/docs/AUTHORS.rst``.


Installation for developers
===========================

Once you have setup your branch as described in `making a code
contribution`_, above, you are ready for the four main steps of the
developer installation:

1. install a build environment
2. build
3. run tests

.. note::

   Note that you if you need to install PyPop from source, but do not
   intend to contribute code, you can skip creating your own forking
   and making an additional branch, and clone the main upstream
   repository directly:

   .. code:: shell

      git clone https://github.com/alexlancaster/pypop.git
      cd pypop
   
For most developers, we recommend using the miniconda approach
described below.

Install the build environment
-----------------------------

To install the build environment, you should choose either ``conda`` or
system packages. Once you have chosen and installed the build
environment, you should follow the instructions related to the option
you chose here in all subsequent steps.

Install build environment via miniconda (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Visit https://docs.conda.io/en/latest/miniconda.html to download the
   miniconda installer for your platform, and follow the instructions to
   install.

      In principle, the rest of the PyPop miniconda installation process
      should work on any platform that is supported by miniconda, but
      only Linux and MacOS have been tested in standalone mode, at this
      time.

2. Once miniconda is installed, create a new conda environment, using
   the following commands:

   .. code-block:: shell

      conda create -n pypop3 gsl swig python=3

   This will download and create a self-contained build-environment that
   uses of Python to the system-installed one, along with other
   requirements. You will need to use this this environment for the
   build, installation and running of PyPop. The conda environment name,
   above, ``pypop3``, can be replaced with your own name.

      When installing on MacOS, before installing ``conda``, you should
      first to ensure that the Apple Command Line Developer Tools
      (XCode) are
      `installed <https://mac.install.guide/commandlinetools/4.html>`__,
      so you have the compiler (``clang``, the drop-in replacement for
      ``gcc``), ``git`` etc. ``conda`` is unable to include the full
      development environment for ``clang`` as a conda package for legal
      reasons.

3. Activate the environment, and set environments variables needed for
   compilation:

   .. code-block:: shell

      conda activate pypop3
      conda env config vars set CPATH=${CONDA_PREFIX}/include:${CPATH}
      conda env config vars set LIBRARY_PATH=${CONDA_PREFIX}/lib:${LIBRARY_PATH}
      conda env config vars set LD_LIBRARY_PATH=${CONDA_PREFIX}/lib:${LD_LIBRARY_PATH}

4. To ensure that the environment variables are saved, reactivate the
   environment:

   .. code-block:: shell

      conda activate pypop3

5. Skip ahead to `Build PyPop`_.

Install build environment via system packages (advanced)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unix/Linux:
^^^^^^^^^^^

1. Ensure Python 3 version of ``pip`` is installed:

   .. code-block:: shell

      python3 -m ensurepip --user --no-default-pip

   ..

      Note the use of the ``python3`` - you may find this to be
      necessary on systems which parallel-install both Python 2 and 3,
      which is typically the case. On newer systems you may find that
      ``python`` and ``pip`` are, by default, the Python 3 version of
      those tools.

2. Install packages system-wide:

   1. Fedora/Centos/RHEL

      .. code-block:: shell

         sudo dnf install git swig gsl-devel python3-devel

   2. Ubuntu

      .. code-block:: shell

         sudo apt install git swig libgsl-dev python-setuptools

MacOS X
^^^^^^^

1. Install developer command-line tools:
   https://developer.apple.com/downloads/ (includes ``git``, ``gcc``)

2. Visit http://macports.org and follow the instructions there to
   install the latest version of MacPorts for your version of MacOS X.

3. Set environment variables to use macports version of Python and other
   packages, packages add the following to ``~/.bash_profile``

   .. code:: shell

      export PATH=/opt/local/bin:$PATH
      export LIBRARY_PATH=/opt/local/lib/:$LIBRARY_PATH
      export CPATH=/opt/local/include:$CPATH

4. Rerun your bash shell login in order to make these new exports active
   in your environment. At the command line type:

   .. code:: shell

      exec bash -login

5. Install dependencies via MacPorts and set Python version to use
   (FIXME: currently untested!)

   .. code:: shell

      sudo port install swig-python gsl py39-numpy py39-lxml py39-setuptools py39-pip py39-pytest
      sudo port select --set python python39
      sudo port select --set pip pip39

6. Check that the MacPorts version of Python is active by typing:
   ``which python``, if it is working correctly you should see
   ``/opt/local/bin/python``.

Windows
~~~~~~~

(Currently untested in standalone-mode)


Build PyPop
-----------

You should choose *either* of the following two approaches. Don’t try
to mix-and-match the two. The build-and-install approach is only
recommended if don’t plan to make any modifications to the code
locally.

Build-and-install (not recommended for developers)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have setup your environment and cloned the repo, you can use
the following one-liner to examine the ``setup.py`` and pull all the
required dependencies from ``pypi.org`` and build and install the
package.

   Note that if you use this method and install the package, it will be
   available to run anywhere on your system, by running ``pypop``.

..

   If you use this installation method, changes you make to the code,
   locally, or via subsequent ``git pull`` requests will not be
   available in the installed version until you repeat the
   ``pip install`` command.

1. if you installed the conda development environment, use:

   .. code-block:: shell

      pip install .[test]

   ..

      (the ``[test]`` keyword is included to make sure that any package
      requirements for the test suite are installed as well).

2. if you installed a system-wide environment, the process is slightly
   different, because we install into the user’s ``$HOME/.local`` rather
   than the conda environment:

   .. code-block:: shell

      pip install --user .[test]

3. PyPop is ready-to-use, you should `run unit tests with pytest`_.

4. if you later decide you want to switch to using the developer
   approach, below, follow the `cleaning up build`_ before
   starting.

Build-and-run-from-checkout (recommended for developers)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. First manually install the dependencies via ``pip``, note that if you
   are running on Python <= 3.8, you will need to also add
   ``importlib-resources`` to the list of packages, below.

   1. conda

      .. code-block:: shell

         pip install numpy lxml psutil pytest

   2. system-wide

      .. code-block:: shell

         pip install --user numpy lxml psutil pytest

2. Run the build

   .. code-block:: shell

      ./setup.py build

3. You will be runnning PyPop, directly out of the ``src/PyPop``
   subdirectory (e.g. ``./src/PyPop/pypop.py`` and
   ``./src/PyPop/popmeta.py``). Note that you have to include the
   ``.py`` extension when you run from an uninstalled checkout,
   because the script is not installed.

Cleaning up build
~~~~~~~~~~~~~~~~~

If you installed using the approach in `Build-and-install (not recommended
for developers)`_, above, follow the end-user instructions on
:ref:`uninstalling PyPop`.  In addition, to clean-up any compiled
files and force a recompilation from scratch, run the ``clean``
command:

.. code-block:: shell

   ./setup clean --all

Making a documentation or website contribution
==============================================

Interested in maintaining the PyPop website and/or documentation, such
as the *PyPop User Guide*? Here are ways to help.

Overview
--------

All the documentation (including the website homepage) are maintained in
this directory (and subdirectories) as
`reStructuredText <https://docutils.sourceforge.io/rst.html>`__
(``.rst``) documents. reStructuredText is very similar to GitHub
markdown (``.md``) and should be fairly self-explanatory to edit
(especially for pure text changes). From the .rst “source” files which
are maintained here on github, we use
`sphinx <https://www.sphinx-doc.org/en/master/>`__ to generate (aka
“compile”) the HTML for both the pypop.org user guide and and PDF (via
LaTeX) output. We have setup a GitHub action, so that as soon as a
documentation source file is changed, it will automatically recompile
all the documentation, update the ``gh-pages`` branch (which is synced
to the GitHub pages) and update the files on the website.

Here’s an overview of the process:

::

   .rst files -> sphinx -> HTML / PDF -> push to gh-pages branch -> publish on pypop.org

This means that any changes to the source will automatically update both
website home page the documentation.

Once any changes are pushed to a branch (as described below), the GitHub
action will automatically rebuild the website, and the results will be
synced to a “staging” version of the website at:

-  https://alexlancaster.github.io/beta.pypop.org/

Structure
---------

Here’s an overview of the source files for the website/documentation
located in the ``website`` subdirectory at the time of writing.  Note
that some of the documentation and website files, use the
``include::`` directive to include some "top-level" files, located
outside ``website`` like ``README.rst`` and ``CONTRIBUTING.rst``:

-  ``index.rst`` (this is the source for the homepage at
   http://pypop.org/)
-  ``conf.py`` (Sphinx configuration file - project name and other
   global settings are stored here)
   
-  ``docs`` (directory containing the source for the *PyPop User Guide*, which will eventually live at http://pypop.org/docs). 

   -  ``index.rst`` (source for the top-level of the *PyPop User Guide*)
   -  ``guide-chapter-install.rst`` (pulls in parts of the top-level ``README.rst``)
   -  ``guide-chapter-usage.rst``
   -  ``guide-chapter-instructions.rst``
   -  ``guide-chapter-contributing.rst`` (pulls in top-level
      ``CONTRIBUTING.rst`` that contains the source of the text that you are reading right now)
   -  ``guide-chapter-changes.rst`` (pulls in top-level ``NEWS.rst`` and ``AUTHORS.rst``, which is local to ``website``)
   -  ``AUTHORS.rst``
   -  ``licenses.rst`` (pulls in top-level ``LICENSE``)
   -  ``biblio.rst``

-  ``html_root`` (any files or directories commited in this directory
   will appear at the top-level of the website)

   -  ``psb-pypop.pdf`` (e.g. this resides at
      http://pypop.org/psb-pypop.pdf)
   -  ``tissue-antigens-lancaster-2007.pdf``
   -  ``PyPopLinux-0.7.0.tar.gz`` (old binaries - will be removed soon)
   -  ``PyPopWin32-0.7.0.zip``
   -  ``popdata`` (directory - Suppl. data for Solberg et. al 2018 -
      https://pypop.org/popdata/)

-  ``reference`` (directory containing the old DocBook-based
   documentation, preserved to allow for unconverted files to be
   converted later, this directory is ignored by the build process)

Modifying documentation
-----------------------

Minor modifications
~~~~~~~~~~~~~~~~~~~

For small typo fixes, moderate copyedits at the paragraph level
(e.g. adding or modifying paragraphs with little or no embedded markup),
you can make changes directly on the github website.

1. navigate to the ``.rst`` file you want to modify in the GitHub code
   directory, you’ll see a preview of how most of the ``.rst`` will be
   rendered

2. hover over the edit button - you’ll see an “**Edit the file in a
   fork in your project**” (if you are already a project collaborator,
   you may also have the optional of creating a branch directly in the
   main repository).

3. click it and it will open up a window where you can make your changes

4. make your edits (it’s a good idea to look at the preview tab
   periodically as you make modifications)

5. once you’ve finished with the modifications, click “**Commit
   changes**”

6. put in an a commit message, and click “**Propose changes**”

7. this will automatically create a new branch in your local fork, and
   you can immediately open up a pull-request by clicking “**Create pull
   request**”

8. open up a pull-request and submit - new documentation will be
   automatically built and reviewed. if all is good, it will be merged
   by the maintainer and made live on the site.

Major modifications
~~~~~~~~~~~~~~~~~~~

For larger structural changes involving restructuring documentation or
other major changes across multiple ``.rst`` files, **it is highly
recommended** that you should make all changes in your own local fork,
by cloning the repository on your computer and then building the
documentation locally. Here’s an overview of how to do that:

   The commands in the "Sphinx build" section of the workflow
   `.github/workflows/documentation.yaml <https://github.com/alexlancaster/pypop/blob/main/.github/workflows/documentation.yaml>`_
   which are used to run the GitHub Action that builds the documentation
   when it it deployed, is the best source for the most update-to-date
   commands to run, and should be consulted if the instructions in this
   document become out of date.

1. install sphinx and sphinx extensions

   .. code-block:: shell

      pip install setuptools_scm sphinx piccolo-theme sphinx_rtd_theme myst_parser rst2pdf sphinx_togglebutton sphinx-argparse

2. make a fork of pypop if you haven't already (see `previous section <Fork this repository_>`_)

3. `clone the fork and add your fork as an upstream repository <Clone
   the main repository_>`_ on your local computer, and `make a new
   branch`_. Note that you do not need to build pypop first in order to build
   the documentation - you can do them separately. 

4. make your changes to your ``.rst`` files and/or ``conf.py``

5. build the HTML documentation:

   .. code-block:: shell

      sphinx-build website _build

6. view the local documention: you can open up browser and navigate to
   the ``index.html`` in the top-level of the newly-created ``_build``
   directory

7. use ``git commit`` to commit your changes to your local fork.

8. open up a pull-request against the upstream repository

Building the PDF for the *PyPop User Guide* is a bit more involved, as
you will need to have various TeX packages installed.

1. install the LaTeX packages (these are packages needed for Ubuntu,
   they may be different on your distribution):

   .. code-block:: shell

      sudo apt-get install -y latexmk texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra texlive-luatex texlive-xetex

2. build the LaTeX and then compile the PDF:

   .. code-block:: shell

      sphinx-build -b latex website _latexbuild
      make -C _latexbuild

3. the user guide will be generated in ``_latexbuild/pypop-guide.pdf``



.. _Fork this repository before contributing: https://github.com/alexlancaster/pypop/network/members
.. _up to date with the upstream: https://gist.github.com/CristinaSolana/1885435
.. _contributions to the project: https://github.com/alexlancaster/pypop/network
.. _Gitflow Workflow: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow
.. _Pull Request: https://github.com/alexlancaster/pypop/pulls
