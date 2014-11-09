# Analyse en oursins
###_(Extension pour Qgis 2.0.1 et +)_
L'analyse en oursins permet de représenter des déplacements pendulaires sur une carte pour mettre en évidence des pôles d'attractivités, par exemple pour l'étude de déplacements domicile-travail. 
![](https://raw.githubusercontent.com/LCacheux68224/Oursins/master/ImageDoc/oursin1.png)

## Deux fichiers sont nécessaires :
### 1. Un table de données contenant les paramètres des déplacements ;
Ce fichier doit contenir trois colonnes au minimum :
* Un identifiant géographique du lieu de départ du déplacement ;
* Un identifiant géographique du lieu d'arrivée du déplacement ;
* Le volume du flux observé, c'est à dire le nombre de personnes effectuant le déplacement.

![](https://raw.githubusercontent.com/LCacheux68224/Oursins/master/ImageDoc/Table.png)

Dans cet exemple **COMR** est l'identifiant de la commune de résidence et **COMT** celui de la commune du lieu de travail. **FLUX** correspond au nombre de personnes effectuant ce trajet.

### 2. Un fond de carte (points ou polygones).
Le fond de carte permet d'obtenir automatiquement les coordonnées des points de départs et d'arrivées des déplacements.

## Utilisation : 
L'analyse en oursins se lance soit depuis le menu « **_Vecteur\Outils statistiques\Analyse en oursins_** »,

soit en cliquant sur l'icône ![](https://raw.githubusercontent.com/LCacheux68224/Oursins/master/ImageDoc/oursins.png)

Renseigner les paramètres suivants :
* **Table de flux**-> Table de données contenant la liste des déplacements ;
* **Origine** -> Identifiant géographique du lieu de départ ;
* **Destination** -> Identifiant géographique du lieu d'arrivée ;
* **Flux** -> volume du flux ;
* **Fond de carte** -> fond utilisé pour déterminer les coordonnées ;
* **Identifiant géographique** -> Identifiant géographique permettant de faire la jointure avec les points d'origines et de destinations des déplacements.

Les filtres sont destinés à limiter le nombre de flux représentés. Il est possible de représenter soit tous les flux, soit seulement ceux dépassant une certaine valeur. De même il est possible de ne pas représenter les flux au delà d'une certaine distance. (_La valeur 0 désactive le fitre_) 

Il est possible également de ne sélectionner qu'une partie des entités du fond de carte pour limiter l'analyse à une zone plus restreinte.

![](https://raw.githubusercontent.com/LCacheux68224/Oursins/master/ImageDoc/oursin2.png)

### Deux sorties sont proposées : 
* Une sortie sous forme de carte mémoire qui nécessite l'extension « **Memory Layer Saver** » pour que le fond puisse être enregistré en parallèle au projet dans un fichier _NomDuProjet.qgs.mldata_ ;
* Une sortie sous forme de fond Shapefile classique.









  


