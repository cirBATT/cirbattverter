# Connectique et compatibilité des contrôleurs

[Sommaire](README.md) · [Réglage DC-DC](03-reglage-dcdc.md) · [Réglage onduleur](04-reglage-onduleur.md)

Les tableaux ci-dessous décrivent la révision publiée. Les nets proviennent de la netliste KiCad et ont été comparés aux pads du PCB. Le CSV [connector-nets.csv](reports/connector-nets.csv) conserve les noms exacts.

**Interface en cours de validation.** Les anciennes pistes +15V de J5-17 sont supprimées. Les références du pilote Q15 restent à revoir avant mise sous tension ; voir la [revue du 19 octobre](11-revue-corrections-2026-10-19.md).

## Bornes utilisateur

| Repère / borne | Net | Fonction / point à vérifier |
| --- | --- | --- |
| J1, borne 1 | BAT+ | Entrée positive batterie, avec protections DC externes adaptées |
| J2, borne 1 | GND1 | Retour négatif batterie |
| J7, borne 1 | GND3 | Domaine relié capacitivement ; fonction de protection et raccordement au châssis à définir |
| J7, borne 2 | OUT_N | Un des deux fils AC ; le nom N ne définit pas un neutre relié à la terre |
| J7, borne 3 | OUT_P | Autre fil AC ; objectif 230 V entre bornes 2 et 3 |
| FAN1, borne 1 | Collecteur de Q13 | Retour commuté du ventilateur |
| FAN1, borne 2 | +12V | Positif du ventilateur ; référence et courant admis à définir |

Identifier les bornes avec la numérotation des pads dans KiCad. Ne pas déduire leur ordre d'une photo prise de l'autre face. Le modèle [Cirbatt.step](../hardware/mechanical/Cirbatt.step) aide à l'encombrement, mais ne précise pas un schéma de câblage de sécurité.

## J4 : commande du DC-DC

Interface logique conforme à l'ordre des broches EGT003 documenté par EGmicro ; **référence exacte du module et adaptation mécanique à confirmer**.

| J4 | Net KiCad | Équivalent module |
| --- | --- | --- |
| 1 | TEMP | Temp |
| 2 | BEEP | Beep |
| 3 | BAT | Détection batterie |
| 4 | FAN | Commande ventilateur |
| 5 | Net-(J4-Pin_5) | Retour VFB du module ; nom de net supprimé, raccordement U1/C7/R32 conservé |
| 6 | GND1 | GND |
| 7 | +12V | Alimentation module |
| 8 | LO1 | LO1 |
| 9 | IN_DRV1_N | VS1 |
| 10 | IN_DRV1_P | HO1 |
| 11 | LO2 | LO2 |
| 12 | IN_DRV2_N | VS2 |
| 13 | IN_DRV2_P | HO2 |
| 14 | IFB | Retour courant |

