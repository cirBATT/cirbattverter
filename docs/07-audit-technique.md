# Audit historique des sources du 14 octobre 2026

**Document historique.** Pour le ZIP corrigé reçu le 16 octobre, consulter la [revue actuelle](10-revue-corrections-2026-10-16.md). Les constats et décomptes ci-dessous décrivent la révision initiale.

[Sommaire](README.md) · [Rapports bruts](reports/README.md)

Analyse du **14 octobre 2026**, à partir du commit matériel `57c311172280aa886eefcb7f3e61cd4b875de159`, avec KiCad CLI **10.0.5**. Les empreintes SHA-256 des circuits et exports analysés sont conservées dans [source-manifest.csv](reports/2026-10-14/source-manifest.csv).

**Conclusion : cette révision ne dispose pas encore d'un dossier permettant à un utilisateur de fabriquer et mettre en service seul un produit qualifié.** La documentation a été développée ; les anomalies matérielles ci-dessous doivent être levées et les informations manquantes publiées.

## Périmètre et méthode

- Lecture du README, des contributions, du schéma principal, des deux PCB, des deux projets `.kicad_pro`, du fichier de règles et des dépendances de bibliothèques.
- Extraction de la netliste avec KiCad, comparaison des connexions schéma/PCB et inventaire des composants.
- ERC du schéma ; DRC des deux PCB ; contrôle de parité sur la carte principale.
- Nouvelle exécution DRC sur une **copie isolée**, en réactivant `clearance`, `hole_clearance` et `annular_width`. Les règles du projet source n'ont pas été modifiées.
- Contrôle de la composition des archives Gerber, de leurs métadonnées et de la couverture BOM/CPL.
- Lecture des dépendances STEP et des vues de schéma/implantation ; contrôle visuel des notices officielles des modules.

Pas de carte physique, mesure, simulation de puissance, extraction électromagnétique ou essai d'isolation. Le modèle STEP n'a pas fait l'objet d'une qualification mécanique/thermique. Les exports historiques n'ont pas été comparés à une nouvelle fabrication complète après remplissage des zones. Les résultats documentent des constats et des points à valider, pas un rendement ou une puissance démontrée.

## Résultats KiCad

Les bibliothèques personnalisées manquantes ont été récupérées depuis les objets intégrés aux sources, sans changer les schémas ni le cuivre. Les rapports « original » précèdent cette récupération, les rapports « current » la suivent.

| Contrôle | Erreurs | Avertissements | Complément |
| --- | --- | --- | --- |
| ERC original | 7 | 32 | 39 signalements |
| ERC après récupération des bibliothèques | 7 | 13 | 20 signalements ; plus de dépendance personnalisée introuvable dans ce contrôle |
| DRC principal, règles originales | 0 | 179 | Avant récupération ; contrôles d'espacement désactivés |
| DRC principal, mêmes règles après récupération | 0 | 157 | 26 avertissements de parité supplémentaires |
| DRC principal sur copie, 3 contrôles réactivés | **28** | 157 | **185** signalements + 26 de parité |
| DRC planaire | **40** | 10 | 50 signalements |

Les 28 erreurs du contrôle renforcé principal comprennent **16 anneaux de perçage insuffisants**, **9 signalements d'espacement** et **3 contacts entre nets**. Le planaire comporte **36 erreurs de distance cuivre/contour** et **4 ponts de masque**. Inspecter chaque occurrence : certains seuils ou géométries peuvent avoir une explication de fabrication, qui reste à documenter.

Le premier DRC principal affichait zéro erreur parce que plusieurs contrôles étaient ignorés. Zéro connexion manquante ne signifie pas absence de court-circuit, protection correcte ou isolation suffisante. Cette réserve est particulièrement importante pour le planaire, dont les pistes n'ont pas de nets.

Les 26 problèmes de parité sont : 8 duplications des références `REF**`, 9 empreintes mécaniques supplémentaires, 8 pastilles thermiques U4 sans broches correspondantes dans le symbole, et 1 différence de champ LCSC pour FAN1. **J4 et J5 ont les mêmes nets dans le schéma et le PCB** ; leur défaut de compatibilité concerne le module externe.

## Constats à traiter avant mise sous tension

