"use client";

import { useLocale } from "next-intl";
import { usePathname, useRouter } from "@/navigation";
import { useTransition } from "react";

export default function LanguageSwitcher() {
    const locale = useLocale();
    const router = useRouter();
    const pathname = usePathname();
    const [isPending, startTransition] = useTransition();

    const toggleLanguage = () => {
        const nextLocale = locale === "fr" ? "ar" : "fr";
        startTransition(() => {
            router.replace(pathname, { locale: nextLocale });
        });
    };

    return (
        <button
            onClick={toggleLanguage}
            disabled={isPending}
            className="fixed top-4 right-4 bg-white/90 backdrop-blur shadow-md px-4 py-2 rounded-full font-bold text-blue-600 hover:bg-gray-100 transition z-50 flex items-center gap-2"
        >
            <span>{locale === "fr" ? "العربية" : "Français"}</span>
            <span className="text-xl">{locale === "fr" ? "🇩🇿" : "🇫🇷"}</span>
        </button>
    );
}
