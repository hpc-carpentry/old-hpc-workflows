---
title: Setup
---

There are several pieces of software you need to install before the workshop.
Though installation help will be provided at the workshop, we recommend that
these tools are installed (or at least downloaded) beforehand. Anaconda
Python is a very large download.

## Lesson Data Files

The files used in this lesson can be downloaded:

* [Linux/Mac](files/workflow-engines-lesson.tar.gz)
* [Windows](files/workflow-engines-lesson.zip)

Once downloaded, please extract to the directory you wish to work in for all
the hands-on exercises.

Solutions for most episodes can be found in the `.solutions` directory inside
the code download.

A `requirements.txt` file is included in the download. As described below,
this can be used to install the required Python packages.

## Python 3 / Anaconda

You will need Python 3.6 or better to use the sample files, since some
relatively new Python features are used. Instructions are given here for
installing Anaconda, although any Python will work.

1. Visit the [Anaconda download page][anaconda]
2. Select your operating system (Windows, macOS, or Linux).
3. Download the Python 3 64-bit graphical installer.
4. After the download completes, run the installer to install Anaconda.

> ## Follow the Installation Guide
>
> If you need more detailed guidance, then please follow the [Anaconda
> Installation guide][anaconda-installation].
{: .callout}

### Updating Anaconda

1. Once Anaconda is installed, it is a good idea to update it.
2. The article [Keeping Anaconda Up To Date][anaconda-update] is a good guide to
   updating Anaconda after it is installed.
3. It boils down to opening an Anaconda terminal and running the command:

~~~
conda update --all
~~~
{: .source}

> ## Updating is not essential for this course
>
> If you would rather skip updating, then it is not essential for this course.
{: .callout}

### Additional Libraries

The example code also requires the `matplotlib` and `numpy` libraries. They
are installed by default with Anaconda, but if you are using a different
Python you may need to install them manually. Using `pip`, the command would
be:

~~~
pip install --user numpy matplotlib
~~~
{: .language-bash}

The example files download also contains a `requirements.txt` file that can
be used to specify the required packages for a Python virtual environment.
There are many guides to this process online, including the [official
documentation](https://docs.python.org/3/tutorial/venv.html).

## Snakemake

Once you have Python 3 available, you need to install the Snakemake library.

### Anaconda

You can install Snakemake at an Anaconda prompt:

~~~
conda install -c bioconda -c conda-forge snakemake-minimal
~~~
{: .language-bash}

> ## Note
> At the time of writing, the `snakemake` conda package was not installing correctly,
> however the `snakemake-minimal` was working. This lesson does not require any
> features beyond those included with the minimal install.
{: .callout}

### Vanilla Python

You can install Snakemake with:

~~~
pip install --user snakemake
~~~
{: .language-bash}

If you used the supplied `requirements.txt` to create a Python virtual
environment then `snakemake` should already be installed. For more
information, please refer to the [Snakemake installation
documentation](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html).

## Windows-Specific Instructions

Some of the commands used in this lesson assume that some common Linux
commands are available. These include `rm`, and `tar`. These commands are not
available by default on Windows systems. While there are many solutions,
including using the Windows Subsystem for Linux (WSL), a simple approach that
we have tested is to install Git for Windows. This installs a lightweight
command-line environment that contains the required Linux commands and can be
configured to use Anaconda Python.

First, download and install the Windows [Git client][git-win].

Then, add Anaconda to your Git Bash `$PATH`:

1. Open Git Bash from the Start Menu.
2. Run the following command: `export
PATH=$PATH:~/AppData/Local/Continuum/anaconda3/Scripts`
3. Run the following
command: `source activate`

Now you are good to go!

{% include links.md %}

[anaconda]: https://www.anaconda.com/distribution/
[anaconda-installation]: https://docs.anaconda.com/anaconda/install/
[anaconda-update]: https://www.anaconda.com/keeping-anaconda-date/
[git-win]: https://git-scm.com/download/win
