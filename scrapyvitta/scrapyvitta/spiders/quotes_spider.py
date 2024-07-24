import scrapy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from ..models import ScrapedItem, engine
import re
from tenacity import retry, stop_after_attempt, wait_fixed

Session = sessionmaker(bind=engine)


def clean_text(text):
    # Elimina espacios en blanco al principio y al final
    text = text.strip()
    # Elimina saltos de línea y tabulaicones
    text = re.sub(r'\s+', ' ', text)
    # Eliminar comillas dobles al principio y al final si existen
    text = text.strip('"')
    return text


def clean_tags(tags):
    # Eliminar espacios en blanco y convierte en minusculas
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
    start_urls = ['https://quotes.toscrape.com/']

    def parse(self, response):
        self.logger.info(f"Scraping page: {response.url}")
        session = Session()
        try:
            for quote in response.css('div.quote'):
                author = quote.css('small.author::text').get()
                tags = quote.css('div.tags a.tag::text').getall()
                about = quote.css('span.text::text').get()

                self.logger.info(f"Extracted quote: Author: {author}, Tags: {tags}")

                item = ScrapedItem(
                    author=author,
                    tags=', '.join(tags),
                    about=about
                )
                session.add(item)

                yield {
                    'author': author,
                    'tags': tags,
                    'about': about
                }
            self.commit_session(session)
            self.logger.info(f"Successfully committed {session.new} new items to the database")

        except OperationalError as e:
            session.rollback()
            self.logger.error(f"Database error: {e}")
        except Exception as e:
            session.rollback()
            self.logger.error(f"Other error: {e}")
        finally:
            session.close()

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            self.logger.info(f"Moving to next page: {next_page}")
            yield response.follow(next_page, self.parse)
        else:
            self.logger.info("Finished scraping all pages")

    def commit_session(self, session):
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error committing to database: {e}")
            raise
