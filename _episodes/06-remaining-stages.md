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
- "Add a `clean` rule to your Snakefile."
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
> As well as a new rule you may also need to update existing rules.
>
> > ## Solution
> >
> > FIXME: add plot rule
> {: .solution}
{: .challenge}

## Cleaning House

It is common practice to have a `clean` rule that deletes all intermediate
and generated files, taking your workflow back to a blank slate.

> ## Cleaning Up
>
> Add a new rule called `clean` to remove all auto-generated files (`.dat`, `.png`,
> `results.txt`).
>
> > ## Solution
> >
> > FIXME: add clean rule
> {: .solution}
{: .challenge}

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
> > ## Solution
> >
> > FIXME: add all rule
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
> * Create an archive file to hold all our `.dat` files, plots, and the
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
> > FIXME: add archive rule and changes to other rules
> {:.solution}
{: .challenge}

After these exercises our final workflow should look something like the following:

![Final directed acyclic graph](../fig/05-final-dag.svg)

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

{% include links.md %}
