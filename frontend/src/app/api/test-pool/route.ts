import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

export async function GET() {
    try {
        const { Pool } = await import('pg');

        // Just create pool, don't query yet
        const pool = new Pool({
            connectionString: process.env.DATABASE_URL,
            ssl: {
                rejectUnauthorized: false
            }
        });

        return NextResponse.json({
            status: 'OK',
            message: 'Pool created successfully',
            hasConnectionString: !!process.env.DATABASE_URL,
            connectionStringLength: process.env.DATABASE_URL?.length
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
