# Régler le DC-DC et comprendre la résonance

[Sommaire](README.md) · [Connectique](02-connectique.md) · [Mise en service](06-mise-en-service.md)

**Aucune fréquence DC-DC validée n'est fournie dans le dépôt.** Ne pas utiliser les exemples ci-dessous comme une consigne à appliquer directement à la puissance. La référence et la révision de la carte DC-DC restent à confirmer ; l'EGS005Q confirmé par le porteur du projet commande l'onduleur AC, pas cet étage.

## Deux notions différentes

La **fréquence de résonance** appartient au circuit L/C et à ses parasites. La **fréquence de commutation** est réglée par la carte de contrôle. Tourner un potentiomètre change la seconde ; cela ne change pas la première.

Le but du réglage est de choisir une commutation compatible avec les caractéristiques réelles du transformateur, la branche résonante, la batterie et la charge. Ce choix doit être confirmé par les formes d'onde de courant et de tension.

## Ce que montrent les sources

| Élément | Donnée publiée | Conséquence |
| --- | --- | --- |
| L1 | Valeur `22uF` ; LCSC C2976970 ; bibliothèque SMMS1770-330M | Unité incorrecte et valeur contradictoire ; composant d'achat annoncé à 33 µH |
| C2 | 100 nF | Vérifier capacité réelle, tolérance, tenue en tension et courant HF |
| T1 | Primaire + deux secondaires, sans caractéristiques magnétiques | Inductance de fuite et flux à déterminer |
| T4 | CS4200V-01L, détection courant en série | Rapport et bande passante à confirmer pour les seuils |
| J4 | 14 broches, ordre EGT003, empreinte 1,27 mm | Module exact et adaptation mécanique manquants |

