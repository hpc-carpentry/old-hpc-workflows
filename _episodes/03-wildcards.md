---
title: "Wildcards"
teaching: 30
exercises: 20
questions:
- "How can I abbreviate the rules in my pipeline?"
objectives:
- "Use Snakemake wildcards to simplify our rules."
- "Understand that outputs depend not only on the input data files but
also on the scripts or code."
keypoints:
- "Use `{output}` to refer to the output of the current rule."
- "Use `{input}` to refer to the dependencies of the current rule."
- "You can use Python indexing to retrieve individual outputs and inputs
(example: `{input[0]}`)"
- "Wildcards can be named (example: `{input.file1}`)."
- "Naming the code or scripts used by a rule as inputs ensures that the rule
is executed if the code or script changes."
---

After the exercise at the end of the previous episode, our Snakefile looked like this:

~~~
# Generate summary table
rule zipf_test:
    input:
        'isles.dat',
        'abyss.dat',
        'last.dat'
    output: 'results.txt'
    shell: 'python zipf_test.py abyss.dat isles.dat last.dat > results.txt'

rule dats:
    input:
        'isles.dat',
        'abyss.dat',
        'last.dat'

# delete everything so we can re-run things
rule clean:
    shell: 'rm -f *.dat results.txt'

# Count words in one of the books
rule count_words:
    input: 'books/isles.txt'
    output: 'isles.dat'
    shell: 'python wordcount.py books/isles.txt isles.dat'

rule count_words_abyss:
    input: 'books/abyss.txt'
    output: 'abyss.dat'
    shell: 'python wordcount.py books/abyss.txt abyss.dat'

rule count_words_last:
    input: 'books/last.txt'
    output: 'last.dat'
    shell: 'python wordcount.py books/last.txt last.dat'
~~~
{: .language-python}

This has a lot of duplication. For example, the names of text
files and data files are repeated in many places throughout the
Snakefile. Snakefiles are a form of code and, in any code, repetition
can lead to problems (e.g. we rename a data file in one part of the
Snakefile but forget to rename it elsewhere).

> ## D.R.Y. (Don't Repeat Yourself)
>
> In many programming languages, the bulk of the language features are
> there to allow the programmer to describe long-winded computational
> routines as short, expressive, beautiful code.  Features in Python,
> R, or Java, such as user-defined variables and functions are useful in
> part because they mean we don't have to write out (or think about)
> all of the details over and over again.  This good habit of writing
> things out only once is known as the "Don't Repeat Yourself"
> principle or D.R.Y.
{: .callout}

Let us set about removing some of the repetition from our Snakefile.
In our `zipf_test` rule we duplicate the data file names and the
name of the results file name:

~~~
rule zipf_test:
    input:  'abyss.dat', 'last.dat', 'isles.dat'
    output: 'results.txt'
    shell: 'python zipf_test.py abyss.dat isles.dat last.dat > results.txt'
~~~
{: .language-python}

Looking at the results file name first, we can replace it in the action
with `{output}`:

~~~
rule zipf_test:
    input:  'abyss.dat', 'last.dat', 'isles.dat'
    output: 'results.txt'
    shell:  'python zipf_test.py abyss.dat isles.dat last.dat > {output}'
~~~
{: .language-python}

`{output}` is a Snakemake [wildcard][ref-wildcard] which is equivalent to the
value we specified for the rule output.

We can replace the dependencies in the action with `{input}`:

~~~
rule zipf_test:
    input:  'abyss.dat', 'last.dat', 'isles.dat'
    output: 'results.txt'
    shell:  'python zipf_test.py {input} > {output}'
~~~
{: .language-python}

`{input}` is another wildcard which means 'all the inputs
of the current rule'. Again, when Snakemake runs it will replace this
variable with the actual inputs.

Let's update our text files and re-run our rule:

