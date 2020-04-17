# Description
Ceci est un simple bot programmé en Python qui tout les jours entre minuit et une heure du matin vient ajouter 10 nouvelles chansons de Hip-Hop populaires en ce moment (5 Françaises et 5 Américaines) à une playlist Spotify Publique (en remplaçant les 10 chansons du jours précédent). Le bot vérifie que chaque chanson est nouvelle et qu'elle n'a pas déjà été ajoutée dans le passé, afin que chaque jour ce soit 10 musiques encore jamais vu (sur la playlist) qui soit ajoutées.

# Dépendances
- Python (>= 3.2)
- [spotipy](https://github.com/plamere/spotipy) (>= 2.11.1)
- [pytz](https://launchpad.net/pytz) (>= 2019.3)
- [redis](https://github.com/andymccurdy/redis-py) (>= 3.2.1)


# Misc
La playlist sur laquelle le bot est mis en place peut être trouvée ici: https://liamco.io/spotify

# License
[MIT License](LICENSE)
