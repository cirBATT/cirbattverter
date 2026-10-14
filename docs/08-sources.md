# Sources et versions

[Sommaire](README.md)

Notices consultées le **14 octobre 2026**. Les liens pointent vers les fabricants ou vers une copie de leur notice identifiée comme telle. Les PDF propriétaires ne sont pas redistribués dans le dépôt. Relever la version correspondant au composant/module réellement acheté.

## Sources du projet

- [Schéma principal](../hardware/inverter/cirBATTverter_1KWH.kicad_sch), netliste extraite avec KiCad CLI 10.0.5.
- [PCB principal](../hardware/inverter/cirBATTverter_1KWH.kicad_pcb), [projet principal](../hardware/inverter/cirBATTverter_1KWH.kicad_pro), [règles personnalisées](../hardware/inverter/cirBATTverter_1KWH.kicad_dru).
- [PCB planaire](../hardware/planar-transformer/PlanarW_11082026.kicad_pcb), [projet planaire](../hardware/planar-transformer/PlanarW_11082026.kicad_pro).
- [Modèle mécanique](../hardware/mechanical/Cirbatt.step), [exports de production](../production/README.md).
- [Rapports et inventaires](reports/README.md), [manifestes de sources](reports/source-manifest.csv).

## EGS005Q

[EGmicro — EGS005Q, notice utilisateur V1.0](https://www.egmicro.com/static/application/DC-AC%E6%96%B9%E6%A1%88/%E5%8D%95%E5%90%91%E9%80%86%E5%8F%98/EGD1000W_24V%28EG1611%2BEG8025Q%29/%E6%96%87%E6%A1%A3/11.%E7%94%A8%E6%88%B7%E6%89%8B%E5%86%8C_EGS005Q%20%E6%AD%A3%E5%BC%A6%E6%B3%A2%E9%80%86%E5%8F%98%E5%99%A8%E9%A9%B1%E5%8A%A8%E6%9D%BF%E7%94%A8%E6%88%B7%E6%89%8B%E5%86%8CV1.0.pdf).

Le porteur du projet a fourni la même notice ainsi que `12.原理图_EGS005Q_2024-07-26.pdf`. Le schéma daté confirme le connecteur P3, dont **17 = GND2** et **26 = IFBCOM**. La notice fournie et la notice téléchargée ont la même empreinte SHA-256. Les [empreintes des trois documents](reports/controller-documents.json) permettent de retrouver les versions utilisées ; les PDF ne sont pas redistribués ici.

Pages utiles : 3–5 pour photos et brochage ; 6 pour cavaliers ; 7–8 pour test du module ; 9 pour dimensions. Le tableau de temps mort et le paragraphe « défaut usine » de la page 6 se contredisent pour JP3+JP6 : documenté dans le [guide](04-reglage-onduleur.md).

## EGT003

[EGmicro — EGT003_24/48/60V, notice utilisateur V1.0](https://www.egmicro.com/static/application/DC-AC%E6%96%B9%E6%A1%88/%E5%8D%95%E5%90%91%E9%80%86%E5%8F%98/EGD1000W_24V%28EG1611%2BEG8025Q%29/%E6%96%87%E6%A1%A3/15.%E7%94%A8%E6%88%B7%E6%89%8B%E5%86%8C_EGT003_24V%E5%89%8D%E7%BA%A7%E9%A9%B1%E5%8A%A8%E6%9D%BF%E7%94%A8%E6%88%B7%E6%89%8B%E5%86%8CV1_0.pdf).

Le schéma fourni `13.原理图_EGT003_24V_2023-07-06.pdf` confirme le diviseur R3 = 22 kΩ / R4 = 2 kΩ et R5 sur FADJ. Les 24 kΩ ajoutés par la carte principale sont pris en compte dans le [calcul des seuils batterie](03-reglage-dcdc.md#diviseur-batterie-du-schéma-egt003-fourni).

Pages utiles : 1 pour schéma, R5 et variante batterie ; 3 pour brochage ; 4–5 pour test indépendant ; 7 pour pas 2,54 mm. Cette notice établit une correspondance d'interface avec J4 ; elle ne confirme pas le module réellement choisi pour cirBATTverter.

## EG1611

[EGmicro — EG1611, fiche V1.2 du 13 mai 2021](https://www.egmicro.com/static/doc/DC-AC%E7%94%B5%E6%BA%90%E8%8A%AF%E7%89%87/%E5%8D%95%E7%9B%B8%E9%80%86%E5%8F%98/EG1611%E9%80%86%E5%8F%98%E5%99%A8%E6%8E%A8%E6%8C%BD%E5%85%A8%E6%A1%A5PWM%E6%8E%A7%E5%88%B6%E8%8A%AF%E7%89%87%E6%95%B0%E6%8D%AE%E6%89%8B%E5%86%8CV1.2.pdf).

§8.5–8.6 pour FADJ et temps mort du composant. Les valeurs d'un circuit intégré ne doivent pas être confondues avec celles d'un module qui l'utilise.

## EG8025

[EGmicro — EG8025, Datasheet in English V1.0, 13 février 2020](https://www.egmicro.com/static/upload/drive/%E7%BD%91%E7%AB%99%E5%85%AC%E5%BC%80%E8%8A%AF%E7%89%87%E7%94%A8%E6%88%B7%E6%89%8B%E5%86%8C/%E9%80%86%E5%8F%98%E7%94%B5%E6%BA%90/EG8025%20Datasheet%20in%20English%20V1.0%2820200213%29.pdf).

§8.1 pour porteuse ; §8.2–8.5 pour mesures ; §12 pour UART. La documentation de protocole consultée ne fournit pas une procédure d'outil PC validée pour le module du projet.

[Page officielle de la famille EGmicro](https://www.egmicro.com/products/filter_single?category_id=13&lang=en) et [design de référence EG1611 + EG8025Q](https://www.egmicro.com/solution/solution_1?application_id=38&lang=en). Les performances du design de référence ne sont pas des mesures de cirBATTverter.

## Composants auxiliaires et magnétiques

- [Texas Instruments — LM5013](https://www.ti.com/lit/ds/symlink/lm5013.pdf) : référence FB nominale de 1,2 V, brochage et conditions d'alimentation.
- [Texas Instruments — TL431](https://www.ti.com/lit/ds/symlink/tl431.pdf) : référence et conditions de fonctionnement. Le calcul idéal du projet n'est pas une validation de la boucle.
- [Tokmas — CID12N65D, notice fabricant hébergée par X-ON](https://xonstorage.blob.core.windows.net/pdf/tokmas_cid12n65dtokmas_apr22_xonlink.pdf) : pilote intégré, références locales et limites. Le tableau de cette copie contient une incohérence de nom VDD/VCC ; confronter la version livrée au schéma du composant.
- [SMMS1770-330M / C2976970, fiche produit LCSC](https://www.lcsc.com/product-detail/power-inductors_sxn-shun-xiang-nuo-elec-smms1770-330m_C2976970.html) : rapprochement de la référence d'achat L1 avec une inductance 33 µH. Vérifier la notice fabricant avant qualification.
- [PROD Tech — série PDMCAT, notice fabricant hébergée par LCSC, p. 11](https://datasheet.lcsc.com/datasheet/pdf/0494e4526be3390a1f5969b85c025245.pdf?productCode=C2943063) : PDMCAT18107-202ML de mode commun.
- [KiCad — téléchargement](https://www.kicad.org/download/) : installer aussi les bibliothèques officielles.

## Niveaux de preuve utilisés dans le guide

**Source** : valeur, net, cavalier ou information directement trouvé dans un fichier/notice. **Calcul** : résultat dérivé de valeurs explicites, avec hypothèses. **À mesurer** : comportement du matériel qui ne peut pas être confirmé par les sources seules.

Les objectifs 48 V, 230 V et 1 kW viennent de la présentation originale du projet. Aucune qualification sur banc n'est fournie dans le dépôt analysé. Les réglages précis manquants restent donc indiqués comme tels.
