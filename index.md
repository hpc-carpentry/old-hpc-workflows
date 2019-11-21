---
layout: lesson
root: .  # Is the only page that doesn't follow the pattern /:path/index.html
permalink: index.html  # Is the only page that doesn't follow the pattern /:path/index.html
---

This lesson teaches the basics of modern workflow engines
through [Snakemake](https://snakemake.readthedocs.io/en/stable/).

zipfs-lawThe example workflow performs a frequency analysis of several public
domain books sourced from [Project Gutenberg](https://www.gutenberg.org/),
testing how closely each book conforms to [Zipf's Law][zipf].
All code and data are provided. This example has been chosen over a more
complex scientific workflow as the goal is to appeal to a wide audience and
to focus on building the workflow without distraction from the underlying
processing.

At the end of this lesson, you will:

* Understand the benefits of workflow engines.
* Be able to create reproducible analysis pipelines with Snakemake.

## Pre-requisites

* Some basic Python programming experience, ideally in Python 3.
* Familiarity with running programs on a command line.

If you require a refresher or introductory course, then I suggest one or more of these Carpentry courses:

* [CSIRO Data School Introduction to Python](https://csiro-data-school.github.io/python/)
* [Programming with Python](http://swcarpentry.github.io/python-novice-inflammation/)
* [The Unix Shell](https://swcarpentry.github.io/shell-novice/)

> ## Setup
>
> Please follow the instructions in the [Setup page][lesson-setup].
>
> The files used in this lesson can be downloaded:
>
> * [for Linux/Mac][linux_code_pack]
> * [for Windows][win_code_pack]
{: .prereq}

{% include links.md %}

[linux_code_pack]: {{ relative_root_path }}/files/workflow-engines-lesson.tar.gz
[win_code_pack]: {{ relative_root_path }}/files/workflow-engines-lesson.zip
[zipf]: {{ relative_root_path }}/reference#zipfs-law
