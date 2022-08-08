---
layout: lesson
root: .  # Is the only page that doesn't follow the pattern /:path/index.html
permalink: index.html  # Is the only page that doesn't follow the pattern /:path/index.html
---

Learn to tame your unruly data processing workflow with [Snakemake][snakemake],
a tool for creating reproducible and scalable data analyses. Workflows are
described via a human readable, Python-based language. They can be seamlessly
scaled to server, cluster, grid, and cloud environments, without the need to
modify the workflow definition. In this lesson, you will build up a
reproducible, automated, and efficient workflow step by step with
Snakemake. Along the way, you will learn the benefits of modern workflow
engines and how to apply them to your own work.

The example workflow will launch several cluster jobs with the [Amdahl][amdahl]
program from the [Introduction to High-Performance Computing][hpc-intro] using
different numbers of processors, collect the output from each job, and create a
graph of "speedup" (reference runtime, usually one processor or node or GPU, divided by the runtime with increased compute resources) as
a function of the processor count. You will use this data to analyze the
performance of the program, and compare it to the predictions made by Amdahl's
Law. This example has been chosen over a more complex, real-world scientific
workflow as the goal is to focus on building the workflow without getting
distracted by the underlying science domain.

At the end of this lesson, you will:

* Understand the benefits of workflow engines.
* Be able to create reproducible analysis pipelines with Snakemake.
* Estimate the proportion of parallel work from a scaling study.

## Prerequisites

* Familiarity with the command line and shell scripting, preferably having
  taken [The Unix Shell][shell-novice] recently or as part of this workshop.
* A basic grasp of HPC scheduler interactions, preferably having taken
  [Introduction to HPC][hpc-intro] recently or as part of this workshop.
* Familiarity with the [Python][python-lang] programming language is _not_
  required, but will help if you're curious about the inner workings of the
  provided "black box" programs.

> ## Setup
>
> Please follow the instructions in the [Setup page](setup).
>
> The files used in this lesson can be downloaded:
>
> * [Linux/macOS][unix_code_pack]
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

{% include links.md %}

[amdahl]: https://github.com/ocaisa/amdahl
[hpc-intro]: https://carpentries-incubator.github.io/hpc-intro/
[python-lang]: https://www.python.org
[shell-novice]: https://swcarpentry.github.io/shell-novice/
[snakemake]: https://snakemake.readthedocs.io
[unix_code_pack]: {{ relative_root_path }}/files/workflow-engines-lesson.tar.gz
[win_code_pack]: {{ relative_root_path }}/files/workflow-engines-lesson.zip