| ID | Constat et preuve | Effet possible / action attendue |
| --- | --- | --- |
| A01 | J5-17 = `+15V` dans schéma et PCB ; EGS005Q V1.0, p. 5 : broche 17 = GND | Court-circuit du rail via le module. Corriger l'interface, vérifier toutes les broches et documenter l'adaptation avant insertion. |
| A02 | J5-26 laissée ouverte ; notice : entrée IFBCOM | Une protection ne peut pas être considérée raccordée. Définir son câblage, niveau de repos et comportement avec les shunts. |
| A03 | R35-1 = `/400V` ; C3-1 et J5-1 = `/+400V` ; ERC `isolated_pin_label` sur `400V` | La netliste ne raccorde pas le diviseur TL431 au bus. Revoir le nom et le raccordement, puis valider seuil et dynamique. |
| A04 | DRC renforcé : piste `Net-(U4-FB)` sur In2.Cu en contact avec 3 vias `/+15V`, autour de x=265–266 mm, y=182,5 mm | Retour du régulateur auxiliaire modifié/court-circuité. Inspecter le cuivre, corriger et refaire les contrôles. Les coordonnées sont celles du PCB. |
| A05 | U4 : R48 = 453 kΩ, R49 = 49,9 kΩ ; mêmes valeurs que R44/R45 d'U3 | Cible théorique ≈12,09 V, pas 15 V. Vérifier besoins des composants, marge d'alimentation et nom du rail. Ce calcul ne prouve pas une incompatibilité à 12 V. |
| A06 | Q15-7/11 = ISENSE1_P ; Q15-12 = ISENSE3_P, séparés par les réseaux de shunts | Référence logique/pilote différente de la source. Vérifier l'intention, la tension entre SGND/PGND et les chemins de retour. |
| A07 | GND3 sort sur J7-1 ; liaisons C38–C49 vers GND1/GND2 ; C17/C21 entre domaines | Raccordement au châssis/PE, classe des condensateurs et isolation non qualifiés. Publier une étude et un câblage justifiés. |

### Vérification complète de l'interface EGS005Q

Les trois PDF fournis ont été examinés. Le schéma EGS005Q du 26 juillet 2024 confirme **P3-17 = GND2** ; J5-17 est raccordée à `+15V` dans les deux sources KiCad. Les empreintes des documents sont conservées dans [controller-documents.json](reports/controller-documents.json).

