# Mise en service, mesures et dépannage

[Sommaire](README.md) · [Fabrication](05-fabrication.md) · [Audit](07-audit-technique.md)

Cette procédure est une trame de qualification. **La révision publiée ne doit pas être alimentée telle quelle** : les incompatibilités J5, le retour du bus et les défauts de cuivre doivent être examinés et corrigés. La manipulation de la puissance appartient à une personne formée et équipée pour la haute tension.

## Banc et instruments

Préparer alimentation/émulateur batterie à énergie limitée, limitation et protection DC, multimètre adapté, oscilloscope avec sondes différentielles appropriées, mesure de courant isolée, mesure L/C, charge d'essai résistive adaptée, mesure thermique et arrêt accessible. La plage de tension, les limites de courant et le dispositif de décharge doivent être établis avant l'essai.

Ne pas utiliser la batterie de forte capacité comme source du premier essai. Une alimentation limitée en courant peut néanmoins laisser passer l'énergie de ses condensateurs : la limitation ne suffit pas à définir un banc sûr.

Les masses de voies d'un oscilloscope de table sont généralement communes et reliées à la terre. Ne pas les attacher aux sources flottantes des transistors, au bus ou à GND2. Une sonde différentielle doit avoir une tenue au mode commun et aux transitoires adaptée, pas seulement une gamme d'affichage suffisante.

## Étape 0 : revue hors tension

- [ ] Révision matérielle corrigée identifiée ; rapport ERC/DRC joint et anomalies justifiées.
- [ ] J5-17 compatible avec GND du module ; IFBCOM et toutes les protections traitées.
- [ ] Retour `400V` réellement relié au bus prévu ; stabilité et seuils de la limitation vérifiés.
- [ ] Cuivre U4-FB/+15V inspecté et corrigé ; auxiliaires conformes.
- [ ] Module DC-DC identifié ; pas J4, sens et diviseur BAT complets connus.
- [ ] Noyau, connexions du planaire, isolation et refroidissement documentés.
- [ ] Fusible, sectionnement, précharge, décharge et arrêt installés selon une étude adaptée.
- [ ] Polarités C3, diodes, transistors et modules contrôlées ; pas de court-circuit inexpliqué.
- [ ] Schéma du raccordement châssis/terre défini ; GND3 n'a pas été assimilée arbitrairement à PE.

Une mesure à l'ohmmètre sur un condensateur peut évoluer pendant sa charge. Comprendre la mesure avant de conclure qu'un rail est court-circuité ou isolé.

## Étape 1 : auxiliaires et modules séparés

La carte ne possède pas de commande générale d'inhibition clairement documentée. Retirer un module et définir un montage d'essai spécifique est préférable à supposer que tout restera arrêté au branchement.

| Point | Référence de mesure | Valeur / contrôle |
| --- | --- | --- |
| Sortie U3 / J4-7 | GND1, J4-6 | Calcul ≈12,09 V ; comparer à la spécification du module DC-DC |
| Sortie U4 / J5-8 | GND2, J5-3 ou 27 | Calcul ≈12,09 V malgré le nom +15V ; conformité à vérifier |
| Sortie U6 / J5-7 | GND2 | Objectif 5 V, vérifier tolérance et ondulation |
| TH2/TFB1 | GND2 | Idéal ≈0,83 V à 25 °C pour NTC 10 kΩ |
| TH3/TFB2 | GND2 | Idéal ≈1,91 V à 25 °C pour NTC 10 kΩ |

U4 reçoit son énergie du secondaire auxiliaire de T1 : il n'est pas nécessairement alimenté à l'arrêt du DC-DC. Un essai séparé demande un montage défini qui évite le retour d'énergie entre alimentations. Ne pas injecter une tension directement sur les rails sans analyser les chemins de courant.

Tester la carte DC-DC seule selon [son guide](03-reglage-dcdc.md). Tester l'EGS005Q seule selon [son guide](04-reglage-onduleur.md), puis revenir en mode normal. Conserver les relevés de fréquence, amplitude, références et temps morts.

## Étape 2 : DC-DC à énergie limitée

Avec l'onduleur maintenu hors fonctionnement par un moyen validé :

1. Définir tension d'essai et fréquence compatibles avec le noyau, les interrupteurs et la limitation du bus.
2. Brancher les sondes et la charge DC adaptées avant de mettre sous tension. Définir les limites d'arrêt à partir des fiches et marges de conception.
3. Observer démarrage, courant batterie, courant résonant et bus. Le nom +400V ne constitue pas une mesure attendue exacte.
4. Vérifier le fonctionnement de la limitation de tension par une méthode d'essai contrôlée. Ne pas provoquer une surtension en débranchant un retour sous puissance.
5. Contrôler symétrie des commandes, crêtes, éventuelle saturation et échauffement.
6. Couper, attendre la décharge avec le dispositif prévu et **mesurer** l'absence de tension avant de modifier le montage.

Il n'existe pas de résistance de décharge du bus clairement identifiée dans le schéma. Ne pas considérer un temps d'attente fixe comme une preuve de décharge ; ne pas court-circuiter C3 avec un outil.

