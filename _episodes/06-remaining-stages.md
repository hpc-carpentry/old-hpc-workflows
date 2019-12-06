---
title: "Completing the Pipeline"
teaching: 5
exercises: 20
questions:
- "How do I add new processing rules to a Snakefile?"
- "What are some common practices for Snakemake?"
- "How can I get my workflow to clean up generated files?"
- "What is a default rule?"
objectives:
- "Add a rule to your Snakefile that generates PNG plots of word frequencies."
- "Add an `all` rule to your Snakefile."
- "Make `all` the default rule."
keypoints:
- "It is common practice to have a `clean` rule that deletes all intermediate and generated files, taking your workflow back to a blank slate."
- "A default rule is the rule that Snakemake runs if you don't specify a rule on the command line. It is simply the first rule in a Snakefile."
- "Many Snakefiles define a default target called `all` as first target in the file. This runs by default and typically executes the entire workflow."
---

## Generating Plots

> ## Creating PNGs
>
> Your challenge is to update your Snakefile so that it can create `.png`
> files from `.dat` files using `plotcount.py`.
>
> * The new rule should be called `make_plot`.
> * All `.png` files should be created in a directory called `plots`.
>
> As well as a new rule you may also need to update existing rules.
>
> Remember that when testing a pattern rule, you can't just ask Snakemake to
> execute the rule by name. You need to ask Snakemake to build a specific file.
> So instead of `snakemake count_words` you need something like `snakemake dats/last.dat`.
>
> > ## Solution
> >
> > Modify the `clean` rule and add a new pattern rule `make_plot`:
> > ~~~
> > # delete everything so we can re-run things
> > rule clean:
> >     shell: 'rm -rf dats/ plots/ *.dat results.txt'
> >
> > # plot one word count dat file
> > rule make_plot:
> >     input:
> >         cmd='plotcount.py',
> >         dat='dats/{file}.dat'
> >     output: 'plots/{file}.png'
> >     shell: 'python {input.cmd} {input.dat} {output}'
> > ~~~
> > {:.language-python}
> {: .solution}
{: .challenge}

## Cleaning House

It is common practice to have a `clean` rule that deletes all intermediate
and generated files, taking your workflow back to a blank slate.

We already have a `clean` rule, so now is a good time to check that it
removes all intermediate and output files.

## Default Rules

The default rule is the rule that Snakemake runs if you don't specify a rule
on the command-line (e.g.: if you just run `snakemake`).

The default rule is simply the first rule in a Snakefile. While the default
rule can be anything you like, it is common practice to call the default rule
`all`, and have it run the entire workflow.

> ## Add an `all` rule
>
> Add an `all` rule to your Snakefile.
>
> Note that `all` rules often don't need to do any processing of their own.
> It is suffient to make them depend on all the final outputs from other rules.
> In this case, the outputs are `results.txt` and all the PNG files.
>
> > ## Hint
> >
> > It is easiest to use `glob_wildcards` and `expand` to build the list of
> > all expected `.png` files.
> {:.solution}
> > ## Solution
> >
> > First, we modify the existing code that builds `DATS` to first extract the
> > list of book names, and then to build `DATS` and a new global variable
> > listing all plots:
> > ~~~
> > # Build the list of book names. We need to use it multiple times when building
> > # the lists of files that will be built in the workflow
> > BOOK_NAMES = glob_wildcards('./books/{book}.txt').book
> >
> > # The list of all dat files
> > DATS = expand('dats/{file}.dat', file=BOOK_NAMES)
> >
> > # The list of all plot files
> > PLOTS = expand('plots/{file}.png', file=BOOK_NAMES)
> > ~~~
> > {:.language-python}
> >
> > Now we can define the `all` rule:
> > ~~~
> > # pseudo-rule that tries to build everything.
> > # Just add all the final outputs that you want built.
> > rule all:
> >     input: 'results.txt', PLOTS
> > ~~~
> > {:.language-python}
> {:.solution}
{:.challenge}

## Creating an Archive

Let's add a processing rule that depends on all previous stages of the workflow.
In this case, we will create an archive tar file.

> ## Windows Note
>
> If you are using a Windows system, make sure you have followed the
> [setup instructions][lesson-setup] regarding the use of Git Bash.
> This should provide the required environment for the `tar` command to work.
{:.callout}

> ## Creating an Archive
>
> Update your pipeline to:
>
> * Create an archive file called `zipf_analysis.tar.gz`
> * The archive should contain all `.dat` files, plots, and the
> Zipf summary table (`results.txt`).
> * Update `all` to expect `zipf_analysis.tar.gz` as input.
> * Remove the archive when `snakemake clean` is called.
>
> The syntax to create an archive is:
> ~~~
> tar -czvf zipf_analysis.tar.gz file1 directory2 file3 etc
> ~~~
> {: .language-bash}
>
> > ## Solution
> >
> > First the `create_archive` rule:
> > ~~~
> > # create an archive with all results
> > rule create_archive:
> >     input: 'results.txt', DATS, PLOTS
> >     output: 'zipf_analysis.tar.gz'
> >     shell: 'tar -czvf {output} {input}'
> > ~~~
> > {:.language-python}
> >
> > Then the update to the `clean target`:
> > ~~~
> > # delete everything so we can re-run things
> > rule clean:
> >     shell: 'rm -rf dats/ plots/ *.dat results.txt zipf_analysis.tar.gz'
> > ~~~
> > {:.language-python}
> >
> > Then the change to `all`. The workflow would still be correct without this
> > step, but since `create_archive` requires building everything, it is simpler
> > to just get `all` to depend on `create_archive`. This means we have just one
> > rule to maintain if we add new outputs later on.
> > ~~~
> > # pseudo-rule that tries to build everything.
> > # Just add all the final outputs that you want built.
> > rule all:
> >     input: 'zipf_analysis.tar.gz'
> > ~~~
> > {:.language-python}
> {:.solution}
{: .challenge}

After these exercises our final workflow should look something like the following:
![Final directed acyclic graph][fig-final-dag]

> ## Adding more books
>
> We can now do a better job at testing Zipf's rule by adding more books.
> The books we have used come from the [Project Gutenberg](http://www.gutenberg.org/) website.
> Project Gutenberg offers thousands of free ebooks to download.
>
>  **Exercise instructions:**
>
> * go to [Project Gutenberg](http://www.gutenberg.org/) and use the search box to find another book,
> for example ['The Picture of Dorian Gray'](https://www.gutenberg.org/ebooks/174) from Oscar Wilde.
> * download the 'Plain Text UTF-8' version and save it to the `books` folder;
> choose a short name for the file
> * optionally, open the file in a text editor and remove extraneous text at the beginning and end
> (look for the phrase `End of Project Gutenberg's [title], by [author]`)
> * run `snakemake` and check that the correct commands are run
> * check the results.txt file to see how this book compares to the others
{: .challenge}

[fig-final-dag]: {{ relative_root_path }}/fig/06-final-dag.svg

{% include links.md %}
