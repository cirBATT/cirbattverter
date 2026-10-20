# Revue des corrections du 20 octobre 2026

[Sommaire](README.md) · [Connectique actuelle](02-connectique.md) · [Revue précédente](11-revue-corrections-2026-10-19.md)

**La référence de Q15 est corrigée dans les sources reçues.** Source, SGND, PGND et retours de C52/C53 rejoignent maintenant ISENSE3_P. Les deux shunts R59/R60 restent séparés. Les anciens points J5-17 et R35 restent corrigés. **La révision n'est cependant pas approuvée pour fabrication ou mise sous tension : les contrôles renforcés conservent 33 erreurs DRC et l'ERC 7 erreurs.** Les points non résolus restent ouverts.

**English summary:** Q15 source, SGND/PGND and C52/C53 returns now share ISENSE3_P, while the two 10 mΩ leg shunts remain separate. Supplied Gerbers and drill files match fresh exports from the supplied PCB after explicitly documented header normalization. Strengthened DRC still reports 33 errors and ERC 7 errors/11 warnings. No bench qualification or manufacturing approval is claimed.

## Révision examinée

ZIP reçu le **20 octobre 2026**, schéma et PCB enregistrés le même jour. SHA-256 de l'archive : `955298936ce66b51dce858ddac3a5095957948128a465ba8e9f6908ac21ac108`. Le [manifeste d'import](reports/2026-10-20/input-manifest.json) conserve les empreintes brutes des 22 fichiers retenus et la comparaison à la publication précédente `c00bd3aedd5058c9eb56942cf3f57c292a063a8b`.

Le schéma, le PCB et le Gerber ZIP sont modifiés. Les réglages du projet KiCad sont identiques à la révision précédente, malgré une nouvelle date de sauvegarde. Les autres fichiers, notamment BOM/CPL, modèles et PCB planaire, sont conservés ; aucun nouveau PCB planaire n'est fourni. Les bibliothèques relatives du dépôt sont maintenues. L'historique d'éditeur, les dépôts Git imbriqués et les états/verrous sont exclus. Les textes publiés utilisent LF ; l'archive originale n'est pas modifiée. Aucun circuit n'est corrigé automatiquement par cette revue.

## Corrections vérifiées

| Objet | Net courant dans schéma et PCB | Constat |
| --- | --- | --- |
| Q15-7 / SGND | ISENSE3_P | Référence logique désormais sur le net source de Q15 |
| Q15-11 / PGND | ISENSE3_P | Référence du pilote désormais sur le net source de Q15 |
| Q15-12 / S | ISENSE3_P | Source du bras 2 conservée |
| C52-2 | ISENSE3_P | Retour du découplage VDD associé à Q15 |
| C53-2 | ISENSE3_P | Retour du découplage VCC associé à Q15 |
| R59-1 / J5-15 IFB2P | ISENSE3_P | Mesure du bras 2 sur R59 = 10 mΩ |
| R60-1 / J5-24 IFB1P | ISENSE1_P | Mesure du bras 1 sur R60 = 10 mΩ ; nœud distinct |
| R59-2 / R60-2 / IFB1N / IFB2N | ISENSE1_N | Retours bas communs, au-dessus de R52 |
| J5-26 / IFBCOM | ISENSE1_N | Raccordement maintenu au côté haut de R52 = 10 mΩ |
| R35-1 | +400V | Correction du retour bus maintenue |
| J5-17 | Non connectée | Anciens segments +15V toujours absents ; aucun court-circuit signalé par le DRC renforcé |

**A06 est corrigé au niveau du câblage déclaré**, y compris les condensateurs associés. R59 et R60 ne sont pas remis en parallèle : l'ancienne mesure commune de 5 mΩ ne décrit pas cette révision. Q17 conserve source/SGND/PGND sur ISENSE1_P. Le module EGS005Q présente toujours GND2 à P3-17 ; la carte laisse ce pad NC et utilise notamment J5-3/27 pour GND2. Ce point n'est plus présenté comme l'ancien court-circuit +15V.

La cohérence des nets n'est pas une qualification des boucles de commande et de mesure. Vérifier le retour Kelvin, les boucles de découplage, les références des niveaux PWM, les filtres/gains, le signe, les seuils et la dynamique des protections IFB/IFBCOM sur le montage réel. Les formules idéales de chute des shunts restent `VIFB2 = I_R59 × 0,010 Ω`, `VIFB1 = I_R60 × 0,010 Ω` et `VIFBCOM = I_R52 × 0,010 Ω`, pour les courants qui traversent effectivement chaque résistance. Elles ne donnent pas directement le courant AC efficace ni une consigne de protection validée.

## Vérification des fichiers de production

