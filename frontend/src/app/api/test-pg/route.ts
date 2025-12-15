import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

export async function GET() {
    try {
        // Try to import pg and connect
        const { Pool } = await import('pg');

        const pool = new Pool({
            connectionString: process.env.DATABASE_URL,
            ssl: {
                rejectUnauthorized: false
            }
        });

        const result = await pool.query('SELECT NOW()');
        await pool.end();

        return NextResponse.json({
            status: 'OK',
            message: 'Database connection successful',
            timestamp: result.rows[0].now
        });
    } catch (error: any) {
        return NextResponse.json({
            status: 'ERROR',
            error: error.message,
            stack: error.stack,
            code: error.code
        }, { status: 500 });
    }
}
