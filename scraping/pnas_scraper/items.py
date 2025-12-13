import scrapy

class MedecinItem(scrapy.Item):
    nom_complet = scrapy.Field()
    specialite = scrapy.Field()
    wilaya = scrapy.Field()
    adresse = scrapy.Field()
    telephone = scrapy.Field()
    site_web = scrapy.Field()
    photo_url = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    # Defaults handled in pipeline/spider
