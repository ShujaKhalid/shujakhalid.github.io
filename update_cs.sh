#!/bin/sh

# Push the site to the University of Toronto CS web space.
# index.html is self-contained (inline CSS), but the project thumbnails
# live in images/, so copy both.
scp -p index.html skhalid@cs.toronto.edu:/u/skhalid/public_html/
scp -pr images skhalid@cs.toronto.edu:/u/skhalid/public_html/
scp -pr data skhalid@cs.toronto.edu:/u/skhalid/public_html/
