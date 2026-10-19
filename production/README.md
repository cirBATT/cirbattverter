# Exports de production non approuvés

**ZIP Gerber principal remplacé par celui reçu le 19 octobre, exporté le 17 octobre.** Les quatre couches cuivre et les deux masques sont présents ; le dossier reste non approuvé. BOM/CPL et planaire inchangés. Lire la [revue actuelle](../docs/11-revue-corrections-2026-10-19.md).

**Lire l'[audit](../docs/07-audit-technique.md) et le [guide de fabrication](../docs/05-fabrication.md) avant usage. Cette révision ne constitue pas un ensemble approuvé pour commande.**

| Dossier / fichier | État revérifié le 19 octobre 2026 |
| --- | --- |
| `inverter/gerber.zip` | 14 fichiers : quatre cuivres, deux masques, profil, sérigraphies/pâtes, gbrjob et perçages PTH/NPTH ; non approuvé |
| `inverter/*_JLCPCB_BOM.xlsx` | 61 lignes groupées, 160 repères ; valeurs et références critiques à compléter |
| `inverter/*_CPL_JLCPCB.xlsx` | 160 positions, y compris traversants ; rotations/polarités à valider |
| `planar-transformer/Gerbers.zip` | 8 couches cuivre, masques et perçages présents ; erreurs DRC et magnétique à traiter |
| `planar-transformer/gerbers/` | Même contenu de fichiers que l'archive du planaire |

Les deux jeux `.gbrjob` décrivent 35 µm de cuivre sur toutes les couches, contrairement aux 70 µm demandés dans le README d'origine. Les exports sont conservés comme preuves de la révision, sans ajouter silencieusement des couches ou changer l'empilage.

Pour publier une version fabricable : identifier le commit corrigé, approuver l'empilage, recalculer les zones, passer les contrôles, regénérer **ensemble** Gerbers/perçages/BOM/CPL et vérifier le visualiseur de fabrication. Joindre la nomenclature système, le noyau et les fichiers de configuration des modules.

Pour une intégration avec une batterie, les [packs de seconde vie cirBATT](https://cirbatt.com/packs) sont présentés sur le site de la marque ; leur compatibilité avec le circuit doit être établie séparément dans le [dossier batterie](../docs/09-batteries-seconde-vie.md).
