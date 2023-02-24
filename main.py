from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
from youtubesearchpython import VideosSearch
from pathlib import Path
from pytube import YouTube



#utilisation de l'API spotify 

load_dotenv()

#récuperation des données du fichier .env
#données personnels et à récuperer sur le site https://developer.spotify.com/

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

#demande à l'utilisateur le lien d'une playist spotify
#demande à l'utilisateur un nom pour le dossier à creer
playlist_link = input("Entrez lien de la Playlist Spotify à télecharger: ")
directory_folder_name = input("Quel nom souhaitez-vous donner à votre playList ? : ")

# Parent Directory path
parent_dir = "/home/ignite/Musique/"
# Path
path = os.path.join(parent_dir, directory_folder_name)
try:
    os.mkdir(path)
except OSError as error:
    print(error) 
print("démarrage du télechargement de la Playlist'% s' " % directory_folder_name)



# utilisation de l'API spotify
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# télécharge la musique dans le dossier crées précédemment
def download_audio(url):

    yt = YouTube(url)
    video = yt.streams.filter(abr='160kbps').last()
    out_file = video.download(output_path=path)
    base, ext = os.path.splitext(out_file)
    new_file = Path(f'{base}.mp3')
    os.rename(out_file, new_file)

    if new_file.exists():
        print(f'{yt.title} has been successfully downloaded.')
    else:
        print(f'ERROR: {yt.title}could not be downloaded!')

# trouves le premier résultat de la chanson sur youtube 
# utilisation de la playlist youtubesearchpython 

def search_and_download(music):
    videosSearch = VideosSearch(music, limit=1)

    for i in range(1):
        ytb_url = videosSearch.result()['result'][i]['link']
        download_audio(ytb_url)


# get uri from https link
if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", playlist_link):
    playlist_uri = match.groups()[0]
else:
    raise ValueError("Expected format: https://open.spotify.com/playlist/...")

# récupére la liste des morceaux de la playlist 
tracks = sp.playlist_tracks(playlist_uri)["items"]

# extraction du nom et de l'artiste
# appel de la fonction search_and_download pour télecharger
for track in tracks:
    name = track["track"]["name"]
    artists = ", ".join(
        [artist["name"] for artist in track["track"]["artists"]]
    )
    song = name + " " + artists
    
    search_and_download(song)





