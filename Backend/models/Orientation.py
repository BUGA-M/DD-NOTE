
class OrientationOFPPT:

    bac_categories = {
        "scientifique": [
            "Sciences Mathématiques A", "Sciences Mathématiques B",
            "Sciences Physiques", "Sciences de la Vie et de la Terre",
            "Sciences Agronomiques", 
            "2ème Bac Sciences Mathématiques A (BIOF)", "2ème Bac Sciences Mathématiques B (BIOF)",
            "2ème Bac Sciences Physiques (BIOF)", "2ème Bac Sciences de la Vie et de la Terre (SVT) (BIOF)",
            "2ème Bac Sciences Agronomiques (BIOF)"
        ],
        "technique": [
            "Sciences et Technologies Électriques", "Sciences et Technologies Mécaniques",
            "2ème Bac Sciences et Technologies Électriques (BIOF)", "2ème Bac Sciences et Technologies Mécaniques (BIOF)",
            "Arts Appliqués"
        ],
        "economique": [
            "Sciences Économiques", "Sciences de Gestion Comptable"
        ],
        "litteraire": [
            "Lettres", "Sciences Humaines", "Langue Arabe", "Sciences Islamiques"
        ]
    }

    # Filières proposées selon la catégorie de bac
    filieres_par_categorie = {
        "scientifique": ["développement digital", "réseaux informatiques", "génie civil", "génie électrique", "agroalimentaire", "biotechnologie"],
        "technique": ["électromécanique", "maintenance industrielle", "design graphique", "mécatronique","développement digital", "réseaux informatiques", "génie civil"],
        "economique": ["gestion des entreprises", "finance-comptabilité", "commerce international"],
        "litteraire": ["secrétariat", "communication", "éducation préscolaire"]
    }

    @classmethod
    def get_filiere_from_bac(cls, bac_type):
        for categorie, bacs in cls.bac_categories.items():
            if bac_type in bacs:
                return cls.filieres_par_categorie.get(categorie, ["Pas de filières disponibles."])
        return ["Type de bac non reconnu."]
