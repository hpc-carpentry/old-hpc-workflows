#!/usr/bin/env nextflow

// Configuration parameters
params.inputPath = "../books/"
params.resultsPath = "results"
params.archiveFile = "zipf_analysis.tgz"
params.echo = false


// In nextflow, the safest way to do something after you know that all other
// steps have completed is to handle the workflow.onComplete event.
// Note that this is a groovy function, so you can"t use the nextflow
// additions to the groovy language.
workflow.onComplete {
    // Run a tar command to build the archive file
    "tar -C $params.resultsPath -chzvf $params.resultsPath/$params.archiveFile dats/ plots/ results/".execute()
}

// count the words in a book
process countWords {
    echo params.echo
    publishDir params.resultsPath + "/dats"

    input:
        file book from Channel.fromPath(params.inputPath + "*.txt")

    output:
        file "${book.baseName}.dat" into plot_dats, zipf_dats

    """
        echo "Processing ${book} --> ${book.baseName}.dat"
        wordcount.py $book ${book.baseName}.dat
    """
}

// produce a plot
process makePlots {
    echo params.echo
    publishDir params.resultsPath + "/plots"

    input:
        file dat from plot_dats

    output:
        file "${dat.baseName}.png"

    """
        echo "Plotting ${dat} --> ${dat.baseName}.png"
        plotcount.py $dat ${dat.baseName}.png
    """
}

// do the Zipf test on all book results
process zipfTest {
    echo params.echo
    publishDir params.resultsPath + "/results"

    input:
        file datsList from zipf_dats.collect()

    output:
        file "results.txt"

    """
        echo "Calculating Zipf's law results for each book"
        zipf_test.py $datsList > results.txt
    """
}

