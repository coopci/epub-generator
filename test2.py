#!/usr/bin/env python
# -*- coding: utf-8 -*-
import openlit




print "234"
# content = openlit.fetch_download_page(335) # 五凤吟
# content = openlit.fetch_download_page(54) # 風流悟
# content = openlit.fetch_download_page(414) # 玉樓春
#content = openlit.fetch_download_page(108)  # 	歷史通俗演義 - 前漢
# content = openlit.fetch_download_page(116)  # 歷史通俗演義 - 後漢
# content = openlit.fetch_download_page(109)# 歷史通俗演義 - 兩晉
# content = openlit.fetch_download_page(55) # 玉嬌梨
content = openlit.fetch_download_page(111) # 歷史通俗演義 - 南北史

#print content
print "asdf"
download_url, title = openlit.parse_download_page(content)
# download_url = "http://open-lit.com/bookdown.php?downloadid=156&gbid=37"
print "download_url:", download_url
print "title:", title


zipf = openlit.fetch_htmlzip(download_url)


# openlit.parse_zip(zipf)
openlit.parse_zip(zipf, title) # 会保存到 D:/ebooks/epubs/
