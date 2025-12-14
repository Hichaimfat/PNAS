import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
    try {
        // Check authorization
        const authHeader = request.headers.get('authorization');
        const cronSecret = process.env.CRON_SECRET;

        if (cronSecret && authHeader !== `Bearer ${cronSecret}`) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        // Note: Scrapy cannot run in Next.js serverless environment
        // This endpoint is kept for compatibility but returns a message
        // In production, you would:
        // 1. Use a separate scraping service (e.g., GitHub Actions, Render Cron)
        // 2. Or implement a Node.js-based scraper using cheerio/puppeteer

        return NextResponse.json({
            message: 'Scraper endpoint - requires external service',
            note: 'Scrapy cannot run in serverless. Use GitHub Actions or separate service.'
        });
    } catch (error: any) {
        console.error('Scraper error:', error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
