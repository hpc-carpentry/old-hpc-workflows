---
layout: page
title: Discussion
---

## Why not other workflow/pipeline tools?

There are lots of other pipeline/workflow management tools out there
(in fact, this lesson was adapted from Software Carpentry's [GNU Make lesson](http://swcarpentry.github.io/make-novice/)).
Why teach Snakemake instead of these other tools?

* It's free, open-source, and installs in about 5 seconds flat via `pip`.

* Snakemake works cross-platform (Windows, MacOS, Linux) and is compatible with all HPC schedulers. More importantly, the same workflow will work and scale appropriately regardless of whether it's on a laptop or cluster *without modification*.

* Snakemake uses pure Python syntax. There is no tool specific-language to learn like in GNU Make, NextFlow, WDL, etc.. Even if students end up not liking Snakemake, you've still taught them how to program in Python at the end of the day.

* Anything that you can do in Python, you can do with Snakemake (since you can pretty much execute arbitrary Python code anywhere).

* Snakemake was written to be as similar to GNU Make as possible. Users already familiar with Make will find Snakemake quite easy to use.

* It's easy. You can teach Snakemake in an afternoon.

{% include links.md %}
