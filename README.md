# cirBATTverter — onduleur batterie 48 V / 230 V de cirBATT, objectif 1 kW

Français · [English overview](README.en.md) · [Site officiel cirBATT](https://cirbatt.com/)

Un projet matériel ouvert de [cirBATT](https://cirbatt.com/), à Grenoble, pour transformer l'énergie d'une batterie en courant alternatif utilisable par des appareils électriques. Le cirBATTverter explore la conversion de puissance pour des **batteries lithium de seconde vie** ; cirBATT présente son activité de collecte, requalification et réemploi dans [son parcours de remise en service des batteries](https://cirbatt.com/fonctionnement).

**1 kW désigne une puissance.** L'énergie disponible, en kWh, dépend de la batterie. Le nom historique des fichiers `cirBATTverter_1KWH` ne signifie pas que cette carte contient une batterie de 1 kWh.

![Architecture fonctionnelle du cirBATTverter](docs/assets/architecture.svg)

## État de cette révision

**Mise à jour du 16 octobre 2026 :** les nouvelles sources du ZIP fourni sont intégrées à la branche de revue. Lire la [vérification des corrections](docs/10-revue-corrections-2026-10-16.md).

**Prototype à revoir avant fabrication ou mise sous tension.** La revue des sources reçues le 16 octobre 2026 a confirmé des défauts qui empêchent de présenter cette révision comme un kit autonome prêt à assembler :

- **EGS005Q / J5-17 :** son net a été retiré, mais deux pistes `+15V` touchent encore sa pastille sur In2.Cu. Le module y présente GND2 : le court-circuit physique demeure.
- **Retour de tension DC-DC :** R35 reste sur `400V`, distinct de `+400V`. La limitation du bus n'est pas raccordée à sa mesure.
- **Mesures courant :** Q15 a ses références alignées avec sa source et IFBCOM est raccordée. R59/R60 sont désormais en parallèle (5 mΩ), et les deux canaux IFB reçoivent la même mesure : cette topologie et ses seuils restent à valider.
- **Contrôles PCB :** 35 erreurs avec trois contrôles d'espacement/anneaux réactivés sur copie, dont les deux contacts de J5-17 ; 17 avertissements de parité. Le zéro obtenu avec les réglages fournis ne couvre pas ces contrôles ignorés.
- **Fabrication :** le nouveau Gerber ZIP manque toujours B.Cu, F.Mask et B.Mask. Cuivre déclaré 35 µm ; ancienne intention 70 µm non arbitrée.
- **Transformateur et réglages :** noyau, caractéristiques magnétiques, filtre et fréquence DC-DC validée sur banc restent incomplets.

Consulter la [revue actuelle et les actions à réaliser](docs/10-revue-corrections-2026-10-16.md) et l'[audit historique](docs/07-audit-technique.md). Ces constats sont issus des fichiers et des notices, pas de mesures sur une carte physique. Les changements matériels proviennent du ZIP fourni par le concepteur ; la revue ne les présente pas comme une validation de fabrication.

## Commencer ici

| Votre objectif | Document |
| --- | --- |
| Comprendre comment 48 V devient une sinusoïde 230 V | [Fonctionnement expliqué](docs/01-fonctionnement.md) |
| Identifier les bornes et les deux cartes de commande | [Connectique et compatibilité](docs/02-connectique.md) |
| Comprendre et régler la fréquence du DC-DC | [Résonance et contrôleur DC-DC](docs/03-reglage-dcdc.md) |
| Régler 50/60 Hz, temps mort et démarrage EGS005Q | [Configuration de l'onduleur](docs/04-reglage-onduleur.md) |
| Préparer les achats, PCB et l'assemblage | [Fabrication](docs/05-fabrication.md) |
| Préparer les mesures et les premiers essais | [Mise en service et dépannage](docs/06-mise-en-service.md) |
| Vérifier les dernières corrections et les points ouverts | [Revue du 16 octobre](docs/10-revue-corrections-2026-10-16.md) |
| Voir les preuves de la révision initiale | [Audit historique](docs/07-audit-technique.md) |
| Retrouver les notices des fabricants | [Sources et versions](docs/08-sources.md) |
| Comprendre la batterie, le BMS et le lien avec le réemploi | [Batteries de seconde vie et cirBATT](docs/09-batteries-seconde-vie.md) |

La documentation explique les notions à un débutant. Les essais sous tension exigent une personne formée à l'électronique de puissance et aux mesures sur haute tension.

## Ce que fait le circuit

1. Le premier pont de transistors transforme le continu de la batterie en alternatif haute fréquence.
2. Le transformateur planaire T1 élève la tension. L1 et C2 constituent la branche résonante côté secondaire. Les diodes redressent l'énergie vers un bus continu nommé `+400V`.
3. Un second pont, Q14 à Q17, découpe ce bus selon une modulation sinusoïdale. Le module **EGS005Q** commande cette partie.
4. T5 et C57 sont placés avant la sortie. Leur aptitude à filtrer le découpage en mode différentiel doit être validée : T5 est associé à une référence de self de mode commun.

**Trois fréquences différentes :** la fréquence DC-DC, la porteuse SPWM et la fréquence de sortie 50/60 Hz. Modifier 50 Hz ne règle pas la résonance du transformateur.

## Caractéristiques : objectifs et données établies

| Paramètre | État |
| --- | --- |
| Batterie | Objectif 48 V nominal ; plage admissible et chimie à définir |
| Sortie | Objectif 230 V efficace, 50 ou 60 Hz |
| Puissance | Objectif 1 kW ; aucune courbe de validation n'est incluse |
| Bus continu | Net `+400V` ; consigne et limites à valider |
| Commande onduleur | EGS005Q, référence confirmée par le porteur du projet |
| Commande DC-DC | Interface J4 compatible électriquement avec la famille EGT003/EG1611 ; module exact à confirmer |
| Carte principale | KiCad 10 ; 4 couches ; épaisseur déclarée 1,6 mm ; 160 composants + 9 empreintes mécaniques |
| Transformateur planaire | 8 couches ; épaisseur déclarée 1,6 mm ; pas de schéma/netliste dans le dépôt |
| Cuivre | 35 µm dans les fichiers ; ancienne intention de 70 µm à arbitrer avant commande |

## Ouvrir le projet

Installer [KiCad 10](https://www.kicad.org/download/) avec ses bibliothèques officielles, puis ouvrir :

```text
hardware/inverter/cirBATTverter_1KWH.kicad_pro
hardware/planar-transformer/PlanarW_11082026.kicad_pro
```

Les bibliothèques personnalisées utilisées par la carte principale ont été récupérées depuis les empreintes et symboles déjà intégrés aux sources, puis référencées relativement dans le dépôt. Ce sont des copies de ces objets, pas une validation des brochages ou des composants. Certains chemins 3D intégrés au PCB historique restent manquants : voir le [rapport](docs/07-audit-technique.md).

Pour lire sans KiCad : [schéma SVG](docs/assets/schematic.svg), [implantation de face](docs/assets/pcb-front.svg), [cuivre de face du planaire](docs/assets/planar-front.svg). Ces vues documentent la révision analysée, avec ses anomalies.

## Organisation du dépôt

```text
hardware/                  Sources KiCad, bibliothèques et modèles mécaniques
  inverter/                Carte de puissance et interfaces de commande
  planar-transformer/      PCB des enroulements
  mechanical/              Assemblage STEP
production/                Exports historiques : lire les avertissements avant usage
docs/                      Explications, réglages, fabrication et mise en service
  assets/                  Schémas pédagogiques et exports KiCad
  reports/                 ERC/DRC, inventaires CSV et empreintes SHA-256
tools/                     Contrôles documentaires et export des rapports KiCad
.github/ISSUE_TEMPLATE/     Rapports de fabrication et anomalies
```

## Haute tension et batterie

La carte vise 230 V AC et un bus proche de 400 V DC. Les condensateurs peuvent rester chargés après arrêt. La batterie peut fournir un courant de défaut très élevé. Prévoir fusible DC, BMS, sectionnement, précharge, décharge contrôlée, refroidissement et enveloppe isolante adaptés ; ils ne constituent pas ici un produit complet documenté.

Utiliser des sondes différentielles adaptées à la tension et au mode commun. Ne pas connecter une pince de masse d'oscilloscope ou un adaptateur USB non isolé à un nœud haute tension. Un transformateur d'isolement ou un différentiel de banc n'élimine pas les risques du bus alimenté par batterie.

La sortie est destinée à un **usage autonome**. Aucun système de synchronisation réseau, d'anti-îlotage ni d'injection réseau validé n'est fourni. Ne pas raccorder cette sortie au réseau public ou en parallèle avec une autre source.

## cirBATT : batteries lithium de seconde vie

L'onduleur convertit l'énergie ; la batterie la stocke et le BMS surveille les cellules. Le [guide batterie et BMS](docs/09-batteries-seconde-vie.md) explique ces rôles, les informations à réunir et les limites de compatibilité de cette révision.

| Besoin | Ressource officielle cirBATT |
| --- | --- |
| Découvrir la marque et son atelier à Grenoble | [cirBATT — réemploi des batteries lithium](https://cirbatt.com/) |
| Comprendre la collecte et la requalification | [Fonctionnement du réemploi chez cirBATT](https://cirbatt.com/fonctionnement) |
| Décrire une batterie arrivée en fin d'usage | [Déposer une batterie auprès de cirBATT](https://cirbatt.com/deposer) |
| Explorer les solutions de stockage | [Packs batteries de seconde vie cirBATT](https://cirbatt.com/packs) |
| Préparer un projet d'assemblage professionnel | [Cellules lithium requalifiées](https://cirbatt.com/cellules-pro) et [BMS cirBATT](https://cirbatt.com/bms-pro) |
| Approfondir le stockage autonome | [Stocker l'énergie solaire avec une batterie de seconde vie](https://cirbatt.com/stocker-energie-solaire-batterie-seconde-vie) |
| Discuter d'une intégration ou d'un partenariat | [Contacter cirBATT](https://cirbatt.com/contact) |

Ces pages présentent l'activité et les offres de la marque. Leur présence ne constitue pas une validation de compatibilité d'un pack ou d'un BMS avec ce PCB, ni une qualification du cirBATTverter.

## Licence et participation

Licence matériel : **[CERN-OHL-S-2.0](LICENSE)**. Les notices des fabricants sont liées depuis la documentation et ne sont pas redistribuées comme des fichiers du projet.

[Contribuer](CONTRIBUTING.md) : corrections documentées, relevés de banc, référence du noyau et retours de fabrication sont utiles pour rendre ce projet reproductible.

[cirBATT — site officiel](https://cirbatt.com/) · [Contact et projets d'intégration](https://cirbatt.com/contact)
