BOT_NAME = "pnas_scraper"

SPIDER_MODULES = ["pnas_scraper.spiders"]
NEWSPIDER_MODULE = "pnas_scraper.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure item pipelines
ITEM_PIPELINES = {
   "pnas_scraper.pipelines.PostgresPipeline": 300,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Postgres Connection (Make sure to set env vars or update this)
POSTGRES_HOST = "localhost"
POSTGRES_DB = "pnas_db"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "password"
