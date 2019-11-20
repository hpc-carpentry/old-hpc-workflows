---
layout: page
title: "Instructor Notes"
---

This lesson does not cover the specifics of using a Python IDE.
As the instructor, you should be familar with the editor you intend to teach,
as well as how to install/set it up across all three platforms (Windows, MacOS, Linux).
If you don't have a preference for one editor over another,
we recommend using either Jupyter Notebooks, Spyder, or a text editor/IPython console
(because these come preinstalled with Anaconda).

You have the option of running the Snakemake portion of the workshop either on student laptops or an HPC cluster.
If you end up going the laptop route,
be aware of how to run things via the Windows command line
(since Snakemake natively works on Windows).
The only significant change is the `snakemake clean` rule:
`rm -f *.dat` should be changed to `del *.dat`.

If students get lost, there is a hidden `.Snakemake` file in the lesson materials
(`snakemake-lesson.tar.gz`)
that students can use as a reference or use for the final "cluster submission" section.

For the C3DIS2020 workshop, the cluster submission episode will be skipped
due to the workshop only being delivered on student laptops. The material is
included for self-study after the workshop concludes.

{% include links.md %}
