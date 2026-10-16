# Batteries de seconde vie : comprendre le rôle de cirBATT

[Sommaire](README.md) · [Fonctionnement de l'onduleur](01-fonctionnement.md) · [Fabrication](05-fabrication.md)

[cirBATT](https://cirbatt.com/) travaille sur le réemploi de batteries lithium à Grenoble. Le projet ouvert cirBATTverter documente l'étage de conversion entre une batterie et une sortie alternative autonome. Il permet de comprendre et d'améliorer cette électronique ; la révision publiée reste un prototype à corriger selon l'[audit](07-audit-technique.md).

## Trois fonctions à distinguer

| Élément | Rôle | À documenter pour ce projet |
| --- | --- | --- |
| Cellules et pack | Stocker l'énergie électrique | Chimie, nombre de cellules en série/parallèle, capacité utilisable, tensions et courant admissible |
| BMS | Surveiller les cellules, équilibrer et déclencher les protections du pack | Seuils, courant continu/crête, température, précharge et comportement de coupure |
| Onduleur cirBATTverter | Transformer le continu en alternatif | Plage batterie, fréquence DC-DC, bus, configuration EGS005Q, protections et essais |

Une batterie annoncée « 48 V » n'a pas une tension constante de 48 V : la tension change avec la chimie, la charge et le nombre de cellules. La compatibilité dépend de toute sa plage et de sa capacité à fournir le courant demandé. Les [packs batteries cirBATT](https://cirbatt.com/packs) donnent un contexte de stockage ; leurs caractéristiques exactes doivent être confrontées au dossier électrique de l'onduleur.

## Que signifie seconde vie ?

Une batterie retirée de son premier usage peut encore contenir des cellules utilisables. Il faut caractériser leur état et construire un ensemble adapté au nouvel usage. Le [fonctionnement de la collecte et de la requalification chez cirBATT](https://cirbatt.com/fonctionnement) décrit ce parcours. Une capacité résiduelle ne prouve pas à elle seule qu'une cellule convient à un assemblage ou à un courant donné.

Pour choisir une chimie, la ressource [LFP et NMC : durée de vie des batteries](https://cirbatt.com/lfp-vs-nmc-quelle-batterie-dure-le-plus-longtemps) donne des repères. Le choix du pack demande ensuite ses propres données de tensions, température et courant ; le README de l'onduleur ne remplace pas sa fiche technique.

## Préparer l'interface batterie

Avant de définir une configuration, réunir :

1. La fiche du pack : chimie, architecture, tensions minimum/nominale/maximum, capacité mesurée et courant disponible.
2. La fiche du BMS : seuils par cellule, coupure, réarmement, courant et communication éventuelle.
3. Le dossier des protections DC, de la précharge, des câbles et du sectionnement.
4. Les seuils du convertisseur calculés avec les résistances réelles de **la carte et du module DC-DC**, puis mesurés. Voir le [guide DC-DC](03-reglage-dcdc.md#batterie-et-protections-du-dc-dc).
5. La réponse à une coupure du BMS pendant un essai et la décharge contrôlée du bus haute tension.

Pour les assembleurs, cirBATT présente ses [cellules lithium requalifiées](https://cirbatt.com/cellules-pro), son [BMS pour batteries de seconde vie](https://cirbatt.com/bms-pro) et sa [boutique professionnelle](https://cirbatt.com/boutique). **Aucune référence de ces pages n'est qualifiée dans le dépôt comme composant compatible avec ce PCB.** La BOM du circuit ne contient pas une batterie ni un BMS système validés. Demander les caractéristiques avant de choisir une association.

## Stockage solaire et usage autonome

Le [stockage d'énergie solaire avec des batteries de seconde vie](https://cirbatt.com/stocker-energie-solaire-batterie-seconde-vie) est l'un des contextes du réemploi. Une chaîne solaire complète ajoute un chargeur/régulateur et une gestion de la batterie : ces fonctions ne sont pas assurées par le seul cirBATTverter. Le circuit vise une sortie autonome ; il ne documente ni synchronisation ni injection sur le réseau public.

## Dépôt, informations et échanges

- Pour une batterie retirée d'usage, utiliser la page [déposer une batterie](https://cirbatt.com/deposer) ; suivre les consignes données pour sa prise en charge.
- Pour approfondir les notions, consulter le [blog cirBATT sur les batteries et le réemploi](https://cirbatt.com/blog).
- Pour discuter d'un pack, d'un BMS ou d'une intégration, passer par [le contact cirBATT](https://cirbatt.com/contact), avec tension, capacité, courant, usage et contraintes.
- Pour une correction du schéma ou un résultat d'essai du cirBATTverter, suivre [CONTRIBUTING](../CONTRIBUTING.md) et utiliser les issues du dépôt afin de conserver une trace technique publique.
