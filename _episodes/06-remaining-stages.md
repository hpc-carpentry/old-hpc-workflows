---
title: "Completing the Pipeline"
teaching: 0
exercises: 20
questions:
objectives:
keypoints:
---

> ## Creating PNGs
>
> Add new rules and update existing rules to:
>
> * Create `.png` files from `.dat` files using `plotcount.py`.
> * Remove all auto-generated files (`.dat`, `.png`,
>   `results.txt`).
>
> Finally, many Snakefiles define a default target called `all` as first target,
> that will build what the Snakefile has been written to build (e.g. in
> our case, the `.png` files and the `results.txt` file).
> Add an `all` target to your Snakefile (Hint: this rule
> has the `results.txt` file and the `.png` files as dependencies, but
> no actions).  With that in place, instead of running `make
> results.txt`, you should now run `snakemake all`, or just simply
> `snakemake`.
{: .challenge}

> ## Creating an Archive
>
> Update your pipeline to:
>
> * Create an archive, `zipf_analysis.tar.gz`, to hold all our
>   `.dat` files, plots, and the Zipf summary table.
> * Update `all` to expect `zipf_analysis.tar.gz` as input.
> * Remove `zipf_analysis.tar.gz` when `snakemake clean` is called.
>
> The syntax to create an archive is shown below:
> ```bash
> tar -czvf zipf_analysis.tar.gz file1 directory2 file3 etc
> ```
>
{: .challenge}

After these excercises our final workflow should look something like the following:

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

