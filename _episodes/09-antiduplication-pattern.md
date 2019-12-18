---
title: "Make your workflow portable and reduce duplication"
teaching: 15
exercises: 20
questions:
- "How can I eliminate duplicated file names and paths in my workflows?"
- "How can I make my workflows portable and easily shared?"
objectives:
- "Learn to use configuration files to make workflows portable."
- "Learn a safe way to mix global variables and snakemake wildcards."
- "Learn to use configuration files, global variables, and wildcards in a
systematic way to reduce duplication and make your workflows less error-prone."
keypoints:
- "Careful use of global variables can eliminate duplication of file names
and patterns in your Snakefiles"
- "Consistent naming conventions help keep your code readable."
- "Configuration files can make your workflow portable."
-
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

## Removing Duplication

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
> > ## Hint
> >
> > * A formatted string can be used to get the global variables into the `clean`
> > shell command.
> > * If you have inconsistent wildcard names, make them the same.
> {:.solution}
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
> > ALL_DATS = expand(DAT_FILE, book=BOOK_NAMES)
> >
> > # The list of all plot files
> > ALL_PLOTS = expand(PLOT_FILE, book=BOOK_NAMES)
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
> >         dats=ALL_DATS
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
> >     input: RESULTS_FILE, ALL_DATS, ALL_PLOTS
> >     output: ARCHIVE_FILE
> >     shell: 'tar -czvf {output} {input}'
> > ~~~
> > {:.language-python}
> {:.solution}
{:.challenge}

## The Benefits So Far

These changes bring a lot of benefits to Snakefiles, and most of these
benefits increase as your Snakefiles become more complex. Defining each file
pattern just once reduces the chance of error, and makes changing patterns
easier. Having all the file patterns and lists defined at the start of the
file also makes things easier to read. Finally, using the global variable
names elsewhere in the file tends to make rules easier to read. Instead of
trying to remember what the right pattern is, or what a given pattern means,
the extra level of abstraction should improve readability. For example, the `create_archive` rule now looks something like this:

~~~
rule create_archive:
    input: RESULTS_FILE, ALL_DATS, ALL_PLOTS
    output: ARCHIVE_FILE
    shell: 'tar -czvf {output} {input}'
~~~
{:.language-python}

The intent of the rule should be clear, and the intricacies of paths and file
name patterns are not confusing things.

> ## Use Consistent Naming Conventions
>
> I suggest the following global variable naming conventions:
>
> * `*_FILE` for single files or wildcard patterns
> * `ALL_*` for lists of files (frequently build using `expand`)
>
> You can of course use your own conventions. Consistency is the key.
{:.callout}

## Improving Portability

Imagine that we now want to share this workflow with a colleague, but they
have their input files in a different location. Additionally, they require a
different directory layout for the results, and a different results file
name.

In other words, they think our workflow is great, but they want to customise
and configure it.

Of course, they can just modify the Snakefile, but this can get annoying when
the Snakefile is shared (such as through a shared directory or via Git).

A better approach is to use configuration files. Snakemake supports `json`
and `yaml` formats, we use `yaml` here as it is easier to edit and read.

First, move all values that need to be configurable into a configuration file
alongside the Snakefile. Here we show the input file directory that has been
added to `config.yaml`:

~~~
input_dir: books/
~~~
{:.language-yaml}

In the Snakefile we first load the configuration with the `configfile` keyword:

~~~
configfile: 'config.yaml'
~~~
{:.language-python}

Once that has been done, the configuration is accessed through the `config` dictionary created by Snakemake:

~~~
INPUT_DIR = config['input_dir']
~~~
{:.language-python}

Finally, we use Python string formatting to build `BOOK_FILE`. Note that the
we need to escape the wildcard in double curly braces. This ensures the
formatted string contains `{book}`. Failure to do this will cause an
exception since the string formatting code will be expecting a token called
`book`.

{% raw %}
~~~
BOOK_FILE = f'{INPUT_DIR}{{book}}.txt'
~~~
{:.language-python}
{% endraw %}

> ## Combining global variables and wildcards in formatted strings
>
> The safest way to mix global variables and wildcards in a formatted string
> is to remember the following:
>
> * Global variables are surrounded in single curly braces (e.g. `{INPUT_DIR}`).
> * Wildcards are surrounded with double curly braces (`{{book}}`).
> * Use upper-case for globals and lower-case for wildcards.
{:.callout}

> ## Make your workflow configurable
>
> Move all other configurable values into `config.yaml` and adjust the Snakefile.
>
> Remember to test your workflow as you go.
>
> > ## Solution
> >
> > No example code is given here. By this stage you should be able to trust your
> > own judgement.
> >
> > If you really need it, a full example of the entire workflow with no
> > duplication and all configurable values moved into a configuration file
> > is in `.solutions/episode_09/Snakefile` and
> > `.solutions/episode_09/config.yaml` in the downloaded code package.
> >
> > Note that the example uses [f-strings][f-string], which are only available from Python 3.6.
> > If you must use an older version of Python then you can use the older string formatting
> > methods, although the results will be less concise.
> {:.solution}
{:.challenge}

> ## Don't put your configuration file in source control
>
> Instead:
> * create a sample configuration with a different name such as `config_template.yaml`.
> * instruct users to copy the template to the real configuration file (`config.yaml`).
> * make sure the configuration file name is in the `.gitignore` file (or equivalent).
{:.callout}

{% include links.md %}

[f-string]: https://docs.python.org/3/reference/lexical_analysis.html#f-strings