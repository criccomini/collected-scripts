#!/bin/bash
CWD=$(cd "$(dirname "$0")"; pwd)
STRONG_FILE=~/Downloads/strong.csv
DATA_DIR=$CWD/data
RENDERED_DIR=$CWD/rendered

function log {
    echo "[$(date +'%F %T')]: $*"
}

export -f log

log "CWD = $CWD"
log "STRONG_FILE = $STRONG_FILE"
log "DATA_DIR = $DATA_DIR"
log "RENDERED_DIR = $RENDERED_DIR"

log "Fetching $STRONG_FILE"
[ -f STRONG_FILE ] && mv STRONG_FILE $CWD/data/strong.csv

log "Rendering $STRONG_FILE"
$CWD/scripts/lifting/strong.py \
  $CWD/templates/lifting_log.3543.md \
  $CWD/rendered/lifting_log.3543.md \
  $CWD/data/lifting/strong.csv \
  $CWD/data/lifting/531.csv \
  $CWD/data/lifting/stacked.csv

log "Rendering Good Reads"
$CWD/scripts/render_goodreads.py \
  $CWD/templates/books.5877.md \
  $CWD/rendered/books.5877.md \
  39364006

log "Posting rendered files: $RENDERED_DIR"
python $CWD/upload_posts.py $RENDERED_DIR | xargs bash -c 'log Posting: "$@"'