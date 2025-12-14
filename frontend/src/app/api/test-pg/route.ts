import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

export async function GET() {
    try {
        // Try to import pg
        const { Pool } = await import('pg');

        return NextResponse.json({
            status: 'OK',
            message: 'pg module loaded successfully',
            Pool: typeof Pool
        });
    } catch (error: any) {
        return NextResponse.json({
            status: 'ERROR',
            error: error.message,
            stack: error.stack
        }, { status: 500 });
    }
}
