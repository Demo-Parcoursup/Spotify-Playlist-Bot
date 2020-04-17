# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 11:31:59 2020

@author: Liam Cornu
"""

# Import des progiciels nécessaires
import spotipy
import random
import redis
import os
import pytz
import datetime
import time
from creds import username, client_id, client_secret, uri, playlistid

# Pseudo du compte Spotify
pseudo = username

# Connection au compte Spotify via authorisation d'application
Auth = spotipy.util.prompt_for_user_token(pseudo,
                           'playlist-modify-public', # Droits nécessaire par l'application (ici la modification de playlists)
                           client_id=client_id,
                           client_secret=client_secret,
                           redirect_uri=uri
                           )

# Initiation de l'environnement de la base de donnée REDIS
db = redis.from_url(os.environ.get("REDIS_URL"))

# Fonction qui se connecte au compte
def login():
    print('[ INFO ] Connection au compte...')
    sp = spotipy.Spotify(auth=Auth)
    sp.trace = False
    playlist_id = playlistid
    return (sp, playlist_id)

# Fonction qui permet de récupérer toutes les chansons d'une playlist (car l'API Spotify limite le nombre de chansons pouvant être récupérées à 100 par requête)
def get_all_tracks(sp, current_playlist):
    results = sp.playlist_tracks(current_playlist,
                                 offset=0, # Débute à la position 0 (première chanson de la playlist)
                                 fields='items.track.name, items.track.id,total, next', # Renvoie le nom et l'id de chaque chanson, deplus il renvoie le nombre total de chanson dans la playlist et l'url pour récupérer les 100 prochaines chansons
                                 limit=100 # Limite maximale de 100 chansons par requête
                                 )
    tracks = results['items'] # Liste des chansons de la playlist
    total = results['total'] # Nombre totale de chansons dans la playlist
    while results['next']: # Tant qu'il reste d'autre chansons qui n'ont pas encore été récupérées, continuer le loop
        results = sp.next(results)
        tracks.extend(results['items']) # Ajoute les chansons à la liste "tracks"
    return (total, tracks)

# La fonction qui récupères les 10 chansons et les ajoutent à la playlist
def add_tracks(sp, playlist_id):
    
    # Liste de playlists populaires Française et Americaine dans lesquelle le bot va chercher pour de nouvelles musiques de Hip-Hop populaires (format [Nom de la playlist, Id de la playlist])
    US_Playlists = [['RapCaviar', 'spotify:playlist:37i9dQZF1DX0XUsuxWHRQd'], ['Most Essential', 'spotify:playlist:37i9dQZF1DX2RxBh64BHjQ'], ['Hip Hop Central', 'spotify:playlist:37i9dQZF1DWY6tYEFs22tT'], ['Rap Workout', 'spotify:playlist:37i9dQZF1DX76t638V6CA8'], ['Rap 2020', 'spotify:playlist:59rBMYukiDqbIOGsPgwagZ'], ['Get turnt','spotify:playlist:37i9dQZF1DWY4xHQp97fN6'], ['Grimkujow US', 'spotify:playlist:5OpAzLM9zvtGiQTpSnevoN'], ['Postys playlist', 'spotify:playlist:62aTmrLRUWaYSFGbrw23RJ']]
    FR_Playlists = [['Grimkujow FR','spotify:playlist:3VUIBHEVsPLmMfPrv2UFAj'], ['Rap France 2k20', 'spotify:playlist:1cSWAkW9XyjiG67wLtb2bU'], ['Fresh Rap', 'spotify:playlist:37i9dQZF1DWU4xkXueiKGW'], ['PVNCHLNRS', 'spotify:playlist:37i9dQZF1DX1X23oiQRTB5'], ['Rap français 2020', 'spotify:playlist:4l1CEhc7ZPbaEtiPdCSGbl'], ['Rap Fr', 'spotify:playlist:0MF1XGKzqqeL0ZHeqMrq7R']]
    
    # Répète le loop 5 fois afin d'ajouter 5 chansons de Hip-Hop Americaines
    for x in range(5):
        print(f'[ INFO ][ US ] Ajout de la chanson N°{str(x)}')
        current_US_Playlist = random.choice(US_Playlists) # Choisit une playlist aléatoire parmis la liste Américaine
        print(f'[ INFO ][ US ] Playlist choisie: {current_US_Playlist[0]}')
        total, responseone = get_all_tracks(sp, current_US_Playlist[1]) # Récupère l'ensembles des musiques grâce à la fonction précédente
        track_number = random.randint(0, int(total)) # Choisie une chanson au hasard dans la playlist
        track_id = responseone[track_number]['track']['id'] # Récupère l'ID de la chanson
        track_name = responseone[track_number]['track']['name'] # récupère le nom de la chanson
        while db.get(track_id): # Vérifie la base de donnée REDIS si la chanson a déjà été ajoutée dans le passé
            # Si Oui choisir une nouvelle chanson au hasard
            print("[ INFO ][ US ] La chanson choisie a déjà été ajoutée dans le passé, en cours de recherche d'une nouvelle chanson...")
            current_US_Playlist = random.choice(US_Playlists)
            print(f'[ INFO ][ US ] Playlist choisie: {current_US_Playlist[0]}')
            total, responseone = get_all_tracks(sp, current_US_Playlist[1])
            track_number = random.randint(0, int(total))
            track_id = responseone[track_number]['track']['id']
            track_name = responseone[track_number]['track']['name']
        print(f'[ INFO ][ US ] Chanson choisie: {track_name}')              
        sp.user_playlist_add_tracks(username, playlist_id, [track_id]) # Ajoute la chanson à la playlist personelle
        db.set(track_id, 'true') # Ajoute l'id de la chanson à la base de donnée REDIS afin d'éviter de la selectioner une autre fois
        print(f'[ INFO ][ US ] La chanson N°{str(x)} a été ajoutée avec succès')
        time.sleep(3)
        
    # Même principe mais avec 5 chansons de Hip-Hop françaises
    for x in range(5):
        print(f'[ INFO ][ FR ] Ajout de la chanson N°{str(x)}')
        current_FR_Playlist = random.choice(FR_Playlists)
        print(f'[ INFO ][ FR ] Playlist choisie: {current_US_Playlist[0]}')
        total, responsetwo = get_all_tracks(sp, current_FR_Playlist[1])
        track_number = random.randint(0, int(total))
        track_id = responsetwo[track_number]['track']['id']
        track_name = responsetwo[track_number]['track']['name']
        while db.get(track_id):
            print("[ INFO ][ FR ] La chanson choisie a déjà été ajoutée dans le passé, en cours de recherche d'une autre...")
            current_US_Playlist = random.choice(FR_Playlists)
            print('[ INFO ][ FR ] Playlist choisie: {current_US_Playlist[0]}')
            total, responsetwo = get_all_tracks(sp, current_FR_Playlist[1])
            track_number = random.randint(0, int(total))
            track_id = responsetwo[track_number]['track']['id']
            track_name = responsetwo[track_number]['track']['name']
        print('[ INFO ][ FR ] Chanson choisie: {track_name}')              
        sp.user_playlist_add_tracks(username, playlist_id, [track_id])
        db.set(track_id, 'true')
        print(f'[ INFO ][ FR ] La chanson N°{str(x)} a été ajoutée avec succès')     
        time.sleep(3)
        
# Fonction qui supprime toutes les (10) musiques de la playlist personelle
def remove_tracks(sp, playlist_id):
    tracks = [] # Liste vide des chansons
    response = sp.playlist_tracks(playlist_id,
                                  offset=0, # Débute à la position 0
                                  fields='items.track.id' # Récupère les ids des chansons
                                  )
    # Ajoute l'ID de chaque chanson dans la playlist personnelle à la liste "tracks"
    for elt, item in enumerate(response['items']):
        tracks.append(item['track']['id'])
    print("[ INFO ] Suppression des chansons de la playlist")
    # Suppression de toute les chansons via les ids de la liste "tracks" (donc suppression de toutes les chansons de la playlist)
    sp.user_playlist_remove_all_occurrences_of_tracks(
        username, playlist_id, tracks) 

# Va récupérer l'id de la playlist et le wrapper de l'API Spotify via la fonction "login"
sp, playlist_id = login()

# Tant que le token d'authorisation Spotify au compte est actif, continuer le loop (le token s'auto-rafraîchit)
while Auth:
    tz = pytz.timezone('Europe/Berlin') # Mise en place du fuseau horaire (Français)
    heure = datetime.datetime.now(tz).strftime('%H') # Récupère l'heure en format 24 heure (exemple '12' pour midi)
    jour = datetime.datetime.now(tz).strftime('%D') # Récupère la date en format mois/jour/année (exemple 04/17/20 pour le 17 avril 2020)
    if heure == "00": # Vérifie si il est minuit (heure française (fuseau horaire CET))
        if db.get(jour): # Si la date figure déjà dans la base de donnée REDIS (voulant dire que de nouvelles chansons ont déjà été ajoutées), attendre 1 heure
            # Utile si le serveur où est herbergé le bot reboot ou si le script crash et se relance entre minuit et 1 heure du matin, afin d'éviter de rafraichir la playlist pour rien
            print('[ INFO ] Date déjà enregistrée (Reboot Serveur)')
            time.sleep(3600)
        else:
            # Si il est entre minuit et une heure du matin, supprimer toutes les chansons de la playlist et en ajouter 10 nouvelles
            remove_tracks(sp, playlist_id)
            add_tracks(sp, playlist_id)
            db.set(jour, 'true') # Ajout de la date à la base de donnée REDIS
    else:
        # Si il n'est pas encore minuit, attendre pendant une heure et réessayer
        print("[ INFO ] Pas encore minuit, en attente pendant une heure")
        time.sleep(3600)
else:
    # Si le token n'est plus valide, log un message d'érreur
    print("[ ERREUR ] Impossible de récupérer le token d'authorisation Spotify (expiré?)")