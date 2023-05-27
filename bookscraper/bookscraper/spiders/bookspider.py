import scrapy
from bookscraper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        print(f"*--------------*\n UserAgent ya ga go ke : {response.request.headers} \n*--------------*")
        books = response.css("article.product_pod")

        for book in books:
            book_page_path = book.css("h3 a").attrib['href']
            if "catalogue/" in book_page_path:
                book_page_url = f'{self.start_urls[0]}/{book_page_path}'
            else:
                book_page_url = f'{self.start_urls[0]}/catalogue/{book_page_path}'

            yield response.follow(book_page_url, callback=self.parse_book_page)

        next_page_path = response.css("li.next a::attr(href)").get()

        if "catalogue/" in next_page_path:
            next_page_url = f'{self.start_urls[0]}/{next_page_path}'
        else:
            next_page_url = f'{self.start_urls[0]}/catalogue/{next_page_path}'

        yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response):
        table_rows = response.css("table tr")
        book_item = BookItem()
       
        book_item["url"] = response.url
        book_item["title"] = response.css("*.product_main h1::text").get()
        book_item["product_type"] = table_rows[1].css("td::text").get()
        book_item["price_excl_tax"] = table_rows[2].css("td::text").get()            
        book_item["price_inc_tax"] = table_rows[3].css("td::text").get()
        book_item["tax"] = table_rows[4].css("td::text").get()
        book_item["availability"] = table_rows[5].css("td::text").get()
        book_item["num_reviews"] = table_rows[6].css("td::text").get()
        book_item["stars"] = response.css("p.star-rating").attrib["class"]
        book_item["category"] = response.xpath('//*[@id="default"]/div/div/ul/li[3]/a/text()').get()
        book_item["description"] = response.xpath('//*[@id="content_inner"]/article/p/text()').get()
        book_item["price"] = response.css("p.price_color::text").get()
        
        yield book_item

