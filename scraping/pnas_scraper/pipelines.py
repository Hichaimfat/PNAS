import psycopg2
from itemadapter import ItemAdapter

class PostgresPipeline:
    def open_spider(self, spider):
        self.connection = psycopg2.connect(
            host=spider.settings.get("POSTGRES_HOST"),
            database=spider.settings.get("POSTGRES_DB"),
            user=spider.settings.get("POSTGRES_USER"),
            password=spider.settings.get("POSTGRES_PASSWORD"),
        )
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Ensure compulsory fields
        if not adapter.get('nom_complet'):
            return item

        # Default values
        priorite_pub = 0
        completude_profil = 0.5

        insert_query = """
        INSERT INTO medecins (
            nom_complet, specialite, wilaya, adresse, telephone, 
            site_web, photo_url, latitude, longitude,
            priorite_pub, completude_profil
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING; -- Assuming ID won't conflict, but ideally we check uniqueness on Name+Phone or something
        """
        
        # Determine strict logic for duplicates? 
        # For now, simplistic insert.
        
        self.cur.execute(insert_query, (
            adapter.get('nom_complet'),
            adapter.get('specialite'),
            adapter.get('wilaya'),
            adapter.get('adresse'),
            adapter.get('telephone'),
            adapter.get('site_web'),
            adapter.get('photo_url'),
            adapter.get('latitude'),
            adapter.get('longitude'),
            priorite_pub,
            completude_profil
        ))
        self.connection.commit()
        return item
