---
title: "Resources and parallelism"
teaching: 30
exercises: 15
questions:
- "How do I scale a pipeline across multiple cores?"
- "How do I manage access to resources while working in parallel?"
objectives:
- "Modify your pipeline to run in parallel."
keypoints:
- "Use `threads` to indicate the number of cores required by a rule."
- "Use the `-j` argument to Snakemake to indicate how many CPU cores can be used
for parallel tasks."
- "Resources are arbitrary and can be used for anything."
- "The `&&` operator is a useful tool when chaining bash commands."
- "While available resources will limit the total number of tasks that
can execute in parallel, Snakemake will attempt to run at least one
task even when sufficient resources are not available."
- "It is up to you to tell code how many resources it should be using."
---

After the exercises at the end of our last lesson, our Snakefile looks
something like this (note the `dats` and `print_book_names` rules are no
longer required so they have been removed):

~~~
# Build the list of book names. We need to use it multiple times when building
# the lists of files that will be built in the workflow
BOOK_NAMES = glob_wildcards('./books/{book}.txt').book

# The list of all dat files
DATS = expand('dats/{file}.dat', file=BOOK_NAMES)

# The list of all plot files
PLOTS = expand('plots/{file}.png', file=BOOK_NAMES)

# pseudo-rule that tries to build everything.
# Just add all the final outputs that you want built.
rule all:
    input: 'zipf_analysis.tar.gz'

# Generate summary table
rule zipf_test:
    input:
        cmd='zipf_test.py',
        dats=DATS
    output: 'results.txt'
    shell:  'python {input.cmd} {input.dats} > {output}'

# delete everything so we can re-run things
rule clean:
    shell: 'rm -rf dats/ plots/ *.dat results.txt zipf_analysis.tar.gz'

# Count words in one of the books
rule count_words:
    input:
        cmd='wordcount.py',
        book='books/{file}.txt'
    output: 'dats/{file}.dat'
    shell: 'python {input.cmd} {input.book} {output}'

# plot one word count dat file
rule make_plot:
    input:
        cmd='plotcount.py',
        dat='dats/{file}.dat'
    output: 'plots/{file}.png'
    shell: 'python {input.cmd} {input.dat} {output}'

# create an archive with all results
rule create_archive:
    input: 'results.txt', DATS, PLOTS
    output: 'zipf_analysis.tar.gz'
    shell: 'tar -czvf {output} {input}'
~~~
{:.language-python}

At this point, we have a complete data analysis pipeline. Very cool. But how
do we make it run as efficiently as possible?

## Running in parallel

Up to this point, Snakemake has printed out an interesting message whenever
we run our pipeline:

~~~
Provided cores: 1
Rules claiming more threads will be scaled down.
~~~
{: .output}

So far, Snakemake has been run in single-threaded mode, using just one CPU
core. This means that even when Snakemake can identify tasks that could run
at the same time, such as counting words in different books, it still runs
them one at a time. Let's see how to change that, and scale up our pipeline
to run in parallel.

The only change we need to make is run Snakemake with the `-j` argument. `-j`
tells Snakemake the maximum number or CPU cores that it can use.

~~~
snakemake clean
snakemake -j 4    # 4 cores is usually a safe assumption when working on a laptop/desktop
~~~
{:.language-bash}

~~~
Provided cores: 4
Rules claiming more threads will be scaled down.
# more output follows
~~~
{: .output}

Our pipeline ran in parallel and finished roughly 4 times as quickly! The
takeaway here is that all we need to do to scale from a serial pipeline is
run `snakemake` with the `-j` option. By analysing the dependencies between
rules, Snakemake automatically identifies which tasks can run at the same
time. All you need to do is describe your workflow and Snakemake does the
rest.

Note you can also use `snakemake --cores 4` or `snakemake --jobs 4`. The
`-j`, `--cores` and `--jobs` arguments all mean the same thing.

