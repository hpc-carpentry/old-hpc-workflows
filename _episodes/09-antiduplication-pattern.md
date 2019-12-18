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

## Identify Duplicated Paths

First, examine the Snakefile to identify duplicated file names, paths, and patterns.
Move each one to a common global variable at the top of the Snakefile.

For example, we currently refer to single input books in two locations:

~~~
BOOK_NAMES = glob_wildcards('books/{book}.txt').book
~~~
{:.language-python}

~~~
rule count_words:
    input:
        cmd='wordcount.py',
        book='books/{file}.txt'
~~~
{:.language-python}

The different wildcard names (`{book}, {file}`) are a distraction. Both
patterns refer to an input file.

Similarly, the strings that identify a single plot and a single dat file
are duplicated.

> ## Identify Duplication
> How many times does the dat file pattern occur?
> > ## Solution
> >
> > Three times.
> > ~~~
> > DATS = expand('dats/{file}.dat', file=BOOK_NAMES)
> > ~~~
> > {:.language-python}
> > ~~~
> > rule count_words:
> >     input:
> >         cmd='wordcount.py',
> >         book='books/{file}.txt'
> >     output: 'dats/{file}.dat'
> >     shell: 'python {input.cmd} {input.book} {output}'
> > ~~~
> > {:.language-python}
> > ~~~
> > rule make_plot:
> >     input:
> >         cmd='plotcount.py',
> >         dat='dats/{file}.dat'
> >     output: 'plots/{file}.png'
> >     shell: 'python {input.cmd} {input.dat} {output}'
> > ~~~
> > {:.language-python}
> {:.solution}
{:.challenge}

Once duplicated file patterns have been identified, they can be moved to
global variables at the start of the Snakefile and then just refered to by
name.

Here is what the changes for input files might look like:

~~~
# a single input book
BOOK_FILE = 'books/{book}.txt'

# Build the list of book names.
BOOK_NAMES = glob_wildcards(BOOK_FILE).book

rule count_words:
    input:
        cmd='wordcount.py',
        book=BOOK_FILE
    output: 'dats/{book}.dat'
    shell: 'python {input.cmd} {input.book} {output}'
~~~
{:.language-python}

Note that we have adopted `{book}` as the wildcard name, rather than the
inconsistent use of `{book}` and `{file}`.

> ## Global variables also work for `glob_wildcards` and `expand`
>
> Another point to note is the previous code used `BOOK_FILE` for a rule input
> and for a call to `glob_wildcards`. Remember this when updating the calls to
> `expand` in the next challenge.
{:.callout}

> ## Replace all other duplicated strings with global variables
>
> You will need to update:
> * the string for `dat` files (`dats/{file}.dat`)
> * the string for plot files (`plots/{file}.png`)
> * the archive file `zipf_analysis.tar.gz`
> * the results file `results.txt`
>
> > ## Solution
> >
> > This solution is also available as `.solutions/episode_09/Snakefile-remove-duplicates`.
> > Possibly the only tricky part is in the `clean` rule where we use
> > a formatted Python string to build the global variables into the shell
> > command. We used f-string notation, but `string.format` would also work.
> >
> > ~~~
> > RESULTS_FILE = 'results.txt'
> > ARCHIVE_FILE = 'zipf_analysis.tar.gz'
> >
> > # a single plot file
> > PLOT_FILE = 'plots/{book}.png'
> >
> > # a single dat file
> > DAT_FILE = 'dats/{book}.dat'
> >
> > # a single input book
> > BOOK_FILE = 'books/{book}.txt'
> >
> > # Build the list of book names.
> > BOOK_NAMES = glob_wildcards(BOOK_FILE).book
> >
> > # The list of all dat files
> > DATS = expand(DAT_FILE, book=BOOK_NAMES)
> >
> > # The list of all plot files
> > PLOTS = expand(PLOT_FILE, book=BOOK_NAMES)
> >
> > # pseudo-rule that tries to build everything.
> > # Just add all the final outputs that you want built.
> > rule all:
> >     input: ARCHIVE_FILE
> >
> > # Generate summary table
> > rule zipf_test:
> >     input:
> >         cmd='zipf_test.py',
> >         dats=DATS
> >     output: RESULTS_FILE
> >     shell:  'python {input.cmd} {input.dats} > {output}'
> >
> > # delete everything so we can re-run things
> > rule clean:
> >     shell: f'rm -rf dats/ plots/ {RESULTS_FILE} {ARCHIVE_FILE}'
> >
> > # Count words in one of the books
> > rule count_words:
> >     input:
> >         cmd='wordcount.py',
> >         book=BOOK_FILE
> >     output: DAT_FILE
> >     shell: 'python {input.cmd} {input.book} {output}'
> >
> > # plot one word count dat file
> > rule make_plot:
> >     input:
> >         cmd='plotcount.py',
> >         dat=DAT_FILE
> >     output: PLOT_FILE
> >     shell: 'python {input.cmd} {input.dat} {output}'
> >
> > # create an archive with all results
> > rule create_archive:
> >     input: RESULTS_FILE, DATS, PLOTS
> >     output: ARCHIVE_FILE
> >     shell: 'tar -czvf {output} {input}'
> > ~~~
> > {:.language-python}
> {:.solution}
{:.challenge}

## -----------------------------------------------

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

{% include links.md %}

[f-string]: https://docs.python.org/3/reference/lexical_analysis.html#f-strings