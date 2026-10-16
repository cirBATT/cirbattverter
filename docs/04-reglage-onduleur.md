# Configurer l'onduleur EGS005Q

[Sommaire](README.md) · [Connectique](02-connectique.md) · [Mise en service](06-mise-en-service.md)

Le porteur du projet a confirmé **EGS005Q**. Les réglages ci-dessous se rapportent à la **notice V1.0**, dont les tableaux et photos ont été vérifiés. Une carte vendue sous un nom voisin ou une révision différente doit être contrôlée avant usage.

**Prérequis : corriger la compatibilité J5, les défauts du bus et du PCB.** Dans la révision reçue le 16 octobre, J5-17 est marquée non connectée mais touche encore des pistes `+15V` sur In2.Cu, alors que le module y présente GND. Les cavaliers ne permettent pas de corriger cette erreur.

## Fréquence de sortie

| Fonction | Cavalier fermé | Cavalier de la même paire ouvert |
| --- | --- | --- |
| 50 Hz | JP9 | JP10 |
| 60 Hz | JP10 | JP9 |
| Fonctionnement normal | JP7 | JP8 |
| Démarrage progressif activé | JP12 | JP11 |

Les groupes sont repérés **FS/FRQSEL**, **TSM/Test_Mode** et **SST**. Ne jamais fermer les deux choix d'une même paire. [Notice EGS005Q, §3.3, p. 6](08-sources.md#egs005q).

Procédure : mettre hors tension, vérifier l'absence de tension et la décharge, identifier les cavaliers sur la **carte réelle**, relever leur position, sélectionner la fréquence, puis contrôler la sortie lors de la mise en service qualifiée. À 50 Hz, attendre 20 ms par cycle ; à 60 Hz, environ 16,67 ms. Vérifier également la tension efficace, la forme d'onde et une éventuelle composante continue.

Ici, « fréquence réseau » désigne la fréquence choisie pour alimenter des appareils. Cela **n'autorise pas un raccordement au réseau public** : le projet ne documente pas une synchronisation ou une protection d'injection réseau.

## Temps mort

Le temps mort évite une conduction simultanée des interrupteurs d'un bras. Un temps trop court favorise les courants traversants ; un temps trop long déforme la sinusoïde et augmente certaines pertes.

| DT1:DT0 | Cavaliers fermés | Temps mort selon le tableau V1.0 |
| --- | --- | --- |
| 00 | JP3 + JP5 | 300 ns |
| 01 | JP4 + JP5 | 500 ns |
| 10 | JP3 + JP6 | 1 µs |
| 11 | JP4 + JP6 | 1,5 µs |

La notice comporte une contradiction : son paragraphe « réglage usine » cite JP3+JP6 mais annonce 500 ns, alors que son tableau donne **1 µs**. Se fier au tableau pour identifier la configuration, puis **mesurer** le temps mort réel. Il n'existe pas de temps mort qualifié pour ce PCB dans le dépôt. [Notice EGS005Q, p. 6](08-sources.md#egs005q).

Ne pas choisir 300 ns au motif que les GaN sont rapides. Il faut tenir compte de la chaîne EGS005Q → entrée PWM → pilote intégré, des délais et des références locales. Observer les commandes de chaque interrupteur par rapport à sa propre référence, avec des sondes appropriées.

## Sélection des bras HM

Le module associe HM=0 à JP1 et HM=1 à JP2. Le choix dépend du bras connecté au côté OUTL de la boucle de mesure. Dans la netliste du projet, le bras pilote 2, Q14/Q15, rejoint OUT_P via T5, et OUT_P est raccordé à J5-28. Cela rend **HM=0 / JP1 cohérent avec l'intention de câblage**.

C'est une déduction du schéma, pas une validation de stabilité. Vérifier la polarité de T5, le sens des retours de courant et de tension et les commandes réellement appliquées avant l'essai en boucle fermée. Ne pas utiliser HM pour compenser un câblage incorrect des retours.

## Mode de test

