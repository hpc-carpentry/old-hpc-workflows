---
title: "Introduction to Snakemake"
teaching: 15
exercises: 15
questions:
- "How can I make my results easier to reproduce?"
objectives:
- "Understand our example problem."
keypoints:
- "Bash scripts are not an efficient way of storing a workflow."
- "Snakemake is one method of managing a complex computational workflow."
---

## What is Snakemake and why are we using it?

There are many different tools that researchers use to automate this type of work.
Snakemake is a very popular tool, and the one we have selected for this tutorial.
There are several reasons this tool was chosen:

* It’s free, open-source, and installs in about 5 seconds flat via `pip`.

* Snakemake works cross-platform (Windows, MacOS, Linux) and is compatible with all HPC schedulers. More importantly, the same workflow will work and scale appropriately regardless of whether it’s on a laptop or cluster without modification.

* Snakemake uses pure Python syntax. There is no tool specific-language to learn like in GNU Make, NextFlow, WDL, etc.. Even if students end up not liking Snakemake, you’ve still taught them how to program in Python at the end of the day.

* Anything that you can do in Python, you can do with Snakemake (since you can pretty much execute arbitrary Python code anywhere).

* Snakemake was written to be as similar to GNU Make as possible. Users already familiar with Make will find Snakemake quite easy to use.

* It’s easy. You can (hopefully!) learn Snakemake in an afternoon!

The rest of these lessons aim to teach you how to use Snakemake by example.
Our goal is to automate our example workflow, and have it do everything for us in parallel
regardless of where and how it is run (and have it be reproducible!).

{% include links.md %}
