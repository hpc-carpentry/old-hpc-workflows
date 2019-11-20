# Lesson Outline

## Section 1: Introduction

1. Introduction to the example workflow
    1. layout of example package
    2. book files
    3. running the wordcount script manually
    4. running plotcount
    5. testing for zipf's law
    6. bash version of a workflow and discussion of limitations (FIXME: remove hands-on sections and just discuss to save time?)

## Section 2: Introduction

2. Introduction to Snakemake
3. Snakefiles
    1. count words
    2. running snakemake
    3. clean rule
    4. default rule is first
4. Wildcards
   1. Keep it DRY
   2. highlight duplication in current Snakefile
   3. introduce wildcards
   4. cleaning up dependencies
5. Pattern rules
   1. identify remaining duplication in word count rules: they have a common pattern
   2. wildcards
   3. replace all count words rules with a single pattern rule
6. Snakefiles are Python code
   1. importing and calling python functions
   2. simplify dynamic handling of input files
7. Adding remaining stages to pipeline
   1. Creating png plots
   2. Creating an archive. FIXME: will this work on Windows?
   3. Adding more books
8. Resources and parallelism

## Section 3: Nextflow

1. Introduction to Nextflow
    1. concepts: channels and processes
2. Starting on the workflow
    1. A simple main.nf to count words in a file
    2. running nextflow
    3. building a channel from a directory to get list of all books
3. Adding Zipf analysis
   1. channels as communication between processes
4. Adding plots
   1. need a new channel, as the dats channel used in previous episode cannot be reused by another process
5. Adding the archive
   1. Highlight challenge in nextflow of specifying a process that always runs last after everything else is complete.
   2. The onComplete event