JP8 place le module en mode de test ; JP7 correspond au mode normal. En test, les protections et retours ne supervisent pas la sortie comme en fonctionnement normal. **Réserver ce mode au module isolé du circuit de puissance**, selon son montage de test officiel. [Notice EGS005Q, §4.2](08-sources.md#egs005q).

Un signal correct en test ne prouve pas le bon câblage des protections. Revenir à JP7, JP8 ouvert, et vérifier ce point explicitement avant toute mise en service de la puissance.

## Tension de sortie et calibration

L'objectif est 230 V **efficace** entre OUT_P et OUT_N. Ne pas régler cette valeur par le potentiomètre de fréquence du DC-DC, ni interpréter le nom `+400V` comme une consigne de sortie AC.

EGmicro documente une configuration/calibration par UART et un outil fabricant pour EG8025. L'outil, sa version et une procédure validée avec le module du projet ne sont pas fournis. Ne pas inventer un menu, une adresse de registre ou une trame d'écriture à partir d'un autre contrôleur.

Après correction matérielle, la procédure à documenter est :

1. Sur le module seul, sauvegarder les paramètres existants et identifier la version du logiciel interne/protocole.
2. Utiliser l'outil et les instructions correspondant à cette version. Consigner les valeurs de tension, courant, puissance, température et protections avant tout changement.
3. Lors d'un essai qualifié, comparer un instrument True RMS indépendant aux valeurs lues par le module. Vérifier également l'amplitude et la forme de la sinusoïde à l'oscilloscope.
4. Ajuster la consigne et les coefficients de mesure selon la procédure fabricant. Un coefficient de calibration corrige une mesure ; une consigne fixe une cible. Ne pas les confondre.
5. Relire les réglages après redémarrage et les vérifier à vide puis sous charges progressives. Conserver le fichier de paramètres avec la révision du matériel.

Ne pas afficher 1 kW ou 4,35 A comme seuils qualifiés : les limites thermiques, de courant crête et de court-circuit restent à établir pour cette carte.

## Liaison UART

Le protocole EG8025 V1.0 documente **9600 bauds, 8 bits, sans parité, 1 bit de stop**. TXD0 du module se raccorde au RX de l'interface, RXD0 au TX, avec une référence commune sur le banc basse tension. Vérifier les niveaux logiques ; il ne s'agit pas d'une liaison RS-232 ±12 V. [Notice EG8025, §12](08-sources.md#eg8025).

Le port du module est référencé à GND2. Sur une carte sous haute tension, il faut une interface isolée correctement spécifiée. Ne pas relier un PC directement à GND2. Ne pas mettre en parallèle le +5 V d'un adaptateur et celui du module sans avoir étudié leur alimentation.

## Température et courant

Sur la carte principale :

```text
TFB1 = 5 × R40 / (RTH2 + R40), R40 = 2 kΩ
TFB2 = 5 × R42 / (RTH3 + R42), R42 = 6,2 kΩ
```

À 25 °C, si les NTC valent réellement 10 kΩ, on attend idéalement environ 0,83 V et 1,91 V. Les deux canaux ont donc des lois différentes. Pour convertir une tension de déclenchement en température, il faut la courbe R(T), le coefficient B, la tolérance et l'emplacement des NTC. Ils ne sont pas documentés complètement ici.

Les shunts marqués `10m` sont 10 mΩ, pas 10 MΩ. Leur dissipation suit `P = I²R`. Le seuil réel dépend du montage, des amplificateurs du module et du courant instantané. La révision reçue relie maintenant source et références de Q15 à ISENSE1_P, comme Q17. R59 et R60 sont en parallèle (5 mΩ idéaux) et IFB1/IFB2 voient la même mesure. J5-26 rejoint le côté ISENSE1_N de R52 = 10 mΩ. Cette nouvelle topologie impose une revue des gains, seuils et chemins de courant avant calibration ; voir la [revue actuelle](10-revue-corrections-2026-10-16.md#mesure-du-courant-après-la-correction-q15).

## Fiche de configuration à publier

| Paramètre | Valeur à enregistrer |
| --- | --- |
| Référence et révision du module | EGS005Q, révision réelle à relever |
| Fréquence choisie / mesurée | 50 ou 60 Hz / mesure |
| HM | Position et vérification de polarité |
| DT1:DT0 | Cavaliers / temps mort mesuré |
| TSM | Normal avant essai puissance |
| SST | Position / comportement de démarrage |
| Tension AC | Consigne / valeur mesurée à vide et en charge |
| Mesures courant et température | Coefficients et instrument de référence |
| Protections | Seuil, délai, réarmement et essai de validation |
| UART | Version logiciel/protocole et fichier sauvegardé |

Le vert du module peut indiquer un fonctionnement déclaré normal. Il ne confirme ni l'isolation, ni la qualité de la sinusoïde, ni l'efficacité d'une protection laissée non câblée.

## Contexte du projet cirBATT

Ce guide documente la conversion AC du projet [cirBATT](https://cirbatt.com/). Le réglage EGS005Q ne configure pas le BMS ni un chargeur solaire. Pour comprendre une chaîne de stockage plus complète, lire la ressource cirBATT sur le [stockage solaire avec des batteries de seconde vie](https://cirbatt.com/stocker-energie-solaire-batterie-seconde-vie).
