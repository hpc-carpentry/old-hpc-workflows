---
title: "Make your workflow portable and reduce duplication"
teaching: 15
exercises: 15
questions:
- "How can I eliminate duplicated file names and paths in my workflows?"
- "How can I make my workflows portable and easily shared?"
objectives:
- "Learn to use configuration files to make workflows portable."
- "Learn a safe way to mix global variables and snakemake wildcards."
- "Learn to use configuration files, global variables, and wildcards in a
systematic way to reduce duplication and make your workflows less error-prone."
keypoints:
---

Duplication in file names, paths, and pattern strings is a common source of
errors in snakefiles. For example, have a look at how often the directory
names are mentioned (`dats`, `plots` etc) in the examples from this workshop.

This episode presents a pattern for reducing file name duplication and making
your workflows less error-prone. In addition, this approach makes your
workflows more portable by moving all configurable items into a separate
configuration file.

For these exercises, you should start with either your completed Snakefile
from the end of the previous episode, or else use the example Snakefile
`.solutions/episode_09/Snakefile-start`. Copy it to your working directory
and rename to `Snakefile`.

## Use Configuration Files

The first step in this pattern is to move all values that need to be
configurable into a configuration file alongside the Snakefile. While Snakemake
supports `json` and `yaml` formats, we use `yaml` here as it is easier to edit and
read.

~~~
# Use a trailing slash on directories so that an empty string will work to indicate
# the current working directory
input_dir: books/
plot_dir: plots/
dat_dir: dats/
results_file: results.txt
archive_file: zipf_analysis.tar.gz
~~~
{:.language-yaml}

One way to reduce this is to increase the use of global variables at the
start of the Snakefile to define all the configurable parts of your workflow.
However, this requires some extra care when combining the global variables
and Snakemake wildcards in your rule definitions. Let's see it in action
first. In this extract from our workflow we introduce a global variable for
the input directory and then use string formatting to define the
`count_words` rule:

{% raw %}
~~~
INPUT_DIR = 'books/'

rule count_words:
    input:
        cmd='wordcount.py',
        book=f'{INPUT_DIR}{{book}}.txt'
    output: 'dats/{book}.dat'
    shell: 'python {input.cmd} {input.book} {output}'
~~~
{:.language-python}

The key points are:
* The input directory is only specified in a single place.
* When wildcards and global variables are combined in a single string (`input.book`),
a Python f-string is used, and the wildcard is surrounded by double braces
(`{{book}}`).
* When you are just using wildcards (the `shell` section), you can use the standard
Snakemake notation.
{% endraw %}

This can be taken further by moving the hardcoded value for `INPUT_DIR` into a
configuration file. For example:

**config.yaml**:
~~~
input_dir: books/
~~~
{:.language-json}

In the Snakefile, a config is loaded with `configfile` and then values are accessed
from the `config` dictionary:
~~~
configfile: 'config.yaml'

INPUT_DIR = config['input_dir']
~~~
{:.language-python}

This is particularly useful when sharing a workflow with others, or running in different
environments where file locations or other parameters may not be the same.

> ## Full Example
>
> A full example of the entire workflow with no duplication and all configurable values moved
> into a configuration file can be viewed in the `.solutions/episode_09` directory of the
> downloaded code package.
>
> Note that the example uses [f-strings][f-string], which are only available from Python 3.6.
> If you must use an older version of Python then you can use the older string formatting
> methods, although the results will be less concise.
{:.callout}

## dry-run is your friend

Whenever you edit your Snakefile, you should perform a dry-run with
`snakemake clean && snakemake -n` or `snakemake clean && snakemake --dry-run`
immediately afterwards. This will check for errors and make sure that the
pipeline is able to run. The clean is required to force the dry run to test
the entire pipeline.

