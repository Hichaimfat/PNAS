import scrapy
from pnas_scraper.items import MedecinItem

class MedecinsSpider(scrapy.Spider):
    name = "medecins"
    allowed_domains = ["annuaire-sante-algerie.dz"]
    start_urls = ["https://annuaire-sante-algerie.dz/list/"]

    def parse(self, response):
        # NOTE: Selectors are hypothetical based on common patterns.
        # User requested a "minimal performant spider".
        # Real selectors depend on actual HTML structure which I cannot see.
        # Implemented generic extraction logic.
        
        for medecin_card in response.css("div.listing-item"): # Hypothetical selector
            item = MedecinItem()
            item["nom_complet"] = medecin_card.css("h3.title::text").get(default="").strip()
            item["specialite"] = medecin_card.css("div.specialty::text").get(default="Generaliste").strip()
            item["wilaya"] = medecin_card.css("div.location::text").get(default="Alger").strip()
            item["adresse"] = medecin_card.css("div.address::text").get(default="").strip()
            item["telephone"] = medecin_card.css("div.phone::text").get(default="").strip()
            item["site_web"] = medecin_card.css("a.website::attr(href)").get()
            
            # Simple yield
            yield item

        # Pagination
        next_page = response.css("a.next-page::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
