#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import common
import StringIO
import zipfile
from lxml.html import parse, submit_form
import lxml
from ebooklib import epub
from HTMLParser import HTMLParser


# create a subclass and override the handler methods
class DownloadPageParser(HTMLParser):
    def __init__(self):
        self.download_url = ""
        self.temp_download_url = ""
        self.title = ""
        self.data_is_title = False
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            print "Encountered an a "
            href = common.find_attr_by_name(attrs, "href")
            if href.find("bookdown.php") >= 0:
                # print "found:", href
                self.temp_download_url = 'http://open-lit.com/' + href
                print "self.temp_download_url:", self.temp_download_url
        elif tag == "font":
            color = common.find_attr_by_name(attrs, "color")
            if color == "#003399":
                self.data_is_title = True

    def handle_endtag(self, tag):
        pass
        # print "Encountered an end tag :", tag

    def handle_data(self, data):
        pass
        if self.data_is_title:
            self.title = data.strip(u" -- 下載")
            self.data_is_title = False
        if data.endswith(" - html "):
            self.download_url = self.temp_download_url
def fetch_download_page(gbid):
    url = 'http://open-lit.com/bookdown.php?gbid=' + str(gbid)
    req = urllib2.Request(url)
    # req.add_header('Referer', 'http://www.python.org/')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0')
    r = urllib2.urlopen(req)
    content = r.read().decode("big5")
    return content

def parse_download_page(contnet):
    parser = DownloadPageParser()
    parser.feed(contnet)
    return parser.download_url, parser.title

def fetch_htmlzip(url):
    u"""
    返回 一个 装着 zip 数据的 file like object。
    :param url:
    :return:
    """
    req = urllib2.Request(url)
    # req.add_header('Referer', 'http://www.python.org/')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0')
    r = urllib2.urlopen(req)
    content = r.read()
    f = StringIO.StringIO()
    f.write(content)

    with zipfile.ZipFile(f, 'r') as myzip:
        namelist = myzip.namelist()
        print namelist
    return f

def parse_zip(f, title):
    from ebooklib import epub
    book = epub.EpubBook()
    # book.set_identifier('id123456')
    book.set_title(title)
    book.set_language('zh')
    book.toc = []
    # basic spine
    book.spine = ['nav']

    with zipfile.ZipFile(f, 'r') as myzip:
        namelist = myzip.namelist()
        # print namelist
        index = myzip.open("index.htm", "r")
        content = index.read().decode("big5")
        page = lxml.html.fromstring(content)# .getroot()
        # print page
        # table = page.xpath("/html/body/table[2]")
        # table = page.xpath("/html/body/table[2]/tr[1]/td/table")
        # trs = page.xpath("/html/body/table[2]/tr[1]/td/table/tr")
        trs = page.xpath("/html/body/table[2]/tr[1]/td/table/tr/td[1]/table/tr")
        for tr in trs: # 这里每一个tr都应该是目录里的一条。
            a_list = tr.xpath("td/a")
            href = ""
            chapter_title = ""
            for a in a_list:
                # print a
                # help(a)
                href = a.attrib["href"]
                text = a.text_content()
                if text:
                    chapter_title += text + " "
            print chapter_title.encode("utf-8")

            chapter_file_name = href.strip(".htm")+".xhtml"
            # create chapter
            c1 = epub.EpubHtml(title=chapter_title, file_name=chapter_file_name)
            print "href=", href
            print "chapter_file_name=", chapter_file_name

            try:
                chapter_content = myzip.open(href, "r").read().decode("big5", 'ignore')

                chapter_htm = lxml.html.fromstring(chapter_content)
                ele = chapter_htm.xpath("/html/body/table[3]/tr[1]/td/font/p")

                br_list = chapter_htm.xpath("/html/body/table[3]/tr[1]/td/font/p/br")

                c1.content = "<h1>" + chapter_title + "</h1>"

                text = chapter_htm.xpath("/html/body/table[3]/tr[1]/td/font/p")[0].text
                if text:
                    c1.content += "<p>" + text + "</p>"

                for br in br_list:
                    text = br.tail
                    if text:
                        c1.content += "<p>" + br.tail + "</p>"
                pass

                # add chapter
                book.add_item(c1)

                # define Table Of Contents
                book.toc.append(epub.Link(chapter_file_name, chapter_title, chapter_title))
                book.spine.append(c1)
                # c1.content = href
            except Exception, ex:
                pass

            #
            # book.toc = (epub.Link('chap_01.xhtml', 'Introduction', 'intro'),
            #             (epub.Section('Simple book'),
            #              (c1,))
            #             )

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    epub.write_epub("D:/ebooks/epubs/" + title + '.epub', book, {})