import AmazonMusic

controller = AmazonMusic()

controller.music_login()
playlist_name = input("Enter a playlist name: ")
song_list = []
for i in range(1):
    song_info = input("Enter song title and author: ").split(" - ")
    song_list.append([song_info[0], song_info[1]])

if not controller.check_playlist(playlist_name):
    controller.create_playlist(playlist_name)

for song in song_list:
    controller.add_to_playlist(song[0], song[1], playlist_name)
