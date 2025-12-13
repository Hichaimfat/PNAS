import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { NextIntlClientProvider, useMessages } from 'next-intl';
import LanguageSwitcher from "@/components/LanguageSwitcher";
import "../globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "PNAS - Pôle Numérique Algérien de Santé",
    description: "Annuaire des médecins algériens.",
};

export default function LocaleLayout({
    children,
    params: { locale }
}: {
    children: React.ReactNode;
    params: { locale: string };
}) {
    // Receive messages provided in `i18n.ts`
    const messages = useMessages();
    const dir = locale === 'ar' ? 'rtl' : 'ltr';

    return (
        <html lang={locale} dir={dir}>
            <body className={inter.className}>
                <NextIntlClientProvider locale={locale} messages={messages}>
                    <LanguageSwitcher />
                    {children}
                </NextIntlClientProvider>
            </body>
        </html>
    );
}