La donnée 33 µH provient de la [fiche de la référence C2976970](https://www.lcsc.com/product-detail/power-inductors_sxn-shun-xiang-nuo-elec-smms1770-330m_C2976970.html). Elle doit être confrontée à la notice du composant réellement monté et à sa mesure sous les conditions utiles.

## Diviseur batterie du schéma EGT003 fourni

Le schéma `13.原理图_EGT003_24V_2023-07-06.pdf` fourni par le porteur du projet montre **R3 = 22 kΩ** et **R4 = 2 kΩ** sur le module. Les R39/R50 de la carte principale ajoutent 24 kΩ en série en amont. Avec ce module précis et sans autre modification, le facteur total de division vaut :

```text
(24 + 22 + 2) / 2 = 24
```

En utilisant les seuils nominaux de la notice EG1611 V1.2 :

| Fonction | Seuil au circuit intégré | Seuil batterie calculé |
| --- | --- | --- |
| Coupure sous-tension | 1,66 V | 39,84 V |
| Alarme sous-tension | 1,75 V | 42,00 V |
| Coupure surtension | 2,50 V | 60,00 V |

Cette combinaison est cohérente avec l'intention d'adapter le module **24 V** à la carte d'entrée nominale 48 V. C'est une déduction du réseau de résistances. Ces seuils théoriques restent à mesurer et à confronter au pack/BMS utilisé ; ils ne qualifient pas une chimie ou un nombre de cellules particulier. Le montage d'une variante module déjà modifiée pour 48 V changerait ces résultats. [Schéma fourni et notice EG1611](08-sources.md#egt003).

## Calcul préliminaire

Pour un LC série idéal :

```text
f0 = 1 / (2π × √(Lr × Cr))
```

`Lr` est en henrys, `Cr` en farads, le résultat en hertz. Dans ce design, raisonner côté secondaire de puissance. Une inductance mesurée côté primaire doit être ramenée au même côté avec le carré du rapport de spires.

| Hypothèse de calcul, non validée | Résultat idéal |
| --- | --- |
| Lr = 22 µH ; Cr = 100 nF | 107,30 kHz |
| Lr = 33 µH ; Cr = 100 nF | 87,61 kHz |

Ces deux valeurs expliquent pourquoi il faut résoudre la nomenclature de L1. L'inductance effective inclut notamment la fuite du transformateur et les connexions. Ne pas utiliser son inductance magnétisante comme inductance de fuite. Les caractéristiques peuvent évoluer avec le courant et la température.

Exemple de sensibilité : avec une hypothèse de ±20 % sur L et ±10 % sur C, le LC idéal peut varier d'environ −13 % à +18 % en fréquence. Les tolérances réelles de C2 doivent être relevées, pas reprises de cet exemple.

La [fiche de réglage](06-mise-en-service.md#fiche-de-relevé) doit contenir **Lr mesurée, Cr mesurée, configuration du noyau, fréquence choisie et captures de validation**.

## Réglage si le module est bien un EGT003 / EG1611

Pour **EGT003 V1.0**, la notice identifie **R5** comme potentiomètre de fréquence, annonce 40–100 kHz et un temps mort du module de 700 ns. Le pas annoncé est 2,54 mm. Ne pas confondre R5 du module avec les résistances de la carte principale. [Notice EGT003, pp. 1 et 7](08-sources.md#egt003).

Le **composant EG1611 V1.2** utilise FADJ, broche 12. Sa loi indicative est :

```text
f en kHz ≈ 8000 / (200 − 128 × VFADJ / 3)
VFADJ ≈ (3 / 128) × (200 − 8000 / f_kHz)
```

Sa notice décrit 0–3 V pour environ 40–111 kHz, et 500 ns pour le temps mort interne. **Les spécifications du module ne sont pas identiques à celles du circuit intégré** : mesurer les quatre sorties du module acheté. [Notice EG1611 V1.2, §8.5–8.6](08-sources.md#eg1611).

La formule sert à contrôler la cohérence d'une mesure FADJ/fréquence, pas à générer une tension arbitraire sur cette broche. Ne pas forcer FADJ depuis une alimentation externe sans schéma complet du module.

## Procédure de configuration

### A. Identifier et tester la commande seule

1. Retirer le module de la carte de puissance. Relever référence, révision, brochage, pas et positions des réglages.
2. Suivre le montage de test basse tension de **sa** notice. La simulation de BAT et des retours doit correspondre à la variante achetée. Les pontages de la notice de test ne doivent jamais être recopiés sur la carte de puissance alimentée.
3. Alimenter le module avec une source limitée en courant conforme à sa notice. Vérifier les alimentations avant d'observer les sorties.
4. Mesurer la fréquence **entre deux fronts successifs de même sens sur une sortie donnée**. Noter la convention ; ne pas confondre deux impulsions complémentaires avec une fréquence doublée.
5. Si R5 est présent et correspond à la notice, ajuster pour une fréquence cible **déjà calculée et approuvée**. La direction mécanique du réglage n'est pas documentée ici : observer l'effet d'une petite variation sur le module seul.
6. Mesurer rapport cyclique, complémentarité et temps mort. Le réglage de fréquence ne doit pas faire disparaître l'intervalle sans conduction.

### B. Valider le circuit de puissance

Cette étape n'est autorisée techniquement qu'après résolution des [défauts bloquants](07-audit-technique.md), caractérisation magnétique et préparation du banc par une personne qualifiée.

1. Établir la plage de fonctionnement compatible avec le noyau, la tension batterie et les composants. Une fréquence trop basse peut saturer le noyau ; « commencer le plus bas possible » n'est pas une procédure sûre.
2. Prévoir un essai à énergie limitée, avec limitation de courant, arrêt accessible et charge d'essai adaptée. La limite de courant d'une alimentation doit tenir compte de l'énergie stockée dans ses condensateurs et dans la carte.
3. Mesurer simultanément courant résonant et commutations pertinentes avec des instruments adaptés. Vérifier la tension du bus et le courant absorbé, pas seulement la fréquence affichée.
4. Comparer les instants de commutation à la forme du courant. Chercher une commutation douce réellement observée, avec des crêtes acceptables et sans dérive du courant magnétisant. Ne pas déclarer du ZVS ou du ZCS à partir d'une seule capture de grille.
5. Arrêter à toute surintensité inattendue, oscillation non expliquée, tension excessive, asymétrie ou échauffement rapide. Revenir hors tension avant de changer le réglage ou le câblage.
6. Valider ensuite aux tensions minimale/nominale/maximale de la batterie, à vide et sous charges progressives, puis à chaud. Enregistrer fréquence, courants crête/RMS, températures, tension du bus et rendement.

Il n'existe donc pas ici de « position du potentiomètre universelle ». Le dossier doit publier le réglage du prototype mesuré avant de permettre une reproduction indépendante.

## Batterie et protections du DC-DC

Le réseau BAT comprend les résistances **de la carte et du module**. Si le module possède un diviseur simple avec résistance haute `Rhaut_module` et basse `Rbas_module`, et sans autre branche significative :

```text
Vmesure ≈ Vbatterie × Rbas_module /
           (24 kΩ + Rhaut_module + Rbas_module)
```

Cette formule provient du câblage R39/R50 du projet et suppose le réseau du module vérifié. Par exemple, ajouter les 24 kΩ de cette carte à un diviseur déjà prévu pour une batterie 48 V modifie fortement ses seuils. **Ne pas acheter une variante « 48 V » et supposer que la protection restera correcte.** Les seuils doivent être définis d'après la chimie, le nombre de cellules et le BMS.

Le seuil IFB dépend du rapport réel de T4, de R25, des diodes et des formes d'onde. Celui de TEMP dépend de TH4 et du circuit du module. Publier les seuils de coupure et de réarmement mesurés. Le BMS ne remplace pas une protection correctement configurée du convertisseur.

Le retour VFB doit aussi fonctionner : corriger et vérifier le net `400V` avant de considérer la limitation de bus disponible. Ne pas masquer un défaut de retour par une augmentation de fréquence.

## Associer les seuils au pack réel

Les seuils batterie doivent être cohérents avec la chimie, le nombre de cellules et le BMS. Les pages [packs batteries cirBATT](https://cirbatt.com/packs) et [BMS pour batteries de seconde vie](https://cirbatt.com/bms-pro) donnent le contexte de ces fonctions ; la configuration compatible avec ce convertisseur reste à établir selon le [guide batterie](09-batteries-seconde-vie.md).
