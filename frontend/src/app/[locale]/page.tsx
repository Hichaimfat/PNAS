"use client";

import { useState, useEffect } from "react";
import MedecinCard from "@/components/MedecinCard";
import { Search } from "lucide-react";
import { useTranslations } from "next-intl";

interface Medecin {
    id: number;
    nom_complet: string;
    specialite: string;
    wilaya: string;
    telephone?: string;
    priorite_pub: number;
}

export default function Home() {
    const t = useTranslations('Index');
    const [medecins, setMedecins] = useState<Medecin[]>([]);
    const [loading, setLoading] = useState(false);
    const [filters, setFilters] = useState({
        wilaya: "",
        specialite: "",
        q: "",
    });

    const fetchMedecins = async () => {
        setLoading(true);
        try {
            const params = new URLSearchParams();
            if (filters.wilaya) params.append("wilaya", filters.wilaya);
            if (filters.specialite) params.append("specialite", filters.specialite);
            if (filters.q) params.append("q", filters.q);

            // In production, use environment variable for API URL
            let apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
            if (!apiUrl.startsWith('http')) {
                apiUrl = `https://${apiUrl}`;
            }
            const res = await fetch(`${apiUrl}/api/medecins/recherche?${params.toString()}`);
            if (res.ok) {
                const data = await res.json();
                setMedecins(data);
            }
        } catch (error) {
            console.error("Failed to fetch medecins", error);
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        fetchMedecins();
    };

    // Initial load
    useEffect(() => {
        fetchMedecins();
    }, []);

    return (
        <main className="min-h-screen bg-gray-50 flex flex-col items-center">
            {/* Hero Section */}
            <div className="w-full bg-blue-600 text-white py-16 px-4 text-center relative">
                <h1 className="text-4xl font-bold mb-4">{t('title')}</h1>
                <p className="text-xl opacity-90 mb-8">{t('searchPlaceholder')}</p>

                {/* Search Bar */}
                <form onSubmit={handleSearch} className="max-w-4xl mx-auto bg-white p-4 rounded-lg shadow-lg flex flex-col md:flex-row gap-4 text-gray-900">
                    <input
                        type="text"
                        placeholder={t('searchPlaceholder')}
                        className="flex-grow p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        value={filters.q}
                        onChange={(e) => setFilters({ ...filters, q: e.target.value })}
                    />
                    <input
                        type="text"
                        placeholder="Wilaya (ex: Alger)"
                        className="md:w-48 p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        value={filters.wilaya}
                        onChange={(e) => setFilters({ ...filters, wilaya: e.target.value })}
                    />
                    <input
                        type="text"
                        placeholder="Spécialité"
                        className="md:w-48 p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        value={filters.specialite}
                        onChange={(e) => setFilters({ ...filters, specialite: e.target.value })}
                    />
                    <button
                        type="submit"
                        className="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-3 px-8 rounded-md transition-colors flex items-center justify-center gap-2 rtl:flex-row-reverse"
                    >
                        <Search size={20} />
                        {t('searchButton')}
                    </button>
                </form>
            </div>

            {/* Results Section */}
            <div className="w-full max-w-6xl px-4 py-8">
                <h2 className="text-2xl font-bold mb-6 text-gray-800">Résultats ({medecins.length})</h2>

                {loading ? (
                    <div className="text-center py-12">Chargement...</div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {medecins.map((medecin) => (
                            <MedecinCard key={medecin.id} medecin={medecin} />
                        ))}
                    </div>
                )}
            </div>
        </main>
    );
}
