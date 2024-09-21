0. Une run de simulation donne l'amplitude à un point de lecture selon un point d'impact
1. Poser une géométrie, matériau et localisation de capteur fixe
2. Run et stocker les réponses d'amplitude aux impacts en chaque point de la grille
3. Normaliser les données (diviser par le maximum)
4. Faire (ou prendre) une réponse d'amplitude (aka un tap)
5. Calculer la corrélation de cette réponse avec tous les réponses de référence
6. Faire la map de corrélation
7. Prendre la slice dans une direction où le maximum est localisé
8. Faire son graphique
9. Déterminer la résolution et le contraste
10. Répéter 4 à 9 plusieurs fois pour faire étude statistique

11. Répéter pour plusieurs paramètres

## TODO

- figure out l'histoire des axes flippés
- rendre les graphiques beaux avec les labels de mm
- redéfinir les géométries
- définir la batterie de tests (attention aux points hors matière)
- tweak le nom du fichier pour encompass toutes les variables
- save les graphs

## Rencontre Jean

- Réduire la taille des signaux / de leurs dictionnaires pour réduire les retards
- Faire des graphiques de résolution et/ou contraste p/r à nos paramètres tweakés pour pouvoir dire les sweet spots
- Présenter des graphs condensés avec énormément d'info, on a juste 3 pages
