#!/bin/bash
CWD=$(cd "$(dirname "$0")"; pwd)
STRONG_FILE=~/Downloads/strong.csv
DATA_DIR=$CWD/data
RENDERED_DIR=$CWD/rendered

OVERCAST_OPXML_FILE=$DATA_DIR/overcast.xml

function log {
    echo "[$(date +'%F %T')]: $*"
}

export -f log

log "CWD = $CWD"
log "STRONG_FILE = $STRONG_FILE"
log "DATA_DIR = $DATA_DIR"
log "RENDERED_DIR = $RENDERED_DIR"

log "Making $RENDERED_DIR"
mkdir -p $RENDERED_DIR

log "Fetching $STRONG_FILE"
[ -f STRONG_FILE ] && mv STRONG_FILE $CWD/data/strong.csv

log "Fetching $OVERCAST_OPXML_FILE"
$CWD/scripts/fetch_overcast.py $OVERCAST_OPXML_FILE

log "Rendering Strong"
$CWD/scripts/render_strong.py \
  $CWD/templates/lifting_log.3543.md \
  $CWD/rendered/lifting_log.3543.md \
  $CWD/data/strong.csv \
  $CWD/data/531.csv \
  $CWD/data/stacked.csv

log "Rendering Goodreads"
$CWD/scripts/render_goodreads.py \
  $CWD/templates/books.5877.md \
  $CWD/rendered/books.5877.md \
  $GOODREADS_USER_ID

log "Rendering Podcasts"
$CWD/scripts/render_opml_extended.py \
  $CWD/templates/podcasts.6552.md \
  $CWD/rendered/podcasts.6552.md \
  $OVERCAST_OPXML_FILE

log "Posting rendered files: $RENDERED_DIR"
python $CWD/upload_posts.py $RENDERED_DIR | xargs bash -c 'log Posting: "$@"'