set -x
CWD="$( dirname "$0" )"
$CWD/scripts/lifting/strong.py $CWD/templates/lifting_log.md $CWD/rendered/lifting_log.md $CWD/data/lifting/strong.csv $CWD/data/lifting/531.csv $CWD/data/lifting/stacked.csv
