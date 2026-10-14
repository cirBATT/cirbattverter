# Préparer la fabrication et l'assemblage

[Sommaire](README.md) · [Audit à lire avant commande](07-audit-technique.md) · [Mise en service](06-mise-en-service.md)

**Les exports actuels ne forment pas un dossier de fabrication validé.** Cette page donne l'ordre des opérations et les informations à compléter. Ne pas lancer une commande en recopiant les seuls fichiers historiques.

## 1. Choisir une révision corrigée

Identifier le commit utilisé, résoudre les conflits J5/EGS005Q et `400V`, inspecter les contacts U4-FB/+15V, puis exécuter ERC et DRC avec les vérifications d'espacement actives. Les justifications d'exclusion doivent être documentées individuellement ; ne pas neutraliser une famille entière de contrôles pour obtenir un rapport vide.

Vérifier la correspondance schéma/PCB et les empreintes des composants critiques. Les bibliothèques récupérées dans `hardware/inverter/libraries/` permettent de retrouver les objets intégrés au projet ; elles ne prouvent pas qu'un brochage est conforme au composant acheté.

Les fichiers `docs/assets/` sont des vues de lecture. Ils ne sont pas des fichiers de fabrication.

## 2. Définir la commande PCB

| Paramètre | Carte principale | Transformateur planaire |
| --- | --- | --- |
| Couches cuivre | 4 | 8 |
| Dimensions des exports historiques | Environ 190,37 × 103,19 mm | Environ 46,33 × 57,10 mm |
| Épaisseur déclarée | 1,6 mm | 1,6 mm |
| Cuivre dans PCB et gbrjob | 35 µm sur chaque couche | 35 µm sur chaque couche |
| Ancienne demande README | 70 µm | 70 µm |
| Empilage à approuver | Cuivre + prépregs + cœur + isolation | Cuivre + sept diélectriques + isolation inter-enroulements |
| Points non définis complètement | Finition, capacités du fabricant, distances HV, thermique | Isolation, matériau PCB, noyau, rapport de spires, pertes |

35 µm correspond environ à 1 oz/ft² ; 70 µm à 2 oz/ft². Une augmentation de cuivre modifie aussi l'empilage et les possibilités de fabrication, particulièrement sur huit couches. **Le concepteur doit confirmer l'épaisseur par couche et obtenir l'empilage du fabricant.** Ne pas imposer silencieusement 70 µm tout en envoyant des métadonnées de 35 µm.

Les fichiers déclarent 1,6 mm mais il faut vérifier l'épaisseur finale de l'empilage proposé, ses tolérances et son effet sur le montage du noyau. Les paramètres KiCad par défaut ne remplacent pas une étude d'isolation.

## 3. Regénérer les Gerbers

L'archive historique `production/inverter/gerber.zip` contient trois couches cuivre : F.Cu, In1.Cu et In2.Cu. Elle ne contient **ni B.Cu, ni F.Mask, ni B.Mask**. Elle ne peut pas définir la carte quatre couches attendue.

Après corrections et approbation du stackup :

1. Dans l'éditeur PCB, recalculer les zones, vérifier le contour, les découpes et le DRC.
2. Exporter **toutes** les couches cuivre : F.Cu, In1.Cu, In2.Cu, B.Cu pour la carte principale ; F.Cu, In1 à In6.Cu, B.Cu pour le planaire.
3. Exporter F.Mask, B.Mask, Edge.Cuts et les sérigraphies utiles. Les couches de pâte servent à l'assemblage/stencil ; elles ne remplacent pas les masques de soudure.
4. Exporter les perçages métallisés et non métallisés avec des unités cohérentes, ainsi que le fichier `.gbrjob`.
5. Ouvrir le jeu complet dans Gerber Viewer. Contrôler chaque couche, les perçages, la numérotation, les découpes du noyau et la superposition des trous.
6. Comparer les caractéristiques de commande au `.gbrjob`. Publier les fichiers comme un ensemble associé au même commit et au même empilage.

Les fichiers libres et l'archive du planaire publiés sont identiques octet pour octet et comportent huit couches cuivre et les masques. Leur complétude ne résout pas les erreurs DRC, la caractérisation magnétique ou l'isolation.

## 4. Nomenclature et placement

Les deux fichiers JLCPCB contiennent respectivement **160 références uniques**, couvrant les 160 composants électriques du PCB. Les neuf empreintes mécaniques ne sont pas des composants à acheter. Le comptage annoncé autrefois à environ 199 correspondait aux unités du schéma, dont les symboles d'alimentation.

