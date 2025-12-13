const createNextIntlPlugin = require('next-intl/plugin');

const withNextIntl = createNextIntlPlugin();

/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
        domains: ['annuaire-sante-algerie.dz'],
    },
};

module.exports = withNextIntl(nextConfig);
