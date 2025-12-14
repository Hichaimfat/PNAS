import { NextRequest, NextResponse } from 'next/server';
import pool from '@/lib/db';

export async function GET(request: NextRequest) {
    try {
        const searchParams = request.nextUrl.searchParams;
        const q = searchParams.get('q');
        const wilaya = searchParams.get('wilaya');
        const specialite = searchParams.get('specialite');
        const skip = parseInt(searchParams.get('skip') || '0');
        const limit = parseInt(searchParams.get('limit') || '20');

        let query = 'SELECT * FROM medecins WHERE 1=1';
        const params: any[] = [];
        let paramIndex = 1;

        if (wilaya) {
            query += ` AND LOWER(wilaya) = LOWER($${paramIndex})`;
            params.push(wilaya);
            paramIndex++;
        }

        if (specialite) {
            query += ` AND LOWER(specialite) = LOWER($${paramIndex})`;
            params.push(specialite);
            paramIndex++;
        }

        if (q) {
            query += ` AND (LOWER(nom_complet) LIKE LOWER($${paramIndex}) OR LOWER(specialite) LIKE LOWER($${paramIndex}))`;
            params.push(`%${q}%`);
            paramIndex++;
        }

        // Sorting by priority
        query += ` ORDER BY priorite_pub DESC NULLS LAST, 
               CASE 
                 WHEN priorite_pub = 3 THEN date_derniere_mise_a_jour 
                 WHEN priorite_pub = 2 THEN completude_profil::text
                 WHEN priorite_pub = 1 THEN date_derniere_mise_a_jour
                 ELSE nom_complet
               END DESC NULLS LAST`;

        query += ` OFFSET $${paramIndex} LIMIT $${paramIndex + 1}`;
        params.push(skip, limit);

        const result = await pool.query(query, params);

        return NextResponse.json(result.rows);
    } catch (error) {
        console.error('Database error:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}
