import { NextRequest, NextResponse } from 'next/server';
import pool from '@/lib/db';

export async function GET(request: NextRequest) {
    try {
        // Check authorization
        const authHeader = request.headers.get('authorization');
        const cronSecret = process.env.CRON_SECRET;

        if (cronSecret && authHeader !== `Bearer ${cronSecret}`) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        // Run migrations by executing SQL directly
        // This is a simplified version - in production you'd use a proper migration tool
        const migrationSQL = `
      CREATE TABLE IF NOT EXISTS medecins (
        id SERIAL PRIMARY KEY,
        nom_complet VARCHAR(255),
        specialite VARCHAR(255),
        wilaya VARCHAR(100),
        adresse TEXT,
        telephone VARCHAR(50),
        email VARCHAR(255),
        site_web VARCHAR(255),
        horaires TEXT,
        priorite_pub INTEGER DEFAULT 0,
        completude_profil INTEGER DEFAULT 0,
        date_derniere_mise_a_jour TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );

      CREATE TABLE IF NOT EXISTS wilayas (
        id SERIAL PRIMARY KEY,
        code VARCHAR(10) UNIQUE,
        nom VARCHAR(100),
        nom_ar VARCHAR(100)
      );

      CREATE TABLE IF NOT EXISTS specialites (
        id SERIAL PRIMARY KEY,
        nom VARCHAR(255) UNIQUE,
        nom_ar VARCHAR(255)
      );

      CREATE INDEX IF NOT EXISTS idx_medecins_wilaya ON medecins(wilaya);
      CREATE INDEX IF NOT EXISTS idx_medecins_specialite ON medecins(specialite);
      CREATE INDEX IF NOT EXISTS idx_medecins_priorite ON medecins(priorite_pub);
    `;

        await pool.query(migrationSQL);

        return NextResponse.json({
            message: 'Migrations successful',
            output: 'Tables created successfully'
        });
    } catch (error: any) {
        console.error('Migration error:', error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
