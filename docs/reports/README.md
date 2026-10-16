# Rapports de vérification

## Révision reçue le 16 octobre 2026

[Revue actuelle](../10-revue-corrections-2026-10-16.md) · [Synthèse JSON](2026-10-16/summary.json) · [Manifeste du ZIP](2026-10-16/input-manifest.json) · [ERC](2026-10-16/erc.json) · [DRC courant](2026-10-16/drc-inverter.json) · [DRC renforcé sur copie](2026-10-16/drc-inverter-clearance-enabled.json) · [DRC planaire conservé](2026-10-16/drc-planar.json).

Le manifeste racine [source-manifest.csv](source-manifest.csv) décrit les sources courantes avec fins de ligne Git LF. Le [manifeste du 14 octobre](2026-10-14/source-manifest.csv) reste conservé pour l'audit initial. Le CSV J5 et les inventaires racine décrivent la révision actuelle.

## Rapports historiques du 14 octobre 2026

[Audit expliqué](../07-audit-technique.md) · [Guide](../README.md)

Rapports KiCad CLI 10.0.5 du 14 octobre 2026. Les chemins de source ont été rendus relatifs pour publier le dossier sans chemin du poste local ; les signalements et objets sont conservés.

| Fichier | Signification |
| --- | --- |
| [erc-original.json](erc-original.json) | 39 signalements avant récupération des bibliothèques |
| [erc-current.json](erc-current.json) | 20 signalements après récupération, schéma inchangé |
| [drc-inverter-original.json](drc-inverter-original.json) | 179 DRC + 26 parités avec règles originales |
| [drc-inverter-current.json](drc-inverter-current.json) | 157 DRC + 26 parités après récupération |
| [drc-inverter-clearance-enabled.json](drc-inverter-clearance-enabled.json) | 185 DRC dont 28 erreurs + 26 parités sur copie avec 3 règles réactivées |
| [drc-planar.json](drc-planar.json) | 50 DRC dont 40 erreurs sur le planaire |
| [controller-documents.json](controller-documents.json) | SHA-256 et constats des trois PDF fournis par le porteur du projet |
| [source-manifest.csv](source-manifest.csv) | SHA-256 des circuits/projets/exports historiques analysés |
| [components-from-schematic.csv](components-from-schematic.csv) | Les 160 composants électriques avec champs source |
| [connector-nets.csv](connector-nets.csv) | Nets extraits des bornes et interfaces |
| [egs005q-interface-review.csv](egs005q-interface-review.csv) | Comparaison des 29 pads J5 avec le module et vérification des circuits associés |

Le fichier de règles principal `.kicad_dru` est vide. Les contrôles ignorés et niveaux de sévérité figurent dans les projets et dans chaque rapport JSON. Une absence de signalement pour une règle ignorée ne constitue pas un résultat positif.

Le rapport renforcé provient d'une copie du projet avec **uniquement** `clearance`, `hole_clearance` et `annular_width` passés de « ignore » à « error ». Les autres exclusions et seuils restent ceux du projet ; ce n'est pas une vérification exhaustive d'isolation haute tension.

Pour régénérer les contrôles courants sans modifier les sources, utiliser [tools/export-review.ps1](../../tools/export-review.ps1). Le contrôle renforcé se fait séparément sur une copie. Ne pas écraser les rapports datés d'une révision par ceux d'un autre circuit sans mettre à jour l'audit et le manifeste.

Un code retour nul de `kicad-cli` sans `--exit-code-violations` indique la génération du rapport, pas l'absence de violations.
