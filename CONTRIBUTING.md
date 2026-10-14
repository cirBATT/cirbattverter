# Contribuer à cirBATTverter

Le projet vise une reproduction indépendante d'un onduleur batterie. Les [points bloquants](docs/07-audit-technique.md) et les [données manquantes](docs/05-fabrication.md) définissent les priorités actuelles.

## Contributions utiles

- Correction J5 / EGS005Q, IFBCOM, retour de bus et contacts cuivre U4-FB.
- Dossier du transformateur : noyau, matériau, spires, connexions, assemblage et mesures.
- Identification de la carte DC-DC et configuration complète des deux modules.
- Validation du filtre de sortie, de l'isolation et des protections.
- Mesures de rendement, courant, tension, températures et qualité de la sinusoïde.
- Correction de valeurs ambiguës dans la BOM et dossier de production complet.
- Amélioration des explications avec des références vérifiables.

## Rapporter une fabrication ou un défaut

Indiquer commit, fabricant PCB, cuivre **par couche**, empilage, modules/révisions, noyau, composants remplacés, paramètres et conditions d'essai. Joindre les captures avec axes, échelles, sondes et références de masse. Une panne doit préciser le symptôme, la chronologie et les pièces affectées ; ne pas la reproduire à forte énergie pour compléter le rapport.

Les modèles d'issues GitHub proposent ces champs. Ne pas déclarer un essai de 1 kW réussi sans durée, tension batterie, température, refroidissement et méthode de mesure.

## Modifier le projet KiCad

Utiliser KiCad 10 avec ses bibliothèques officielles. Ouvrir le `.kicad_pro` correspondant pour charger les tables locales. Les bibliothèques récupérées sont documentées dans [hardware/inverter/libraries/README.md](hardware/inverter/libraries/README.md).

- Ne pas remplacer automatiquement un symbole ou une empreinte récupérée : comparer les broches, pads et références locales.
- Conserver les fichiers `.kicad_prl`, sauvegardes et états locaux hors Git.
- Ne pas changer silencieusement une hypothèse de cuivre, de noyau ou de composant.
- Après modification matérielle, exécuter ERC, DRC et parité avec les contrôles utiles actifs. Justifier les exclusions et leurs effets.
- Regénérer les exports de fabrication après approbation du circuit, puis mettre à jour manifeste et rapports pour la nouvelle révision.

Les erreurs ERC dues au typage d'une broche peuvent avoir une justification ; la consigner. Un contrôle ignoré n'est pas une justification.

## Documentation et pull requests

Expliquer le problème concret, la modification et la validation. Distinguer lecture des sources, calcul, simulation et mesure. Pour des consignes de réglage, préciser la révision du module, le composant concerné et la convention de mesure de fréquence.

Vérifier les liens locaux avec :

```text
python tools/check-documentation.py
```

Ce script contrôle les liens et la présence des rapports. Il ne valide pas la sécurité ou le fonctionnement électrique.

Licence du projet : [CERN-OHL-S-2.0](LICENSE). Les notices externes gardent leur propre licence ; privilégier un lien vers leur éditeur.

## Collaborer avec cirBATT

Ce projet ouvert s'inscrit dans l'activité de [cirBATT — réemploi des batteries lithium à Grenoble](https://cirbatt.com/). Utiliser les issues et pull requests pour les contributions au circuit. Pour une collaboration industrielle, des cellules, un pack ou une intégration BMS, passer par [le contact cirBATT](https://cirbatt.com/contact).
