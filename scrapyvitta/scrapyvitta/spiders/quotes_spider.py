import scrapy
from sqlalchemy.orm import sessionmaker
from ..models import ScrapedItem, engine


Session = sessionmaker(bind=engine)


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['https://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.css('div.quote'):
            author = quote.css('small.author::text').get()
            tags = quote.css('div.tags a.tag::text').getall()
            about = quote.css('span.text::text').get()

            session = Session()
            item = ScrapedItem(
                author=author,
                tags=', '.join(tags),
                about=about
            )
            session.add(item)
            session.commit()
            session.close()

            yield{
                'author': author,
                'tags': tags,
                'about': about
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)