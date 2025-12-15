import { NextRequest, NextResponse } from 'next/server';
import { sql } from '@vercel/postgres';

export const dynamic = 'force-dynamic';

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

        query += ` ORDER BY priorite_pub DESC NULLS LAST`;
        query += ` OFFSET $${paramIndex} LIMIT $${paramIndex + 1}`;
        params.push(skip, limit);

        const result = await sql.query(query, params);

        return NextResponse.json(result.rows);
    } catch (error: any) {
        console.error('Database error:', error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
