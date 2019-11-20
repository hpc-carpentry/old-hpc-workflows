---
title: Setup
---

There are several pieces of software you will wish to install before the workshop.
Though installation help will be provided at the workshop,
we recommend that these tools are installed (or at least downloaded) beforehand.
Anaconda Python is a very large download.

## Python 3

Please install the Python 3 version of Anaconda from
[https://www.continuum.io/downloads](https://www.continuum.io/downloads)
(however any version of Python 3 will work).

Anaconda is a free version of Python that comes bundled with all of its most
useful tools. Even better, it includes several significant performance
improvements over "vanilla" Python.

The example code also requires the `matplotlib` and `numpy` libraries. They
are installed by default with Anaconda, but if you are using a different
Python you may need to install them manually. Using `pip`, the command would be:

~~~bash
pip install --user numpy matplotlib
~~~
{: .language-bash}

The example files download also contains a `requirements.txt` file that can
be used to specify the required packages for a Python virtual environment.
There are many guides to this process online, and the [official
documentation](https://docs.python.org/3/tutorial/venv.html) can help as
well.

## Snakemake

### Anaconda

Once Anaconda 3 is installed, you can install Snakemake at an Anaconda prompt:

~~~
conda create -c bioconda -c conda-forge -n snakemake snakemake-minimal
~~~
{: .language-bash}

> ## Note
> At the time of writing, the `snakemake` conda package was not installing correctly, however the `snakemake-minimal` was working.
> This lesson does not require any features beyond those included with the minimal install.
{: .callout}

### Vanilla Python

You can install Snakemake with:

~~~
pip install --user snakemake
~~~
{: .language-bash}

For more information, please refer to the [Snakemake installation documentation](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html).

## Lesson Data Files

The files used in this lesson can be downloaded:

* [for Linux/Mac](files/workflow-engines-lesson.tar.gz)
* [for Windows](files/workflow-engines-lesson.zip)

Once downloaded, please extract to the directory you wish to work in for all
the hands-on exercises.

{% include links.md %}
