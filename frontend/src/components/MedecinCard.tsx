import React from 'react';
import { clsx } from 'clsx';
import { Phone, MapPin, Stethoscope } from 'lucide-react';
import { useTranslations } from 'next-intl';

interface MedecinProps {
    id: number;
    nom_complet: string;
    specialite: string;
    wilaya: string;
    telephone?: string;
    priorite_pub: number;
}

const MedecinCard: React.FC<{ medecin: MedecinProps }> = ({ medecin }) => {
    const t = useTranslations('Index');
    const isSponsored = medecin.priorite_pub >= 3;
    const isPremium = medecin.priorite_pub === 2;

    return (
        <div className={clsx(
            "p-6 rounded-lg shadow-md bg-white transition-all hover:shadow-xl border",
            isSponsored ? "border-yellow-500 ring-1 ring-yellow-400" : "border-gray-200",
            isPremium ? "border-blue-200" : ""
        )}>
            <div className="flex justify-between items-start">
                <div>
                    {isSponsored && (
                        <span className="bg-yellow-100 text-yellow-800 text-xs font-semibold px-2 py-0.5 rounded mb-2 inline-block">
                            {t('sponsored')}
                        </span>
                    )}
                    <h3 className="text-xl font-bold text-gray-900">{medecin.nom_complet}</h3>
                    <p className="text-blue-600 font-medium flex items-center gap-2 mt-1">
                        <Stethoscope size={16} /> {medecin.specialite}
                    </p>
                </div>
            </div>

            <div className="mt-4 space-y-2 text-gray-600">
                <div className="flex items-center gap-2">
                    <MapPin size={16} />
                    <span>{medecin.wilaya}</span>
                </div>
                {medecin.telephone && (
                    <div className="flex items-center gap-2">
                        <Phone size={16} />
                        <span dir="ltr">{medecin.telephone}</span>
                    </div>
                )}
            </div>

            <button className="mt-4 w-full bg-blue-50 text-blue-600 py-2 rounded-md hover:bg-blue-100 font-medium transition-colors">
                Voir Profil
            </button>
        </div>
    );
};

export default MedecinCard;
