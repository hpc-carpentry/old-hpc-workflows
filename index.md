---
layout: lesson
root: .  # Is the only page that doesn't follow the pattern /:path/index.html
permalink: index.html  # Is the only page that doesn't follow the pattern /:path/index.html
---

Learn to tame your unruly data processing workflow with
[Snakemake](https://snakemake.readthedocs.io/en/stable/), a tool for creating
reproducible and scalable data analyses. Workflows are described via a human
readable, Python-based language. They can be seamlessly scaled to server,
cluster, grid, and cloud environments, without the need to modify the
workflow definition.

Starting with some independent analysis tasks, you will explore the
limitations of manual processing and shell scripting before building up a
reproducible, automated, and efficient workflow step by step with Snakemake.
Along the way, you will learn the benefits of modern workflow engines and how
to apply them to your own work.

The example workflow performs a frequency analysis of several public domain
books sourced from [Project Gutenberg](https://www.gutenberg.org/), testing
how closely each book conforms to [Zipf's Law][ref-zipf]. This example has
been chosen over a more complex scientific workflow as the goal is to appeal
to a wide audience and to focus on building the workflow without getting
distracted by the underlying science domain.

At the end of this lesson, you will:

* Understand the benefits of workflow engines.
* Be able to create reproducible analysis pipelines with Snakemake.

All code and data are provided.

## Pre-requisites

* Some basic Python programming experience, ideally in Python 3.
* Familiarity with running programs on a command line.

If you require a refresher or introductory course, then I suggest one or more
of these Carpentry courses:

* [CSIRO Data School Introduction to Python](https://csiro-data-school.github.io/python/)
* [Programming with Python](http://swcarpentry.github.io/python-novice-inflammation/)
* [The Unix Shell](https://swcarpentry.github.io/shell-novice/)

> ## Setup
>
> Please follow the instructions in the [Setup page][lesson-setup].
>
> The files used in this lesson can be downloaded:
>
> * [Linux/Mac][linux_code_pack]
> * [Windows][win_code_pack]
>
> Once downloaded, please extract to the directory you wish to work in for all
> the hands-on exercises.
>
> Solutions for most episodes can be found in the `.solutions`
> directory inside the code download.
>
> A `requirements.txt` file is included in the download.
> This can be used to install the required Python packages.
{: .prereq}

[linux_code_pack]: {{ relative_root_path }}/files/workflow-engines-lesson.tar.gz
[win_code_pack]: {{ relative_root_path }}/files/workflow-engines-lesson.zip
[ref-zipf]: {{ relative_root_path }}/reference#zipfs-law

{% include links.md %}