| Fichier | Usage et limite |
| --- | --- |
| `production/inverter/*_JLCPCB_BOM.xlsx` | 61 lignes de composants groupés ; références et codes d'achat historiques |
| `production/inverter/*_CPL_JLCPCB.xlsx` | 160 positions ; comporte aussi des pièces traversantes à traiter selon le procédé d'assemblage |
| [Inventaire CSV du schéma](reports/components-from-schematic.csv) | 160 composants avec leurs champs publiés ; aide à rechercher les références |

Un code LCSC identifie un produit chez un distributeur. Il ne garantit ni disponibilité actuelle, ni substitut compatible, ni qualification électrique. Vérifier la fiche fabricant, la polarité et le boîtier avant validation des achats.

Points particuliers :

- **L1 :** résoudre `22uF` / SMMS1770-330M / 33 µH et vérifier le courant de saturation, l'échauffement et les pertes HF.
- **C3 :** publier capacité, tension, courant d'ondulation, température et dimensions ; la valeur générique `C_Polarized` est insuffisante.
- **C2, C50, C57 :** définir tenue en tension, technologie et courant admissible ; une capacité seule ne suffit pas.
- **C17/C21 et C38–C49 :** vérifier la classe de sécurité requise pour les connexions entre domaines/châssis, le courant de fuite et le dossier d'isolation. Ne pas supposer qu'un MLCC de valeur identique convient.
- **Q1 à Q9 :** documenter la référence exacte des huit MOSFET peu nommés dans le schéma, les pertes et le montage thermique.
- **Q14–Q17 :** conserver la fonction de pilote intégré, vérifier brochage, références SGND/PGND, MSL et refroidissement.
- **D17 / ventilateur :** revoir la diode, Q13 et le courant du ventilateur choisi ; ne pas supposer une diode de petit signal adaptée à toute charge.
- **FAN1 :** le code d'achat du schéma/BOM diffère du champ PCB historique. Vérifier l'empreinte par rapport au connecteur livré.
- **T1 :** composant spécifique, sans référence d'achat dans la BOM. Il faut un dossier magnétique complet.

La CPL doit être contrôlée dans le visualiseur de l'assembleur : origine, unité, face, rotation, pin 1 et polarité. Valider en particulier les pièces de face arrière. Ne pas corriger toutes les rotations avec un décalage global supposé.

## 5. Pièces externes manquantes de la BOM carte

| Ensemble | Informations à fournir avant achat |
| --- | --- |
| Module DC-DC | Modèle/révision, variante batterie, pas/adaptateur J4, notice |
| Module EGS005Q | Révision, orientation, câblage corrigé J5, fichier de configuration |
| Noyau T1 | Fabricant, référence, matériau, dimensions, Ae, entrefer éventuel |
| Montage T1 | Correspondance des pastilles, polarités, fixation, isolants, assemblage |
| Batterie et BMS | Chimie, série/parallèle, tensions, courant permanent/de défaut, protections |
| Protection DC | Fusible DC, sectionnement, précharge, câble et connexions dimensionnés |
| Thermique | Dissipateur, interface thermique/électrique, ventilateur et commande |
| Enveloppe | Matériau, protection contre les contacts, tenue mécanique, passages de câbles |
| Sortie AC | Connectique, câblage, protection et schéma de mise à la terre à étudier |
| Décharge du bus | Dispositif dimensionné, temps et vérification d'absence de tension |

Le modèle STEP d'assemblage facilite les vérifications d'encombrement. Il ne fournit pas automatiquement ces références ni les spécifications d'isolation et de refroidissement.

## 6. Ordre d'assemblage conseillé après validation

1. Réceptionner les PCB : dimensions, empilage, continuité, courts-circuits, qualité des perçages et découpes.
2. Contrôler les composants livrés contre une BOM approuvée. Conserver les fiches et les substitutions.
3. Assembler les CMS avec un procédé adapté aux boîtiers et à leur sensibilité à l'humidité. Inspecter les pads thermiques et les joints cachés.
4. Monter les éléments traversants, le transformateur, les connexions et les supports des modules selon un plan d'assemblage validé.
5. Installer le refroidissement et les isolants ; contrôler que les fixations ne court-circuitent pas des domaines.
6. Vérifier hors tension la polarité des composants, le câblage point par point et l'absence de courts-circuits.
7. Tester les auxiliaires et les modules seuls avant toute conversion de puissance, selon le [guide de mise en service](06-mise-en-service.md).

Conserver une fiche avec fabricant PCB, empilage réel, photos des deux faces, référence des modules, noyau, substitutions et commit. Ces données permettent à une autre personne de reproduire le même matériel.
