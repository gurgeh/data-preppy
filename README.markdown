# Data-preppy...

...is a collection of scripts to work with CSV files and do data preparation, for example for scikit-learn prediction methods. The full files are never held in memory so you can work with very large files if you want to.

I need to write better documentation for this, but for now you sometimes need to read the source.

For now it is _Python 2.7_ only. I gratefully accept pull requests to fix this and other issues.

Depends on numpy, scikit-learn, a little bit on pandas and optionally sknn (a neural network for scikit-learn).

## Quick usage

    ./summarize_csv.py table.csv  # This will calculate and write stats (including unicode sparklines) to stdout. Paste the stats to stat.txt or something
    # Then add "+" in front of the fields that you want to keep
    ./filter.py stat.txt table.csv filtered_table.csv # filter columns
    ./csv_fix.py stat.txt filtered_table.csv fixed_table.csv  # impute standard values in empty cells, split category fields to several boolean fields

## Other files
+add_columns.py - Take two or more CSV files with equal amount of rows and add the columns
+add_rows.py - Add rows of two CSV files with same headers.
+cluster_csv.py - Cluster rows in CSV and add a cluster group column to the rows. Can be useful to get a "holistic" view of each row.
+convert_coords.py - Convert sweref coords to GPS. Not really similar to the other tools.
+dict_merge.py - Run through a CSV and replace cells via translation dict.
+filter_column_names.py - Remove fields from CSV by name
+kill_outliers.py - Run after summarize_csv if you want to remove (presumably broken) rows with different field types than the rest.
+merge_csv.py - Merge two CSV file according to an ID column. Like a join.
+metrics.py - Calculate and graph performance metrics for classification
+predict.py - Some prediction methods
+smart_csv.py - The class used to read CSVs in the other files. Guesses encoding, delimiter, etc.
+split_csv.py - Split CSV into training and test