Le ZIP contient les **11 Gerbers** attendus : quatre cuivres, deux masques, deux pâtes, deux sérigraphies et le profil ; il contient aussi le gbrjob et les deux perçages PTH/NPTH. Le gbrjob indique KiCad 10.0.4 et un export du 20 octobre.

Pour vérifier que l'export reprend le PCB reçu, un export natif neuf a été effectué avec KiCad CLI 10.0.5, `pcb export gerbers --board-plot-params`, dans un dossier de travail séparé, sans recalcul des zones. **Les 11 fichiers correspondent ligne par ligne après retrait des seuls en-têtes de version/date/MD5 indiqués dans le rapport.** Aucun tracé, attribut de net ou d'ouverture n'est retiré de cette comparaison. Les attributs X2 de Q15-7/11/12 et C52-2/C53-2 décrivent également ISENSE3_P.

Les perçages ont été regénérés en Excellon, origine absolue, unités mm et fichiers métallisés/non métallisés séparés. **Les deux fichiers correspondent également**, après retrait des en-têtes de version/date et lignes vides. Méthodes et empreintes normalisées : [comparaison de production](reports/2026-10-20/gerber-comparison.json). Les originaux restent publiés tels que reçus. Cette correspondance ne remplace ni le recalcul des zones d'une future révision corrigée, ni l'approbation du circuit et des capacités du fabricant.

## Résultats KiCad 10.0.5

| Contrôle du 20 octobre | Résultat |
| --- | --- |
| Netliste native / pads PCB | **0 écart de net**, 160 composants électriques comparés |
| ERC | **7 erreurs et 11 avertissements** |
| Détail ERC | 6 alimentations non déclarées pilotées, 1 conflit Q13/U3, 10 différences Device:D, 1 nom multiple ISENSE1_N/ISENSE3_N |
| DRC avec réglages fournis | 0 violation et 0 liaison manquante, **17 avertissements de parité** |
| DRC renforcé sur copie | **33 erreurs : 17 espacements et 16 anneaux**, aucun `shorting_items` ; 17 parités |
| Planaire | Source inchangée ; résultat historique conservé : 40 erreurs et 10 avertissements, sans nouvelle exécution revendiquée |

Les quinze familles ignorées par le projet restent inchangées. Le contrôle renforcé active uniquement `clearance`, `hole_clearance` et `annular_width`, sur une copie ; ce n'est pas une validation exhaustive d'isolation haute tension. Le zéro du DRC fourni ne signifie donc pas que les espacements passent.

Les occurrences restent de même nature que le 19 octobre : un écart DESAT1_P / via OUT_HS1_N d'environ 0,1928 mm pour 0,2000 mm demandé, seize espacements autour des géométries thermiques U3/U4, seize anneaux sur les perçages thermiques. Certains libellés d'espacement de ces pads indiquent une valeur supérieure au seuil malgré le signalement : examiner la représentation et les règles réelles avec le fabricant. Il ne s'agit pas de 33 défauts fonctionnels indépendants. Les dix différences de symbole de diode et les six alimentations non déclarées doivent être examinées, sans ajouter des marqueurs d'alimentation simplement pour obtenir un rapport vide. Le conflit Q13/U3 reste à revoir avec la commande du ventilateur. Les 17 parités concernent huit duplications REF** et neuf empreintes mécaniques supplémentaires.

Les catalogues standard sont accessibles lors de cette exécution. Les messages de refus d'accès registre KiCad sont conservés dans les logs de travail ; exports et rapports ont été produits. Aucun ERC réussi et aucun essai sur carte physique ne sont revendiqués.

## Points restant à résoudre

1. Traiter ou justifier individuellement les espacements/anneaux, les erreurs ERC, les différences de bibliothèques et les parités mécaniques. Conserver les contrôles pertinents actifs.
2. Valider les mesures par bras et IFBCOM, la boucle bus et les auxiliaires ; le rail nommé +15V reste calculé idéalement à environ 12,09 V avec les valeurs R48/R49 actuelles.
3. Confirmer le cuivre par couche (35 µm dans PCB/gbrjob contre une ancienne intention de 70 µm) et l'empilage du fabricant.
4. Compléter et qualifier L1 toujours notée 22uF, noyau/transformateur planaire, T5/C57, C3, isolation, refroidissement, plage batterie et fréquence DC-DC mesurée.
5. Après validation, regénérer ensemble Gerbers, perçages, BOM et CPL depuis le commit retenu, puis publier les résultats de banc et le dossier système.

La PR reste ouverte et non fusionnée tant que ces points ne sont pas résolus. Pour le pack et son BMS, voir le [guide batterie](09-batteries-seconde-vie.md) et [cirBATT](https://cirbatt.com/).