Les **29 pads de J5** et les broches de **17 composants associés** ont été comparés entre netliste du schéma et PCB : leurs nets correspondent. Les commandes HO/LO, les retours VS/SDH, les shunts IFB1/IFB2, les retours OUTL/OUTN, le bus et les canaux de température rejoignent les fonctions attendues du module. Voir la [vérification des circuits](02-connectique.md#vérification-des-circuits-raccordés-à-j5) et le [relevé par broche](reports/egs005q-interface-review.csv).

Cette cohérence n'efface pas **IFBCOM ouverte (A02)** ni la **référence de pilote Q15 (A06)**. FAN/J5-4 n'est pas utilisée : la ventilation actuelle est commandée depuis le DC-DC. Les positions NC 13/18/22 reliées à GND2 demandent une revue du dégagement, et les lois TH2/R40 et TH3/R42 une validation de seuils. Le rail J5-8 calculé à 12,09 V doit être mesuré avec sa marge bootstrap ; ce calcul seul ne démontre pas une incompatibilité avec l'EGS005Q.

### Limitation TL431 prévue

Si le retour était connecté au bus, le diviseur utilise R35+R36 = 750 kΩ en haut et R37 // R38 = `4,7 kΩ // 100 kΩ ≈ 4,489 kΩ` en bas. Avec une référence **nominale de 2,495 V**, le calcul idéal donnerait :

```text
Vseuil ≈ 2,495 × (1 + 750 / 4,489) ≈ 419,35 V
```

Ce résultat est un calcul conditionnel. Le courant de référence, les tolérances, le réseau optocoupleur, l'alimentation +5 V et la dynamique interviennent. Il ne donne pas une consigne du bus validée. Vérifier les tensions de travail des résistances de mesure et la marge par rapport à C3, puis mesurer la limitation après correction. [Notice TL431](https://www.ti.com/lit/ds/symlink/tl431.pdf).

## Dossier de fabrication incomplet

| ID | Constat | Suite attendue |
| --- | --- | --- |
| F01 | `production/inverter/gerber.zip` manque B.Cu, F.Mask et B.Mask ; gbrjob annonce pourtant 4 couches | Regénérer un ensemble complet depuis une révision revue ; ne pas compléter ce ZIP sans reprendre toute la validation. |
| F02 | README original demande 70 µm ; deux PCB et deux gbrjob définissent 35 µm sur toutes les couches | Faire approuver un empilage réel par couche et réévaluer courant, thermique et isolation. |
| F03 | L1 est écrite `22uF`, unité incorrecte ; référence C2976970 associée à 33 µH | Publier valeur corrigée, composant réel et mesure Lr avant consigne de résonance. |
| F04 | Planaire sans schéma/netliste ; pastilles 1/3/6/8/15/16 ; T1 principal numéroté 1–6 | Fournir correspondance, polarités et schéma des enroulements. |
| F05 | Noyau, matériau, spires, Ae, inductances, pertes et entrefer éventuel non documentés | Compléter la conception magnétique et ses essais ; le STEP ne suffit pas. |
| F06 | J4 au pas 1,27 mm, module EGT003 V1.0 documenté au pas 2,54 mm | Identifier le module réel et fournir un adaptateur ou une empreinte approuvée. |
| F07 | T5 associé à une self **de mode commun** PDMCAT18107-202ML ; C57 entre sorties | Mesurer l'inductance différentielle et vérifier la polarité. Ne pas assimiler 2 mH de mode commun à un filtre différentiel de 2 mH. |
| F08 | C3 a une valeur générique ; nombreux semi-conducteurs ont des valeurs `D`, `NPN` ou `Q_NMOS_GDS` | Compléter références fabricant et caractéristiques critiques au-delà des codes d'achat. |

La BOM et la CPL couvrent chacune les mêmes 160 composants que le schéma et le PCB. Cela confirme une couverture des **repères**, pas l'adéquation des produits, l'actualité des achats ni la conformité des rotations. T1 n'a pas de code d'achat ; les modules de commande et les éléments externes ne sont pas une BOM système complète.

## Bibliothèques et modèles 3D

Le `fp-lib-table` initial référençait des bibliothèques absentes et des chemins absolus vers le PC du concepteur. Aucun `sym-lib-table` du projet n'était présent pour les bibliothèques personnalisées. Le schéma et le PCB intégraient néanmoins les objets utilisés, ce qui a permis leur récupération.

La restructuration a ajouté **11 empreintes dans 10 bibliothèques locales** et **3 bibliothèques de symboles**. Les identifiants utilisés par les sources ont été conservés. Le nouveau `fp-lib-table` et le `sym-lib-table` utilisent `${KIPRJMOD}`. Les objets proviennent du PCB/schéma existants, sans modification de routage ou de brochage.

Réserves :

- Les diodes personnalisées intégrées sous `Device:D` diffèrent de la bibliothèque standard ; les 10 avertissements correspondants demeurent. Ne pas les remplacer automatiquement par la définition standard sans comparer les pins.
- L'empreinte LM5013 récupérée contient des pads thermiques numérotés 10–17. Le symbole possède 1–9 ; leur net varie entre U3 et U4. Le snapshot ne résout pas cette représentation.
- Les chemins `${KIPRJMOD}/step/…` dans le PCB historique ne correspondent pas au répertoire publié `3d/`. Un modèle `CID12N65.stp` sous `libs/…` manque. Des variables EASYEDA2KICAD et KICAD8_3DMODEL_DIR peuvent aussi être absentes.
- Les copies de bibliothèque ont certains chemins `step/` ramenés vers `3d/` quand le fichier existe, mais cela ne modifie pas les modèles déjà intégrés au PCB historique.

Ces chemins 3D concernent la visualisation. Ne pas confondre leur réparation avec une vérification du boîtier, de l'isolation mécanique ou du montage thermique.

## Données à publier pour permettre une reproduction indépendante

- Modèle et révision du contrôleur DC-DC, avec câblage/adaptateur, diviseur batterie et temps mort mesuré.
- Révision EGS005Q, interface J5 corrigée, choix HM/DT/FS/SST et fichier de paramètres.
- Noyau et assemblage planaire complets ; mesures de rapport, phase, Lm, fuite, pertes et isolation.
- Valeurs L1/C2 et fréquence DC-DC **mesurées**, avec limites et captures à vide/en charge/à chaud.
- C3 et filtre de sortie dimensionnés ; preuve de qualité de la sinusoïde et de stabilité.
- Plage batterie, protections, séquence de démarrage/arrêt et décharge du bus.
- Refroidissement, enveloppe, schéma de raccordement terre/châssis et dossier d'isolation.
- Rapports de puissance, rendement, température et protections ; critères d'acceptation explicites.
- Gerbers/BOM/CPL approuvés et cohérents avec le même commit et empilage.

Une fois ces informations disponibles et les défauts corrigés, les guides de fabrication et de mise en service peuvent devenir une procédure de reproduction avec des valeurs concrètes. À ce stade, laisser les inconnues visibles évite qu'une valeur d'exemple devienne une consigne dangereuse.

## Échanger sur une révision

Les corrections et preuves de validation se suivent dans les issues du projet. Pour les besoins d'intégration d'une batterie ou de partenariat autour de la marque, utiliser le [contact cirBATT](https://cirbatt.com/contact).