~~~
touch books/*.txt
snakemake results.txt
~~~
{: .language-bash}

We get:

~~~
Provided cores: 1
Rules claiming more threads will be scaled down.
Job counts:
	count	jobs
	1	count_words
	1	count_words_abyss
	1	count_words_last
	1	zipf_test
	4

rule count_words_last:
    input: books/last.txt
    output: last.dat
    jobid: 1

Finished job 1.
1 of 4 steps (25%) done

rule count_words_abyss:
    input: books/abyss.txt
    output: abyss.dat
    jobid: 2

Finished job 2.
2 of 4 steps (50%) done

rule count_words:
    input: books/isles.txt
    output: isles.dat
    jobid: 3

Finished job 3.
3 of 4 steps (75%) done

rule zipf_test:
    input: abyss.dat, last.dat, isles.dat
    output: results.txt
    jobid: 0

Finished job 0.
4 of 4 steps (100%) done
~~~
{: .output}

> ## Update Dependencies
>
> What will happen if you now execute:
>
> ~~~
> touch *.dat
> snakemake results.txt
> ~~~
> {: .language-bash}
>
>
> 1. nothing
> 2. all files recreated
> 3. only `.dat` files recreated
> 4. only `results.txt` recreated
>
> > ## Solution
> > Only `results.txt` recreated.
> >
> > The rules for `*.dat` are not executed because their corresponding `.txt` files
> > haven't been modified.
> >
> > If you run:
> >
> > ~~~
> > touch books/*.txt
> > snakemake results.txt
> > ~~~
> >{: .language-bash}
> >
> >
> > you will find that the `.dat` files as well as `results.txt` are recreated.
> {: .solution}
{: .challenge}

As we saw, `{input}` means 'all the dependencies of the current rule'. This
works well for `results.txt` as its action treats all the dependencies the
same - as the input for the `zipf_test.py` script.

Time for you to update all the rules that build a `.dat` file to use the
`{input}` and `{output}` wildcards.

> ## Rewrite `.dat` rules to use wildcards
>
> Rewrite each `.dat` rule to use the `{input}` and `{output}` wildcards.
> > ## Solution
> > Only one rule is shown here, the others follow the same pattern:
> > ~~~
> > rule count_words:
> >     input: 'books/isles.txt'
> >     output: 'isles.dat'
> >     shell: 'python wordcount.py {input} {output}'
> > ~~~
> > {: .language-python}
> {: .solution}
{: .challenge}

## Handling dependencies differently

For many rules, we will need to make finer distinctions between inputs. It is
not always appropriate to pass all inputs as a lump to your action. For
example, our rules for `.dat` use their first (and only) dependency
specifically as the input file to `wordcount.py`. If we add additional
dependencies (as we will soon do) then we don't want these being passed as
input files to `wordcount.py`: it expects just one input file.

Let's see this in action. We need to add `wordcount.py` as a dependency of
each of our data files so that the rules will be executed if the script
changes. In this case, we can use `{input[0]}` to refer to the first
dependency, and `{input[1]}` to refer to the second.

~~~
rule count_words:
    input: 'wordcount.py', 'books/isles.txt'
    output: 'isles.dat'
    shell: 'python {input[0]} {input[1]} {output}'
~~~
{: .language-python}

Alternatively, we can name our dependencies.

~~~
rule count_words_abyss:
    input:
        cmd='wordcount.py',
        book='books/abyss.txt'
    output: 'abyss.dat'
    shell: 'python {input.cmd} {input.book} {output}'
~~~
{: .language-python}

Let's mark `wordcount.py` as updated, and re-run the pipeline:

~~~
touch wordcount.py
snakemake
~~~
{: .language-bash}

~~~
Provided cores: 1
Rules claiming more threads will be scaled down.
Job counts:
	count	jobs
	1	count_words
	1	count_words_abyss
	1	zipf_test
	3

rule count_words_abyss:
    input: wordcount.py, books/abyss.txt
    output: abyss.dat
    jobid: 2

Finished job 2.
1 of 3 steps (33%) done

rule count_words:
    input: wordcount.py, books/isles.txt
    output: isles.dat
    jobid: 1

Finished job 1.
2 of 3 steps (67%) done

rule zipf_test:
    input: abyss.dat, last.dat, isles.dat
    output: results.txt
    jobid: 0

Finished job 0.
3 of 3 steps (100%) done
~~~
{: .output}

Notice how `last.dat` (which does not depend on `wordcount.py`) is not
rebuilt.

Intuitively, we should also add `wordcount.py` as dependency for
`results.txt`, as the final table should be rebuilt if we remake the `.dat`
files. However, it turns out we don't have to! Let's see what happens to
`results.txt` when we update `wordcount.py`:

~~~
touch wordcount.py
snakemake results.txt
~~~
{: .language-bash}

then we get:

~~~
Provided cores: 1
Rules claiming more threads will be scaled down.
Job counts:
	count	jobs
	1	count_words
	1	count_words_abyss
	1	zipf_test
	3

rule count_words_abyss:
    input: wordcount.py, books/abyss.txt
    output: abyss.dat
    jobid: 2

Finished job 2.
1 of 3 steps (33%) done

rule count_words:
    input: wordcount.py, books/isles.txt
    output: isles.dat
    jobid: 1

Finished job 1.
2 of 3 steps (67%) done

rule zipf_test:
    input: abyss.dat, last.dat, isles.dat
    output: results.txt
    jobid: 0

Finished job 0.
3 of 3 steps (100%) done
~~~
{: .output}

The whole pipeline is triggered, even the creation of the `results.txt` file!
To understand this, note that according to the dependency graph,
`results.txt` depends on the `.dat` files. The update of `wordcount.py`
triggers an update of the `*.dat` files. Thus, `Snakemake` sees that the
dependencies (the `.dat` files) are newer than the target file
(`results.txt`) and thus it recreates `results.txt`. This is an example of
the power of `Snakemake`: updating a subset of the files in the pipeline
triggers rerunning the appropriate downstream steps.

> ## Updating One Input File
>
> What will happen if you now execute:
>
> ~~~
> touch books/last.txt
> snakemake results.txt
> ~~~
> {: .language-bash}
>
> 1. only `last.dat` is recreated
> 2. all `.dat` files are recreated
> 3. only `last.dat` and `results.txt` are recreated
> 4. all `.dat` and `results.txt` are recreated
>
> > ## Solution
> >
> > `3.` only `last.dat` and `results.txt` are recreated
> {: .solution}
{: .challenge}

> ## Update `count_words_last` to depend on `wordcount.py`
>
> Use either indexed or named inputs.
{: .challenge}

> ## Updating `zipf_test` rule
>
> Add `zipf_test.py` as a dependency of `results.txt`
> We haven't yet covered the techniques required to do this with named wildcards
> so you will have to use indexing.
> Yes, this will be clunky, but we'll fix that part later!
> Remember that you can do a dry run with `snakemake -n -p`!
>
> > ## Solution
> >
> >~~~
> > rule zipf_test:
> >     input:  'zipf_test.py', 'isles.dat', 'abyss.dat', 'last.dat'
> >     output: 'results.txt'
> >     shell:  'python {input[0]} {input[1]} {input[2]} {input[3]} > {output}'
> >~~~
> >{:.language-python}
> {: .solution}
{: .challenge}

[ref-wildcard]: {{ relative_root_path }}/reference#wildcard

{% include links.md %}
