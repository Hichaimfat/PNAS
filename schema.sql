-- Enable Extensions
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Tables
CREATE TABLE IF NOT EXISTS wilayas (
    id SERIAL PRIMARY KEY,
    nom TEXT NOT NULL UNIQUE
);

CREATE INDEX IF NOT EXISTS ix_wilayas_nom ON wilayas (nom);

CREATE TABLE IF NOT EXISTS specialites (
    id SERIAL PRIMARY KEY,
    nom TEXT NOT NULL UNIQUE
);

CREATE INDEX IF NOT EXISTS ix_specialites_nom ON specialites (nom);

CREATE TABLE IF NOT EXISTS medecins (
    id SERIAL PRIMARY KEY,
    nom_complet TEXT NOT NULL,
    specialite TEXT NOT NULL,
    wilaya TEXT NOT NULL,
    adresse TEXT,
    telephone TEXT,
    latitude FLOAT,
    longitude FLOAT,
    site_web TEXT,
    photo_url TEXT,
    priorite_pub INTEGER DEFAULT 0,
    completude_profil FLOAT DEFAULT 0.5,
    date_derniere_mise_a_jour TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    informations_additionnelles JSONB DEFAULT '{}'::jsonb
);

-- Basic Indexes
CREATE INDEX IF NOT EXISTS ix_medecins_nom_complet ON medecins (nom_complet);
CREATE INDEX IF NOT EXISTS ix_medecins_specialite ON medecins (specialite);
CREATE INDEX IF NOT EXISTS ix_medecins_wilaya ON medecins (wilaya);

-- Advanced Search Indexes (GIN/Trigram)
CREATE INDEX IF NOT EXISTS ix_medecins_nom_complet_trgm ON medecins USING gin (nom_complet gin_trgm_ops);
CREATE INDEX IF NOT EXISTS ix_medecins_specialite_trgm ON medecins USING gin (specialite gin_trgm_ops);
