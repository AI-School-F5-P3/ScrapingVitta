import scrapy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from ..models import ScrapedItem, engine
import re
from tenacity import retry, stop_after_attempt, wait_fixed

Session = sessionmaker(bind=engine)

def clean_text(text):
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    text = text.strip('"')
    return text

def clean_tags(tags):
    return [tag.strip().lower() for tag in tags if tag.strip()]

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def commit_session(session):
    try:
        session.commit()
    except OperationalError as e:
        session.rollback()
        raise e

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['https://quotes.toscrape.com/page/1/']

    def parse(self, response):
        self.logger.info(f"Scraping page: {response.url}")
        
        for quote in response.css('div.quote'):
            author = quote.css('small.author::text').get()
            tags = quote.css('div.tags a.tag::text').getall()
            text = clean_text(quote.css('span.text::text').get())
            about_link = quote.css('span a::attr(href)').get()

            self.logger.info(f"Extracted quote: Author: {author}, Text: {text[:30]}...")

            yield scrapy.Request(
                response.urljoin(about_link),
                callback=self.parse_author,
                meta={'author': author, 'tags': tags, 'text': text},
                dont_filter=True
            )

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            self.logger.info(f"Moving to next page: {next_page}")
            yield response.follow(next_page, self.parse)
        else:
            self.logger.info("Finished scraping all pages")

    def parse_author(self, response):
        author = response.meta['author']
        tags = response.meta['tags']
        text = response.meta['text']
        about = clean_text(response.css('div.author-description::text').get())

        session = Session()
        try:
            item = ScrapedItem(
                author=author,
                tags=', '.join(clean_tags(tags)),
                about=about,
                text=text
            )
            session.add(item)
            commit_session(session)
            self.logger.info(f"Successfully added item for author: {author}")

        except OperationalError as e:
            session.rollback()
            self.logger.error(f"Database error: {e}")
        except Exception as e:
            session.rollback()
            self.logger.error(f"Other error: {e}")
        finally:
            session.close()

        yield {
            'author': author,
            'tags': tags,
            'about': about,
            'text': text
        }