The most common source of errors is a mismatch in filenames (Snakemake
doesn't know how to produce a particular output file) - `snakemake -n` will
catch this as long as the troublesome output files haven't already been made,
and the `snakemake clean` should take care of that.

## Configuring logging

By default, Snakemake prints all output from stderr and stdout from rules.
This is useful, but if a failure occurs (or we otherwise need to inspect the
logs) it can be extremely difficult to determine what happened or which rule
had an issue, especially when running in parallel.

The solution to this issue is to redirect the output from each rule/ set of
inputs to a dedicated logfile. We can do this using the `log` keyword. Let's
modify our `count_words` rule to be slighly more verbose and redirect this
output to a dedicated logfile.

Two things before we start:

* `&>` is a handy operator in bash that redirects both stdout and stderr to a file.
* `&>>` does the same thing as `&>`, but appends to a file instead of overwriting it.

~~~
# count words in one of our "books"
rule count_words:
    input:
        wc='wordcount.py',
        book='books/{file}.txt'
    output: 'dats/{file}.dat'
    threads: 4
    log: 'dats/{file}.log'
    shell:
        '''
        echo "Running {input.wc} with {threads} cores on {input.book}." &> {log}
        python {input.wc} {input.book} {output} &>> {log}
        '''
~~~
{:.language-python}

~~~
snakemake clean
snakemake -j 8
cat dats/abyss.log
~~~
{:.language-bash}

~~~
# snakemake output omitted
Running wordcount.py with 4 cores on books/abyss.txt.
~~~
{: .output}

Notice how the pipeline no longer prints to the terminal output, and instead
redirects to a logfile.

> ## Choosing a good log file location
>
> Though you can put a log anywhere (and name it anything),
> it is often a good practice to put the log in the same directory
> where the rule's output will be created.
> If you need to investigate the output for a rule and associated logfiles,
> this means that you only have to check one location!
{: .callout}

## Token files

Often, a rule does not generate a unique output, and merely modifies a file.
In these cases it is often worthwhile to create a placeholder, or "token
file" as output. A token file is simply an empty file that you can create
with the touch command (`touch some_file.txt` creates an empty file called
`some_file.txt`).

You can then use the token file as an input to other rules that shouldn't run
until after the rule that generates the token.

An example rule using this technique is shown below:

~~~
rule token_example:
    input:  'some_file.txt'
    output: 'some_file.tkn'   # marks some_file.txt as modified
    shell:
        '''
        some_command --do-things {input} &&
            touch {output}
        '''
~~~
{:.language-python}

## Directory locks

Only one instance of Snakemake can run in a directory at a time. If a
Snakemake run fails without unlocking the directory (if you killed the
process, for instance), you can run `snakemake --unlock` to unlock it.

## Python as a fallback

Remember, you can use Python imports and functions anywhere in a Snakefile.
If something seems a little tricky to implement - Python can do it. The `os`,
`shutil`, and `subprocess` packages are useful tools for using Python to
execute command line actions. In particular, `os.system('some command')` will
run a command on the command-line and block until execution is complete.

## Creating a workflow diagram

Assuming graphviz is installed (`conda install graphviz`), you can create a
diagram of your workflow with the command: `snakemake --dag | dot -Tsvg >
dag.svg`. This creates a plot of your "directed acyclic graph" (a plot of all
of the rules Snakemake thinks it needs to complete), which you can view using
any picture viewing program. In fact this was the tool used to create all of
the diagrams in this lesson:

~~~
snakemake --dag | dot -Tsvg > dag.svg
eog dag.svg     # eog is an image viewer installed on many linux systems
~~~
{:.language-bash}

![Example DAG plot](../fig/06-final-dag.svg)

Rules that have yet to be completed are indicated with solid outlines.
Already completed tasks will be indicated with dashed outlines. In this case,
I ran `snakemake clean`, just before creating the diagram - no rules have
been run yet.

> ## CSIRO Clusters
>
> On CSIRO clusters, you can load the `imagemagick` module to view the
> diagrams:
> ~~~
> module load imagemagick
> snakemake --dag | dot -Tpng | display
> ~~~
> {:.language-bash}
{:.callout}

## Viewing the GUI

Snakemake has an experimental web browser GUI. I personally haven't used it
for anything, but it's cool to know it's there and can be used to view your
workflow on the fly.

`snakemake --gui`

Note that this requires the installation of additional Python packages.

## Where to go for documentation / help

The Snakemake documentation is located at
[snakemake.readthedocs.io](http://snakemake.readthedocs.io)

{% include links.md %}

[f-string]: https://docs.python.org/3/reference/lexical_analysis.html#f-strings