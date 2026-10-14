# cirBATTverter — onduleur 48 V / 230 V, objectif 1 kW

Un projet matériel ouvert de [cirBATT](https://cirbatt.com), à Grenoble, pour transformer l'énergie d'une batterie en courant alternatif utilisable par des appareils électriques.

**1 kW désigne une puissance.** L'énergie disponible, en kWh, dépend de la batterie. Le nom historique des fichiers `cirBATTverter_1KWH` ne signifie pas que cette carte contient une batterie de 1 kWh.

![Architecture fonctionnelle du cirBATTverter](docs/assets/architecture.svg)

## État de cette révision

**Prototype à revoir avant fabrication ou mise sous tension.** L'analyse des sources du 14 octobre 2026 a identifié des défauts qui empêchent de présenter cette révision comme un kit autonome prêt à assembler :

- **EGS005Q / J5 :** la broche 17 est une masse sur le module officiel, mais reçoit le rail `+15V` sur la carte. Un montage direct peut court-circuiter l'alimentation auxiliaire. La protection `IFBCOM`, broche 26, est laissée ouverte.
- **Retour de tension DC-DC :** le diviseur R35/R36 est connecté au net `400V`, distinct du bus `+400V`. La limitation du bus n'est donc pas reliée à la tension qu'elle devrait surveiller dans la netliste.
- **Cuivre du PCB :** un contrôle des espacements réactivé sur une copie signale trois contacts entre `U4-FB` et des vias du rail `+15V`.
- **Fabrication :** l'archive Gerber principale est incomplète. Le cuivre est annoncé à 70 µm dans l'ancien README mais défini à 35 µm dans les deux PCB et leurs fichiers de fabrication.
- **Transformateur et réglages :** la référence du noyau, les caractéristiques magnétiques et une fréquence DC-DC validée sur banc ne sont pas fournies.

Consulter le [rapport technique et les actions à réaliser](docs/07-audit-technique.md). Ces constats sont issus des fichiers et des notices, pas de mesures sur une carte physique. Les schémas, pistes et fichiers de fabrication n'ont pas été corrigés par la restructuration documentaire.

## Commencer ici

| Votre objectif | Document |
| --- | --- |
| Comprendre comment 48 V devient une sinusoïde 230 V | [Fonctionnement expliqué](docs/01-fonctionnement.md) |
| Identifier les bornes et les deux cartes de commande | [Connectique et compatibilité](docs/02-connectique.md) |
| Comprendre et régler la fréquence du DC-DC | [Résonance et contrôleur DC-DC](docs/03-reglage-dcdc.md) |
| Régler 50/60 Hz, temps mort et démarrage EGS005Q | [Configuration de l'onduleur](docs/04-reglage-onduleur.md) |
| Préparer les achats, PCB et l'assemblage | [Fabrication](docs/05-fabrication.md) |
| Préparer les mesures et les premiers essais | [Mise en service et dépannage](docs/06-mise-en-service.md) |
| Voir les anomalies, preuves et données manquantes | [Audit technique](docs/07-audit-technique.md) |
| Retrouver les notices des fabricants | [Sources et versions](docs/08-sources.md) |

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

## Licence et participation

Licence matériel : **[CERN-OHL-S-2.0](LICENSE)**. Les notices des fabricants sont liées depuis la documentation et ne sont pas redistribuées comme des fichiers du projet.

[Contribuer](CONTRIBUTING.md) : corrections documentées, relevés de banc, référence du noyau et retours de fabrication sont utiles pour rendre ce projet reproductible.

[cirbatt.com](https://cirbatt.com) · contact@cirbatt.com
