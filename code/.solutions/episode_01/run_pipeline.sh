# USAGE: bash run_pipeline.sh
# to produce plots for isles and abyss
# and the summary table for the Zipf's law tests

# python wordcount.py books/isles.txt isles.dat
# python wordcount.py books/abyss.txt abyss.dat

python plotcount.py isles.dat isles.png
python plotcount.py abyss.dat abyss.png

# Generate summary table
python zipf_test.py abyss.dat isles.dat > results.txt