J4 est dessiné au pas **1,27 mm**. La notice EGT003 V1.0 indique **2,54 mm** : la compatibilité électrique de l'ordre des broches ne constitue pas une compatibilité d'enfichage. Vérifier le module acheté, l'orientation, le support et l'éventuel adaptateur. [Notice EGT003, pp. 3 et 7](08-sources.md#egt003).

Sur la carte principale, R39 et R50, deux résistances de 12 kΩ, se trouvent **en série** entre BAT+ et J4-3. Le diviseur bas de détection appartient au module externe. Il faut calculer le seuil avec le réseau complet, pas seulement appliquer les valeurs de la notice EGT003.

## J5 : comparaison avec EGS005Q V1.0

| J5 | Net sur carte principale | Broche du module officiel | Résultat |
| --- | --- | --- | --- |
| 1 | +400V | +400V | Mesure directe du bus |
| 2 | Non connectée | NC | Cohérent |
| 3 | GND2 | GND | Cohérent |
| 4 | Non connectée | FAN | Ventilation EGS005Q non câblée |
| 5 | TFB1 | TFB1 | Vérifier étalonnage TH2/R40 |
| 6 | TFB2 | TFB2 | Vérifier étalonnage TH3/R42 |
| 7 | +5V | +5V | Alimentation logique |
| 8 | +15V | +15V | Nom de rail ; calcul U4 ≈ 12,09 V |
| 9 | Non connectée | NC | Cohérent |
| 10 | OUT_HS2_P | 2HO | Commande haute bras 2 |
| 11 | DESAT2_P | SDH2 | Retour shunt R57 |
| 12 | OUT_HS2_N | VS2 | Nœud de commutation bras 2 |
| 13 | Non connectée | NC | Cohérent ; dégagement à vérifier |
| 14 | OUT_LS2_P | 2LO | Commande basse bras 2 |
| 15 | ISENSE3_P | IFB2P | Mesure du bras 2 sur R59 = 10 mΩ |
| 16 | ISENSE1_N | IFB2N | Retour commun aux mesures |
| 17 | Non connectée | GND | Anciens contacts +15V supprimés ; GND2 du module présente via ses autres masses |
| 18 | GND2 | NC | Pad de dégagement relié à la masse sur la carte |
| 19 | OUT_HS1_P | 1HO | Commande haute bras 1 |
| 20 | DESAT1_P | SDH1 | Retour shunt R58 |
| 21 | OUT_HS1_N | VS1 | Nœud de commutation bras 1 |
| 22 | Non connectée | NC | Cohérent ; dégagement à vérifier |
| 23 | OUT_LS1_P | 1LO | Commande basse bras 1 |
| 24 | ISENSE1_P | IFB1P | Mesure du bras 1 sur R60 = 10 mΩ |
| 25 | ISENSE1_N | IFB1N | Retour commun aux mesures |
| **26** | **ISENSE1_N** | **IFBCOM** | **Raccordée au-dessus de R52 ; protection à valider** |
| 27 | GND2 | GND | Cohérent |
| 28 | OUT_P | OUTL | Retour tension AC |
| 29 | OUT_N | OUTN | Retour tension AC |

Source du module : [notice officielle EGS005Q, pp. 3 et 5, et schéma fourni du 26 juillet 2024](08-sources.md#egs005q). Le schéma 2024 confirme explicitement **P3-17 = GND2**. Cette numérotation est celle du connecteur à 29 broches, pas celle du circuit intégré U1 à 70 broches. Le pas EGS005Q est 1,27 mm, comme J5. Vérifier aussi la hauteur, la face d'assemblage et le sens d'insertion.

Les positions 13/18/22 sont NC sur le module. Dans la révision du ZIP du 17 octobre, 13 et 22 sont ouvertes, tandis que 18 reste sur GND2. Vérifier dégagement et isolation. La position 17 est une masse fonctionnelle du module.

## Vérification des circuits raccordés à J5

Les 29 nets J5 et toutes les broches des 160 composants électriques ont été comparés entre netliste KiCad et PCB : aucun écart de net n'a été retrouvé. Le [CSV par broche](reports/egs005q-interface-review.csv) décrit la révision actuelle. Ce contrôle des noms de nets ne remplace pas l’examen du circuit : la différence entre source et références du pilote Q15 existe dans les deux fichiers.

| Groupe | Raccordement courant | Conclusion |
| --- | --- | --- |
| Bras 2 | 10 → PWM Q14 ; 14 → PWM Q15 ; 11 → source Q14/R57-1 ; 12 → R57-2/drain Q15 | HO/LO/SDH/VS affectés au bon bras |
| Bras 1 | 19 → PWM Q16 ; 23 → PWM Q17 ; 20 → source Q16/R58-1 ; 21 → R58-2/drain Q17 | HO/LO/SDH/VS affectés au bon bras |
| Courant IFB1/IFB2 | 15 → ISENSE3_P/R59 ; 24 → ISENSE1_P/R60 ; 16/25 → ISENSE1_N | Deux shunts distincts de 10 mΩ ; gains et protection à valider |
| IFBCOM | 26 → ISENSE1_N ; R52 = 10 mΩ vers GND2 | Raccordement ajouté ; seuil et fonctionnement à vérifier |
| Q15 / Q17 | Q15-S sur ISENSE3_P ; Q15-SGND/PGND et Q17-S/SGND/PGND sur ISENSE1_P | Référence Q15 différente de sa source : point ouvert |
| Tension AC / HM | 28 → OUT_P après T5 depuis bras 2 ; 29 → OUT_N après T5 depuis bras 1 | Affectation cohérente avec HM=0 ; stabilité à valider |
| Mesure bus | 1 → +400V/C3 | Raccordement du module présent ; R35 rejoint désormais ce même bus, régulation à valider |
| Températures | 5 → TH2/R40 ; 6 → TH3/R42 | Lois différentes à étalonner |
| Alimentations | 3/27 → GND2 ; 7 → +5V ; 8 → rail nommé +15V | Tensions réelles et marge bootstrap à vérifier |

J5-4/FAN reste ouverte ; FAN1 est commandé par J4/Q13 dans le domaine batterie. La commande thermique de l'EGS005Q ne commande donc pas directement ce ventilateur. Ne pas réunir GND1 et GND2 pour ajouter cette fonction.

J5-8 conserve un rail calculé idéalement à environ 12,09 V. La notice permet un essai de module à 12–15 V ; ce calcul seul ne prouve pas une incompatibilité. Mesurer les marges et le comportement des pilotes en conditions réelles.

Voir les [preuves et actions restantes](11-revue-corrections-2026-10-19.md). La référence de Q15 et les protections restent à valider ; l’interface n’est pas qualifiée par cette revue.

## Port de configuration

Le port UART est situé **sur l'EGS005Q**, pas sur J4 ni sur les 29 broches J5. Identifier TXD0, RXD0 et GND dans sa notice. La masse est celle du secondaire haute tension, GND2. Un adaptateur USB-UART ordinaire créerait une liaison entre ce domaine et le PC.

Configurer de préférence le module retiré du circuit de puissance, sur un banc basse tension adapté. Pour une communication avec la puissance alimentée, utiliser une interface possédant l'isolation et les tensions assignées appropriées. Vérifier le niveau logique supporté par l'adaptateur avant toute connexion.

## Transformateur : interface encore à documenter

| Broche du symbole T1 | Net dans la carte principale |
| --- | --- |
| 1 | IN_DRV2_N |
| 2 | IN_DRV1_N |
| 3 | Entrée L1 |
| 4 | Entrée redresseur de puissance |
| 5 | Entrée redresseur auxiliaire D25/D27 |
| 6 | Entrée redresseur auxiliaire D26/D28 |

Cette table **ne donne pas** la correspondance avec les pastilles du PCB planaire. Il reste à publier un dessin de raccordement, le rapport de spires, la polarité des enroulements et les essais magnétiques.

## Définir le pack raccordé à J1/J2

La connectique ne suffit pas à établir la compatibilité d'une batterie. Réunir les données du pack et de son BMS selon le [guide batterie](09-batteries-seconde-vie.md). Pour un projet d'intégration, [contacter cirBATT](https://cirbatt.com/contact) avec les plages de tension et de courant attendues.