## Étape 3 : onduleur à vide et sur charge résistive

Après validation du DC-DC et de la compatibilité EGS005Q/GaN :

1. Consigner FS, HM, DT, SST et mode normal. Vérifier que les retours tension/courant sont raccordés et de polarité correcte.
2. Prévoir une charge résistive et un banc compatibles avec le niveau de tension retenu. Mettre sous tension selon la séquence validée.
3. Mesurer la tension efficace entre J7-2 et J7-3, la fréquence, la forme d'onde, l'ondulation HF et l'offset continu.
4. Comparer les mesures indépendantes à la télémétrie du module. Vérifier la stabilité à vide avant de monter la charge.
5. Ajouter des paliers de charge définis par le responsable d'essai. Relever puissance entrée/sortie, courant crête/RMS, températures et tension du bus.

Des charges de 50 W, 100 W, 250 W, etc. peuvent servir à organiser un plan **après** dimensionnement du banc ; elles ne constituent pas des paliers universellement autorisés pour cette révision. Le passage à 1 kW demande une validation thermique et électrique complète. Tester les charges non linéaires et les appels de courant seulement après les charges résistives.

## Étape 4 : protections et durée

Valider sous-tension/surtension batterie et bus, surintensité, surchauffe, défaillance de ventilateur, arrêt et redémarrage. Employer l'injection de signaux ou une méthode qualifiée quand c'est possible. Ne pas essayer un court-circuit franc à pleine batterie pour « voir si cela coupe ».

Documenter seuils, délais, hystérésis et comportement de réarmement. Vérifier si une commande de réarmement pourrait redémarrer automatiquement une charge. La sécurité électrique, les courants de fuite, l'isolation et la CEM demandent des essais distincts des performances de conversion.

## Dépannage guidé par les mesures

| Symptôme | Contrôles prioritaires, hors tension si intervention |
| --- | --- |
| Alimentation auxiliaire s'effondre à l'insertion EGS005Q | Conflit J5-17, orientation, courts-circuits ; ne pas augmenter la limite de courant |
| Bus trop haut ou dérivant | Net 400V/+400V, diviseur et optocoupleur, retour VFB, réglage DC-DC |
| Rail nommé +15V proche de 12 V | Diviseur U4 identique à U3 ; mesurer, vérifier conformité puis traiter le nom/consigne |
| Rail U4 incorrect ou instable | Contacts cuivre FB/+15V, routage, redresseur auxiliaire, marge VIN |
| Courant à vide excessif | Noyau, fréquence, saturation, asymétrie, temps mort, branche L/C |
| Absence d'AC malgré bus présent | Alimentations EGS005Q, mode, défaut déclaré, commandes, retours et IFBCOM |
| AC déformé ou instable | HM/polarités, temps mort, mesures courant, inductance différentielle T5, C57 |
| Fréquence AC incorrecte | FS/JP9/JP10, module réel et configuration ; ne pas tourner R5 du DC-DC |
| Déclenchement thermique inattendu | TH2/TH3, valeurs R40/R42 différentes, loi NTC et couplage thermique |
| Échauffement sans défaut indiqué | Refroidissement, pertes, protection non câblée/mal étalonnée, mode test |

## Fiche de relevé

Copier cette fiche dans un rapport d'essai ; remplir les champs avec des données mesurées, sans remplacer les inconnues par les exemples du guide.

| Élément | Relevé |
| --- | --- |
| Date / opérateur / commit | À renseigner |
| PCB / cuivre / empilage / fabricant | À renseigner |
| Batterie ou émulateur / tension / limitation / protections | À renseigner |
| Modules DC-DC et EGS005Q / révisions | À renseigner |
| Noyau / matériau / assemblage / spires / raccordement | À renseigner |
| Lr / Cr mesurées / méthode / fréquence de mesure | À renseigner |
| Fréquence DC-DC / temps mort / position R5 | À renseigner |
| FS / HM / DT / SST / mode EGS005Q | À renseigner |
| Auxiliaires / bus à vide et en charge | À renseigner |
| Charge / VAC RMS / fréquence / offset / distorsion | À renseigner |
| Courants crête/RMS et puissances entrée/sortie | À renseigner |
| Températures / durée / ambiante / ventilation | À renseigner |
| Seuils et délais de protection mesurés | À renseigner |
| Instruments / sondes / captures / incertitudes | À renseigner |
| Arrêts, anomalies et modifications | À renseigner |

Calculer le rendement à partir de puissances mesurées de manière appropriée : `η = Psortie / Pentrée`. Pour une charge non résistive, `VAC RMS × IAC RMS` donne une puissance apparente ; elle ne remplace pas la mesure de puissance active.

## Préparer une demande d'intégration

Pour échanger avec [cirBATT](https://cirbatt.com/contact) sur l'association batterie/onduleur, transmettre les caractéristiques du pack et du BMS, la révision de la carte et les besoins de l'application. Les relevés nécessaires sont ceux de la fiche ci-dessus et du [guide batterie](09-batteries-seconde-vie.md).
