# Scripts for Collected Notes

This repository contains a collection of scripts for [Collected Notes](http://collectednotes.com/).

The scripts pull data from different data sources, and render markdown files. These files are then posted to Collected Notes. The repository currently integrates with:

* [Strong](https://www.strong.app)  
  I use this to track weight lifting data. I export Strong's CSV data from my phone using Airdrop.
* [Goodreads](https://www.goodreads.com)  
  I use Goodreads to track my reading. My Kindle automatically posts to Goodreads when I share it. A script in this repository pulls the reading data and generates a book list.

## Setup

The scripts require a couple of variables to run. Set your Collected Notes email address, API token, and site ID as environment variables:

```
export COLLECTED_NOTES_API_TOKEN=...
export COLLECTED_NOTES_API_EMAIL=...
export COLLECTED_NOTES_SITE_ID=...
```

You can find your email and API token [here](https://collectednotes.com/accounts/me/token).

You can find your site ID by editing any post:

```
https://collectednotes.com/sites/<site ID>/notes/<post ID>/edit
```

### Build

The repository comes with a build.sh file. This is specific to my needs. You can write your own based off of it. My build. requires you to set these environment variables:

```
# Required for Goodreads
GOODREADS_KEY=...
GOODREADS_USER_ID=...
```

`GOODREADS_KEY` must be set to your Goodreads API key. Click [here](https://www.goodreads.com/api/keys) to get one. Click on your account details to find your Goodreads user ID; it's the number in the URL (https://www.goodreads.com/user/show/<your ID>-foo-bar-baz).

## Templates

The `templates` directory has markdown templates. The templates use Python's built-in [Template](https://docs.python.org/2/library/string.html#template-strings) class. It's simple, but it works. Variables are defined using [PEP 292](https://www.python.org/dev/peps/pep-0292) formatting.

Templates are rendered using the `render_posts.sh` script. This script is specific to my templates and use cases. You should customize it based on your needs.

NOTE: The template filenames must be of the format:

```
template_name.post_id.md
```

See the `templates` directory for examples. The post ID is how the `upload_posts.py` script determines which post to update. You must create the notes manually using the Collected Notes UI. Edit the post to see the post ID in the URL.

## Posting

You can upload your rendered templates using the `upload_posts.py` script. This script uses the environment variables from the setup section to upload your posts to Collected Notes.

I have written my own `build.sh`. This won't work for you out of the box, but you can use it as an example. My `build.sh` gathers some data, renders templates, and pushes markdown to Collected Notes.

## About

You might notice some strange design decisions with these scripts. I have gone out of my way not to depend on anything outside packages. No virtual environment is required. No pip installs. Just simply Python and Bash scripts.
