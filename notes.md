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

- voir si il faut que les hits de l'entrainement soient séparés de 4 cells du bord
- rendu à step 9
- flip les axes x et y pour les labels (ou pour le data, à voir)
- figure out comment avoir résolution et contraste
- Bien définir matériau avec distances et propriétés

## Tips

- Faire seulement 2-3 rangées pour sauver du temps de simulation
- Prendre résolution et contraste à l'oeil
