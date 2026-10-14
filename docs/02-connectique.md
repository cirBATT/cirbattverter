# Connectique et compatibilité des contrôleurs

[Sommaire](README.md) · [Réglage DC-DC](03-reglage-dcdc.md) · [Réglage onduleur](04-reglage-onduleur.md)

Les tableaux ci-dessous décrivent la révision publiée. Les nets proviennent de la netliste KiCad et ont été comparés aux pads du PCB. Le CSV [connector-nets.csv](reports/connector-nets.csv) conserve les noms exacts.

**Ne pas enficher directement l'EGS005Q dans J5 sur cette révision.** Le conflit de la broche 17 doit être résolu par une correction étudiée de la carte ou un adaptateur documenté, puis vérifié hors tension. Un réglage logiciel ne corrige pas ce câblage.

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
| 5 | VFB | Retour de limitation du bus |
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
| 13 | GND2 | NC | Pad de dégagement relié à la masse sur la carte |
| 14 | OUT_LS2_P | 2LO | Commande basse bras 2 |
| 15 | ISENSE3_P | IFB2P | Retour courant bras 2 |
| 16 | ISENSE1_N | IFB2N | Retour commun aux mesures |
| **17** | **+15V** | **GND** | **Conflit : risque de court-circuit de l'alimentation** |
| 18 | GND2 | NC | Pad de dégagement relié à la masse sur la carte |
| 19 | OUT_HS1_P | 1HO | Commande haute bras 1 |
| 20 | DESAT1_P | SDH1 | Retour shunt R58 |
| 21 | OUT_HS1_N | VS1 | Nœud de commutation bras 1 |
| 22 | GND2 | NC | Pad de dégagement relié à la masse sur la carte |
| 23 | OUT_LS1_P | 1LO | Commande basse bras 1 |
| 24 | ISENSE1_P | IFB1P | Retour courant bras 1 |
| 25 | ISENSE1_N | IFB1N | Retour commun aux mesures |
| **26** | **Non connectée** | **IFBCOM** | **Protection à raccorder et valider** |
| 27 | GND2 | GND | Cohérent |
| 28 | OUT_P | OUTL | Retour tension AC |
| 29 | OUT_N | OUTN | Retour tension AC |

Source du module : [notice officielle EGS005Q, pp. 3 et 5, et schéma fourni du 26 juillet 2024](08-sources.md#egs005q). Le schéma 2024 confirme explicitement **P3-17 = GND2**. Cette numérotation est celle du connecteur à 29 broches, pas celle du circuit intégré U1 à 70 broches. Le pas EGS005Q est 1,27 mm, comme J5. Vérifier aussi la hauteur, la face d'assemblage et le sens d'insertion.

Les broches 13/18/22 sont réservées sur le module, et participent à son dégagement. Leur utilisation comme masse sur la carte doit être revue en tenant compte du cuivre et de l'isolation, même sans broche fonctionnelle correspondante.

## Vérification d'une rotation de 180°

J5 utilise une empreinte standard à **29 pads en une seule rangée**, au pas de 1,27 mm. Dans le PCB, la rangée est orientée à 90° : pad 1 à `(219,19 ; 196,10)` mm et pad 29 à `(254,75 ; 196,10)` mm. Le pad 17 est à `(239,51 ; 196,10)` mm. Les numéros sont ceux des pads, pas un comptage effectué depuis une photo.

Si les mêmes 29 contacts sont alignés après inversion complète de la rangée, la correspondance est : **broche module n → pad PCB 30 − n**. La broche 17 devient donc J5-13, pas J5-1.

| Broche EGS005Q V1.0 | Fonction | Alignement 1 → 1 | Alignement inversé 1 → 29 |
| --- | --- | --- | --- |
| 1 | Mesure +400V | J5-1 : +400V | J5-29 : OUT_N |
| 7 | Alimentation +5V | J5-7 : +5V | J5-23 : OUT_LS1_P, commande PWM |
| 8 | Alimentation +15V | J5-8 : rail nommé +15V | J5-22 : GND2 |
| 17 | GND | J5-17 : rail nommé +15V | J5-13 : GND2 |
| 28 | Mesure OUTL | J5-28 : OUT_P | J5-2 : non connecté |
| 29 | Mesure OUTN | J5-29 : OUT_N | J5-1 : +400V |

L'inversion raccorde bien la broche 17 à une masse, mais rend les alimentations et retours incompatibles. **Aucune de ces deux orientations ne fournit un raccordement complet correct pour la notice EGS005Q V1.0.** Tourner ou regarder la carte depuis l'autre face peut changer l'ordre visuel ; cela ne change pas les fonctions électriques des contacts. Si le retournement est effectué autour de l’axe longitudinal du connecteur sans inverser l’ordre de ses contacts, la correspondance reste 1 → 1 et le conflit de J5-17 demeure. Le schéma EGS005Q fourni du 26 juillet 2024 confirme ce brochage. Vérifier une éventuelle autre révision du module sur sa propre notice.

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
