# Bibliothèques récupérées du projet

Les objets de ce dossier proviennent du PCB et du schéma intégrés au commit matériel `57c3111`. Ils ont été récupérés pour rendre les dépendances personnalisées accessibles sur un autre poste, sans modifier les fichiers de circuit.

- `recovered-footprints/` : 11 empreintes dans 10 bibliothèques, exportées avec l'API KiCad 10.0.5 depuis le PCB. La première instance d'un identifiant a servi de snapshot.
- `recovered-symbols/` : définitions intégrées des bibliothèques `Symbols`, `cirbattverter_Library` et `CS4200V_01`.
- `../fp-lib-table` et `../sym-lib-table` : références relatives avec `${KIPRJMOD}`. Les bibliothèques standard restent fournies par KiCad.

Ce sont des **snapshots**, pas de nouvelles définitions certifiées. L'empreinte LM5013 contient des pads thermiques numérotés en plus des broches du symbole. Les instances U3/U4 diffèrent dans les affectations de ces pads ; comparer avant toute mise à jour depuis une bibliothèque.

Les modèles 3D locaux sont référencés vers `3d/` lorsque le fichier correspondant existe. Certains chemins historiques restent manquants dans les objets déjà présents dans le PCB. Voir l'[audit](../../../docs/07-audit-technique.md).

Les anciens fichiers `Components_models/`, archives, `.pretty` et `3d/` sont conservés pour la traçabilité. Ne pas les supprimer avant de vérifier leur provenance et les variantes utiles. Les sources et attributions déjà présentes dans le dépôt sont conservées.
