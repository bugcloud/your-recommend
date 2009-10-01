#!Python2.6
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import amazon_ecs
import urllib2
import xml.parsers.expat
try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree

class SearchedItem:
    ''' Amazon ItemSearch Operation の結果格納  '''
    def __init__(self):

        self.asin = ''
        self.detailPageURL = ''
        self.imageURL = ''
        self.title = ''
        self.author = ''
        self.manufacturer = ''

class SAXTagHandler:
    def __init__(self):
        # XMLParser(SAX)の状態制御
        self.proc_start = False
        self.img_start = False
        self.now_key = ''
        self.item_list = []
    def startElementHandler(self, name, attributes):
        ''' xml.parsers.expat XMLParser のハンドラ
                    要素の開始を処理するごとに呼び出される
            @see http://www.python.jp/doc/release/lib/xmlparser-objects.html
        '''
        if name == 'Item':
            self.proc_start = True
        if name == 'SmallImage':
            self.img_start = True
        if self.proc_start:
            if name == 'Item':
                self.item_list.append(SearchedItem())
            else:
                self.now_key = name

    def startElementHandler2(self, name, attributes):
        ''' xml.parsers.expat XMLParser のハンドラ
                    要素の開始を処理するごとに呼び出される
            @see http://www.python.jp/doc/release/lib/xmlparser-objects.html
        '''
        if name == 'Item':
            self.proc_start = True
        if name == 'SmallImage':
            self.img_start = True
        if self.proc_start:
            if name == 'Item':
                self.item_list.append(SearchedItem())
            else:
                self.now_key = name
                
    def endElementHandler(self, name):
        ''' xml.parsers.expat XMLParser のハンドラ
                    要素の終端を処理するごとに呼び出される
            @see http://www.python.jp/doc/release/lib/xmlparser-objects.html
        '''
        if name == 'ItemAttributes':
            self.proc_start = False
        if name == 'SmallImage':
            self.img_start = False

    def endElementHandler2(self, name):
        ''' xml.parsers.expat XMLParser のハンドラ
                    要素の終端を処理するごとに呼び出される
            @see http://www.python.jp/doc/release/lib/xmlparser-objects.html
        '''
        if name == 'ItemAttributes':
            self.proc_start = False
        if name == 'SmallImage':
            self.img_start = False
            
    def characterDataHandler(self, data):
        ''' xml.parsers.expat XMLParser のハンドラ
                    文字データを処理するときに呼びだされる
            @see http://www.python.jp/doc/release/lib/xmlparser-objects.html
        '''
        if self.proc_start:
            idx = len(self.item_list)
            idx = idx -1
            if idx >= 0:
                if self.now_key == 'ASIN':
                    self.item_list[idx].asin = data
                if self.now_key == 'DetailPageURL':
                    self.item_list[idx].detailPageURL = data
                if self.img_start and self.now_key == 'URL':
                    self.item_list[idx].imageURL = data
                if self.now_key == 'Title':
                    self.item_list[idx].title = data
                if self.now_key == 'Author':
                    self.item_list[idx].author = data
                if self.now_key == 'Manufacturer':
                    self.item_list[idx].manufacturer = data

class MainPage(webapp.RequestHandler):
    def get(self):
        self.redirect('/am_is?keyword=amazon')

class AmazonItemSearch(webapp.RequestHandler):
    ''' Amazon Product Advertising API(ItemSearch) を利用し、キーワード検索を行う
        example http://bugcloud.appspot.com/am_is?keyword=book
    '''
    def get(self):
        keyword = self.request.get('keyword').encode('utf-8')
        if keyword == '':
            keyword = 'amazon'
        operation = amazon_ecs.ItemSearch()
        operation.keywords(keyword)
        operation.search_index('Books')
        operation.response_group('Medium')
        request = operation.request()

        # XMLParserの生成とハンドラのセット
        h = SAXTagHandler()
        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = h.startElementHandler
        p.EndElementHandler = h.endElementHandler
        p.CharacterDataHandler = h.characterDataHandler

        # リクエストの実行と解析
        f = urllib2.urlopen(request)
        p.Parse(f.read())
        self.response.out.write('<div class="result"><ul>')
        for itm in h.item_list:
            self.response.out.write('<li><div class="item">\
                                       <a target="_blank" onMouseover="disp_mess(0)" onMouseout="del_mess(0)" onClick="registRequest(%s)">\
                                         <img src="%s" border="0"/>\
                                       </a>\
                                     </div>\
                                     <div class="attr">\
                                       <table><tr><td>Title :</td><td>%s</td></tr> \
                                       <tr><td>Author :</td><td>%s</td></tr></table>\
                                     </div></li>'
                                    % (itm.asin, itm.imageURL, itm.title, itm.author))
        self.response.out.write('</ul></div>')

    
class AmazonItemLookup(webapp.RequestHandler):
    ''' Amazon Product Advertising API(ItemLookup) を利用し、ASIN検索を行う
        example http://bugcloud.appspot.com/asin_is?asin=1234567890
    '''
    def get(self):
        asin = self.request.get('asin').encode('utf-8')

        operation = amazon_ecs.ItemLookup()
        operation.itemid(asin)
        operation.response_group('Medium')
        request = operation.request()

        # XMLParserの生成とハンドラのセット
        h = SAXTagHandler()
        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = h.startElementHandler2
        p.EndElementHandler = h.endElementHandler2
        p.CharacterDataHandler = h.characterDataHandler

        # リクエストの実行と解析
        f = urllib2.urlopen(request)
        p.Parse(f.read())
        self.response.out.write('<div class="myresult">')
        for itm in h.item_list:
            self.response.out.write('<div class="myrecommend"><a href="%s" target="_blank"><img src="%s" border="0"/></a></div>\
                                       <div class="myattr">\
                                         <table><tr><td class="icon"><img src="http://bugcloud.appspot.com/static/images/title.png" border="0" /></td><td>%s</td></tr> \
                                         <tr><td class="icon"><img src="http://bugcloud.appspot.com/static/images/author.png" border="0" /></td><td>%s</td></tr>\
                                         <tr><td class="icon"><img src="http://bugcloud.appspot.com/static/images/manufacturer.png" border="0" /></td><td>%s</td></tr></table>\
                                       </div>'
                                    % (itm.detailPageURL, itm.imageURL, itm.title, itm.author, itm.manufacturer))
        self.response.out.write('</div>')
        
                
application = webapp.WSGIApplication([
                                      ('/', MainPage),
                                      ('/am_is', AmazonItemSearch),
                                      ('/asin_is', AmazonItemLookup),
                                      ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()