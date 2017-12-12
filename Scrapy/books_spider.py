# -*- coding: utf-8 -*-
import scrapy

Ratings = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

class ScrapeSpider(scrapy.Spider):
    name = "bookstoscrape"
    start_urls = [
        'http://books.toscrape.com/',
    ]

    def parse(self, response):
        for book_url in response.css("article.product_pod > h3 > a ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(book_url), callback=self.parse_book_page)
        next_page = response.css("li.next > a ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_book_page(self, response):
        book = {}
        product = response.css("div.product_main")
        book["Title"] = product.css("h1 ::text").extract_first()
        book["Price(£)"] = product.css("p.price_color ::text").re_first(r'\d+')
        book['Category'] = response.xpath(
            "//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()"
        ).extract_first()

        # Stock with a Regex to get the number only
        book["Availability"] = response.xpath(
            "//table/tr[6]/td/text()"
        ).re_first(r'\d+')

        # Ratings
        book["Ratings(1-5)"] = Ratings.get(response.xpath(
            "//h1/following-sibling::p[3]/@class"
        ).re_first(r'One$|Two$|Three$|Four$|Five$'))

        # Universal Product Code
        book["UPC"] = response.xpath(
            "//table/tr[1]/td/text()"
        ).extract_first()
        yield book
