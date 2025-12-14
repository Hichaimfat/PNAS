import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

export async function GET() {
    try {
        return NextResponse.json({
            status: 'OK',
            env: {
                hasDatabaseUrl: !!process.env.DATABASE_URL,
                databaseUrlLength: process.env.DATABASE_URL?.length || 0,
                databaseUrlPrefix: process.env.DATABASE_URL?.substring(0, 30) + '...',
                nodeEnv: process.env.NODE_ENV,
                vercelEnv: process.env.VERCEL_ENV
            }
        });
    } catch (error: any) {
        return NextResponse.json({
            status: 'ERROR',
            error: error.message,
            stack: error.stack
        }, { status: 500 });
    }
}