> ## How many CPUs does your computer have?
>
> Now that our pipeline can use multiple CPUs, how do we know how many CPUs
> to provide to the `-j` option? Note that for all of these options, it's
> best to use CPU cores, and not CPU threads.
>
> **Linux** - You can use the `lscpu` command. Look for the number listed alongside `CPU(s):`.
>
> **All platforms** - Python's `psutil` module can be used to fetch
> the number of cores in your computer.
> Using `logical=False` returns the number of true CPU cores.
> `logical=True` gives the number of CPU threads on your system.
>
> ~~~
> import psutil
> psutil.cpu_count(logical=False)
> ~~~
> {:.language-python}
>
{: .callout}

## Managing CPUs

Each rule has a number of optional keywords aside from the usual `input`,
`output`, and `shell`/`run`. The `threads` keyword is used to specify how
many CPU cores a rule needs while executing. Though in reality CPU threads
are not the same as CPU cores, the two terms are interchangeable when working
with Snakemake.

Let's pretend that our `count_words` rule is multithreaded and can run on 4
CPU cores. We can specify this with the `threads` keyword in our rule. We
will also modify the rule to print out the number of threads it thinks it is
using.

> ## Note
> Please note that just giving something 4 threads in Snakemake does not
> make it run in parallel! It just tells Snakemake to reserve that number
> of cores from the total available (indicated by the value passed to `-j`).
>
> In this case `wordcount.py` is actually still running with 1 core, we
> are simply using it as a demonstration of how to go about running
> something with multiple cores.
{:.callout}

~~~
rule count_words:
    input:
        cmd='wordcount.py',
        book='books/{file}.txt'
    output: 'dats/{file}.dat'
    threads: 4
    shell:
        '''
        echo "Running {input.cmd} with {threads} cores."
        python {input.cmd} {input.book} {output}
        '''
~~~
{:.language-python}

Now, when we run `snakemake -j 4`, the `count_words` rules are run one at a
time. All of our other rules will still run in parallel. Unless otherwise
specified with `{threads}`, rules will use 1 core by default.

~~~
Provided cores: 4
Rules claiming more threads will be scaled down.
Job counts:
	count	jobs
	1	all
	4	count_words
	1	make_archive
	4	make_plot
	1	zipf_test
	11

rule count_words:
    input: wordcount.py, books/last.txt
    output: dats/last.dat
    jobid: 3
    wildcards: file=last
    threads: 4

Running wordcount.py with 4 cores.
Finished job 3.
1 of 11 steps (9%) done

# other output follows
~~~
{:.output}

What happens when we don't have 4 cores available? What if we tell Snakemake
to run with 2 cores instead?

~~~
snakemake -j 2
~~~
{:.language-bash}

~~~
Provided cores: 2
Rules claiming more threads will be scaled down.
Job counts:
	count	jobs
	1	all
	4	count_words
	1	make_archive
	4	make_plot
	1	zipf_test
	11

rule count_words:
    input: wordcount.py, books/last.txt
    output: dats/last.dat
    jobid: 6
    wildcards: file=last
    threads: 2

Running wordcount.py with 2 cores.
Finished job 6.
1 of 11 steps (9%) done

# more output below
~~~
{: .output}

The answer is given by `Rules claiming more threads will be scaled down.`.
When Snakemake doesn't have enough cores to run a rule (as defined by
`{threads}`), Snakemake will run that rule with the maximum available number
of cores instead. After all, Snakemake's job is to get our workflow done. It
automatically scales our workload to match the maximum number of cores
available without us editing the Snakefile.

> ## Tasks Still Need to Know How Many Cores are Available
>
> How the number of threads required by a rule matches the number of cores
> allowed to Snakemake by the `-j N` argument determines how many instances
> of that rule Snakemake will run at the same time. It does not mean that
> the code being executed will magically know what the limits are.
>
> The previous code example showed how the `{threads}` wildcard can be used
> to get the actual number of cores allocated to an action.
> This value can be passed in as a command-line argument or set to an
> environment variable.
{:.callout}

## Chaining multiple commands

Up until now, all of our commands have fit on one line. To execute multiple
bash commands, the only modification we need to make is use a Python
multiline string (begin and end with `"""` or `'''`).

