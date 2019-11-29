---
title: "Scaling a pipeline across a cluster"
teaching: 30
exercises: 15
questions:
- "How do I run my workflow on an HPC system?"
objectives:
- "Understand the Snakemake cluster job submission workflow."
keypoints:
- "Snakemake generates and submits its own batch scripts for your scheduler."
- "`localrules` defines rules that are executed locally, and never submitted to a cluster."
- "`$PATH` must be passed to Snakemake rules."
- "`nohup <command> &` prevents `<command>` from exiting when you log off."
---

Right now we have a reasonably effective pipeline that scales nicely on our
local computer. However, for the sake of this course, we'll pretend that our
workflow actually takes significant computational resources and needs to be
run on a [HPC cluster][ref-hpc-cluster].

> ## HPC cluster architecture
>
> Most HPC clusters are run using a [scheduler][ref-scheduler].
> The scheduler is a piece of software that decides when a job will run, and on which nodes.
> It allows a set of users to share a shared computing system as efficiently as possible.
> In order to use it, users typically must write their commands to be run into a shell script
> and then "submit" it to the scheduler.
>
> A good analogy would be a university's room booking system.
> No one gets to use a room without going through the booking system.
> The booking system decides which rooms people get based on their requirements
> (# of students, time allotted, etc.).
{: .callout}

Normally, moving a workflow to be run by a cluster scheduler requires a lot
of work. Batch scripts need to be written, and you'll need to monitor and
babysit the status of each of your jobs. This is especially difficult if one
batch job depends on the output from another. Even moving from one cluster to
another (especially ones using a different scheduler) requires a large
investment of time and effort - all the batch scripts from before need to be
rewritten.

Snakemake does all of this for you. All details of running the pipeline
through the cluster scheduler are handled by Snakemake - this includes
writing batch scripts, submitting, and monitoring jobs. In this scenario, the
role of the scheduler is limited to ensuring each Snakemake rule is executed
with the resources it needs.

We'll explore how to port our example Snakemake pipeline by example. Our
current Snakefile is shown below:

FIXME: update to match new sample code

~~~
# our zipf analysis pipeline
DATS = glob_wildcards('books/{book}.txt').book

rule all:
    input:
        'zipf_analysis.tar.gz'

# delete everything so we can re-run things
rule clean:
    shell:
        '''
        rm -rf results dats plots
        rm -f results.txt zipf_analysis.tar.gz
        '''

# count words in one of our "books"
rule count_words:
    input:
        wc='wordcount.py',
        book='books/{file}.txt'
    output: 'dats/{file}.dat'
    threads: 4
    shell:
        '''
        python {input.wc} {input.book} {output}
        '''

# create a plot for each book
rule make_plot:
    input:
        plotcount='plotcount.py',
        book='dats/{file}.dat'
    output: 'plots/{file}.png'
    resources: gpu=1
    shell:  'python {input.plotcount} {input.book} {output}'

# generate summary table
rule zipf_test:
    input:
        zipf='zipf_test.py',
        books=expand('dats/{book}.dat', book=DATS)
    output: 'results.txt'
    shell:  'python {input.zipf} {input.books} > {output}'

# create an archive with all of our results
rule make_archive:
    input:
        expand('plots/{book}.png', book=DATS),
        expand('dats/{book}.dat', book=DATS),
        'results.txt'
    output: 'zipf_analysis.tar.gz'
    shell: 'tar -czvf {output} {input}'
~~~
{:.language-python}

To run Snakemake on a cluster, we need to tell it how it to submit jobs. This
is done using the `--cluster` argument. In this configuration, Snakemake runs
on the cluster login node and submits jobs. Each cluster job executes a single
rule and then exits. Snakemake detects the creation of output files, and
submits new jobs (rules) once their dependencies are created.

## Transferring our workflow

FIXME: change to a CSIRO system (pearcey?)

Let's port our workflow to Compute Canada's Graham cluster as an example (you
will probably be using a different cluster, adapt these instructions to your
cluster). The first step will be to transfer our files to the cluster and log
on via SSH. Snakemake has a powerful archiving utility that we can use to
bundle up our workflow and transfer it.

~~~
snakemake clean
tar -czvf pipeline.tar.gz .
# transfer the pipeline via scp
scp pipeline.tar.gz yourUsername@graham.computecanada.ca:
# log on to the cluster
ssh -X yourUsername@graham.computecanada.ca
~~~
{:.language-bash}

At this point we've archived our entire pipeline, sent it to the cluster, and
logged on. Let's create a folder for our pipeline and unpack it there.

~~~
mkdir pipeline
mv pipeline.tar.gz pipeline
cd pipeline
tar -xvzf pipeline.tar.gz
~~~
{:.language-bash}

FIXME: for pearcey, snakemake is installed, so direct to the appropriate module

If Snakemake and Python are not already installed on your cluster, you can
install them using the following commands:

~~~
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b
echo 'export PATH=~/miniconda3/bin:~/.local/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
conda install -y matplotlib numpy graphviz
pip install --user snakemake
~~~
{:.language-bash}

Assuming you've transferred your files and everything is set to go, the
command `snakemake -n` should work without errors.

## Cluster configuration with `cluster.json`

Snakemake uses a JSON-formatted configuration file to retrieve cluster
submission parameters. An example (using SLURM) is shown below. You can check
to see if your `cluster.json` is valid JSON syntax by pasting its contents
into the box at [jsonlint.com](https://jsonlint.com).

~~~
{
    "__default__":
    {
        "time": "0:5:0",
        "mem": "1G"
	},
    "count_words":
    {
        "time": "0:10:0",
        "mem": "2G"
    }
}
~~~
{:.language-json}

This file has several components. The values under `__default__` represent a
set of default configuration values that will be used for all rules. The
defaults won't always be perfect, however - chances are some rules may need
to run with non-default amounts of memory, cores, or time limits. We are
using the `count_words` rule as an example of this.

This is sufficient configuration for these exercises. For more information,
please consult the [Cluster Configuration][cluster-config-docs] documentation.

## Local rule execution

Some Snakemake rules perform trivial tasks where job submission might be
overkill (i.e. less than 1 minute worth of compute time). It would be a
better idea to have these rules execute locally (i.e. where the `snakemake`
command is run) instead of as a job. Snakemake lets you indicate which rules
should run always run locally with the `localrules` keyword. Let's define
`all`, `clean`, and `make_archive` as local rules near the top of our
`Snakefile`.

~~~
localrules: all, clean, make_archive
~~~
{:.language-python}

## Running our workflow on the cluster

Ok, time for the moment we've all been waiting for - let's run our workflow
on the cluster. To run our Snakefile, we'll run the following command:

~~~
snakemake -j 100 --cluster-config cluster.json --cluster "sbatch -A {cluster.account} --mem={cluster.mem} -t {cluster.time} -c {threads}"
~~~
{:.language-bash}

While things execute, you may wish to SSH to the cluster in another window so
you can watch the pipeline's progress with `watch squeue -u $(whoami)`.

Now, let's dissect the command we just ran:

* **`-j 100`** - `-j` no longer controls the number of cores when running on a
cluster. Instead, it controls the maximum number of jobs that snakemake can
have submitted at a time. This does not come into play here, but generally a
sensible default is slightly below the maximum number of jobs you are allowed
to have submitted at a time on your system.

* **`--cluster-config`** - This specifies the location of a JSON file to read
cluster configuration values from. This should point to the `cluster.json`
file we wrote earlier.

* **`--cluster`** - This is the submission command that should be used for the
scheduler. Note that command flags that normally are put in batch scripts are
put here (most schedulers allow you to add submission flags like this when
submitting a job). In this case, all of the values come from our
`--cluster-config` file. You can access individual values with
`{cluster.propertyName}`. Note that we can still use `{threads}` here.
When submitting jobs, Snakemake will use the current value of `threads` given
in the Snakefile for each rule.

> ## Notes on `$PATH`
>
> As with any cluster jobs, jobs started by Snakemake need to have the commands
> they are running on `$PATH`. For some schedulers (SLURM), no modifications
> are necessary - variables are passed to the jobs by default. You just need to
> load all the required environment modules prior to running Snakemake.
{:.callout}

> ## Submitting a workflow with nohup
>
> `nohup some_command &` runs a command in the background and lets it keep
> running if you log off. Try running the pipeline in cluster mode using
> `nohup` (run `snakemake clean` beforehand).
>
> Where does the Snakemake log go to?
>
> Why might this technique be useful?
>
> You can kill the running Snakemake process with `killall snakemake`.
> Notice that if you try to run Snakemake again, it says the directory is locked.
> You can unlock the directory with `snakemake --unlock`.
{: .challenge}

> ## Running Snakemake itself as a batch job
>
> Can we also submit the `snakemake --cluster` pipeline as a batch job?
>
> Is this a good idea? What are some problems of this approach?
{:.discussion}

[ref-hpc-cluster]: {{ relative_root_path }}/reference#hpc-cluster
[ref-scheduler]: {{ relative_root_path }}/reference#scheduler
[cluster-config-docs]: https://snakemake.readthedocs.io/en/stable/snakefiles/configuration.html#cluster-configuration

{% include links.md %}
