#!/usr/bin/env python
# -*- coding: utf-8 -*-
import openlit


from ebooklib import epub

book = epub.EpubBook()
epub.write_epub('test.epub', book, {})



print "234"
#content = openlit.fetch_download_page(37)
#print content
print "asdf"
# download_url, title = openlit.parse_download_page(content)
download_url = "http://open-lit.com/bookdown.php?downloadid=156&gbid=37"
print "download_url:", download_url
#print "title:", title


# zipf = openlit.fetch_htmlzip(download_url)


# openlit.parse_zip(zipf)
openlit.parse_zip("YDHMLVFSUMMU-html.zip", u"新紀元")