One important addition we should be aware of is the `&&` operator. `&&` is a
bash operator that runs commands as part of a chain. If the first command
fails, the remaining steps are not run. This is more forgiving than bash's
default "hit an error and keep going" behavior. After all, if the first
command failed, it's unlikely the other steps will work.

Let's modify `count_words` to chain the `echo` and `python` commands:
~~~
rule count_words:
    input:
        cmd='wordcount.py',
        book='books/{file}.txt'
    output: 'dats/{file}.dat'
    threads: 4
    shell:
        '''
        echo "Running {input.cmd} with {threads} cores." &&
        python {input.cmd} {input.book} {output}
        '''
~~~
{:.language-python}

Notice the use of the `{threads}` wildcard in the action to access the current
number of CPU cores allocated to the rule.

## Managing other types of resources

Not all compute resources are CPUs. Examples might include limited amounts of
RAM, number of GPUs, database locks, or perhaps we simply don't want multiple
processes writing to the same file at once. All non-CPU resources are handled
using the `resources` keyword.

For our example, let's pretend that creating a plot with `plotcount.py`
requires dedicated access to a GPU (it doesn't), and only one GPU is
available. How do we indicate this to Snakemake so that it knows to give
dedicated access to a GPU for rules that need it? Let's modify the
`make_plot` rule as an example:

~~~
rule make_plot:
    input:
        cmd='plotcount.py',
        dat='dats/{file}.dat'
    output: 'plots/{file}.png'
    resources: gpu=1
    shell: 'python {input.cmd} {input.dat} {output}'
~~~
{:.language-python}

We can execute our pipeline using the following (using 4 cores and 1 gpu):

~~~
snakemake clean
snakemake -j 4 --resources gpu=1
~~~
{:.language-bash}

~~~
Provided cores: 4
Rules claiming more threads will be scaled down.
Provided resources: gpu=1
# other output removed for brevity
~~~
{: .output}

Resources are entirely arbitrary - like wildcards, they can be named
anything. Snakemake knows nothing about them aside from the fact that they
have a name and a value. In this case `gpu` indicates simply that there is a
resource called `gpu` used by `make_plot`. We provided 1 `gpu` to the
workflow, and the `gpu` is considered in use as long as the rule is running.
Once the `make_plot` rule completes, the `gpu` it consumed is added back to
the pool of available `gpu`s. To be extra clear: `gpu` in this case does not
actually represent a GPU, it is an arbitrary limit used to prevent multiple
tasks that use a `gpu` from executing at the same time.

But what happens if we run our pipeline without specifying the number of GPUs?

~~~
snakemake clean
snakemake -j 4
~~~
{:.language-bash}

~~~
Provided cores: 4
Rules claiming more threads will be scaled down.
Unlimited resources: gpu
~~~
{: .output}

If you have specified that a rule needs a certain resource, but do not
specify how many you have, Snakemake will assume that the resources in
question are unlimited.

> ## What happens if Snakemake does not have enough resources?
>
> Modify your Snakefile and the snakemake arguments to test what
> happens when you have less resources available than the number
> required by a rule.
>
> For example, you might set `gpu=2` in `make_plot`, and then
> run `snakemake --resources gpu=1`.
>
> What do you think will happen? What actually happens?
>
> > ## Solution
> >
> > Similar to the case where a rule specifies more threads than are
> > available, the rule still runs.
> >
> > Resource constraints will limit the maximum number of rules that
> > Snakemake will attempt to run at the same time, but not the minimum.
> > Where sufficient resources are not available, Snakemake will still
> > run at least one task.
> >
> > Once again, it is up to the code being run by the rule to check that
> > sufficient resources are actually available.
> {:.solution}
{:.challenge}

> ## Other uses for `resources`
>
> Resources do not have to correspond to actual compute resources.
> Perhaps one rule is particularly I/O heavy,
> and it's best if only a limited number of these jobs run at a time.
> Or maybe a type of rule uses a lot of network bandwidth as it downloads data.
> In all of these cases, `resources` can be used to constrain access
> to arbitrary compute resources so that each rule can run efficiently.
>
> Snakemake will run your rules in such a way as to maximize throughput given your
> resource constraints.
{: .callout}

{% include links.md %}
