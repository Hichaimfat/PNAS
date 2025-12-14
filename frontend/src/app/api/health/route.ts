import { NextResponse } from 'next/server';
import pool from '@/lib/db';

export const dynamic = 'force-dynamic';

export async function GET() {
    try {
        // Test simple de connexion
        const result = await pool.query('SELECT NOW()');

        return NextResponse.json({
            status: 'OK',
            database: 'Connected',
            timestamp: result.rows[0].now,
            env: {
                hasDatabaseUrl: !!process.env.DATABASE_URL,
                databaseUrlPrefix: process.env.DATABASE_URL?.substring(0, 20) + '...'
            }
        });
    } catch (error: any) {
        return NextResponse.json({
            status: 'ERROR',
            error: error.message,
            stack: error.stack,
            env: {
                hasDatabaseUrl: !!process.env.DATABASE_URL,
                databaseUrlPrefix: process.env.DATABASE_URL?.substring(0, 20) + '...'
            }
        }, { status: 500 });
    }
}
