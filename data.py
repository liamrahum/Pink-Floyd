FILE_PATH = 'db.txt'
ALBUM_DELIMITER = '#'
SONG_DELIMITER = '*'
DATA_DELIMITER = '::'
START_INDEX = 1
ERROR = "GIVEN DATA NOT FOUND"


def parse_file():
    """
    Function gets database file and parses it
    :return: albums dict
    """

    # Opens file and reads into buffer
    with open(FILE_PATH, 'r') as file:
        data = file.read()
    albums_dict = {}
    album_details_dict = {}
    songs_dict = {}
    song_dict = {}
    for album in data.split(ALBUM_DELIMITER)[START_INDEX:]:
        # Temporarily save album as variable
        album_data = album[:album.find(SONG_DELIMITER) - 1].split(DATA_DELIMITER)

        album_details_dict['year'] = album_data[START_INDEX]

        # for each song in album...
        for song in album.split(SONG_DELIMITER)[START_INDEX:]:
            # Temporarily save song as variable
            song_data = song.split(DATA_DELIMITER)

            # Convert variables data to dict
            song_dict['singer'] = song_data[START_INDEX]
            song_dict['length'] = song_data[START_INDEX + 1]
            song_dict['lyrics'] = song_data[START_INDEX + 2]

            # Save song data as dict in songs
            songs_dict[song_data[0]] = song_dict.copy()

        # Save songs data as dict in album
        album_details_dict['songs'] = songs_dict.copy()

        # Save albums data as dict in albums
        albums_dict[album_data[0]] = album_details_dict.copy()

        songs_dict = {}  # Reset songs
    return albums_dict


albums = parse_file()  # Gets parsed file data into buffer


def create_response(answer):
    # if none of what we wanted was found, There's an error
    if ERROR in answer:
        return f"404:#ERROR:INVALID ARGUMENTS"
    # if exit message
    if "HAVE A GOOD DAY" in answer:
        return f"200:{answer}"
    # if answer is valid
    return f"200:ANS {answer}"


def get_albums(data):
    return create_response([album for album in albums.keys()])  # returns list of albums as string


def get_album_songs(album_name):
    return create_response([song for song in albums[album_name]["songs"].keys()] if album_name in albums else ERROR)  # returns songs in album if argument is valid


def get_song_len(song_name):
    for album_details in albums.values():
        if song_name in album_details["songs"].keys():
            return create_response(album_details["songs"][song_name]["length"])  # returns song length by name
    return create_response(ERROR)


def get_song_lyrics(song_name):
    for album_details in albums.values():
        if song_name in album_details["songs"].keys():
            return create_response(album_details["songs"][song_name]["lyrics"])  # returns song lyrics if name found
    return create_response(ERROR)


def get_album_by_song(song_name):
    for a_name, a_details in albums.items():
        if song_name in a_details["songs"].keys():
            return create_response(a_name)  # returns album if song found in it
    return create_response(ERROR)


def get_songs_by_word_in_name(word):
    songs = []
    for a_name, a_details in albums.items():
        for song in a_details["songs"].keys():
            if word.lower() in song.lower():
                songs.append(song)
    return create_response(songs)   # returns songs with the word in name


def get_songs_by_lyrics(word):
    songs = []
    for a_name, a_details in albums.items():
        for s_key, s_value in a_details["songs"].items():
            if word.lower() in s_value["lyrics"].lower():
                songs.append(s_key)
    return create_response(songs)   # returns songs with word(s) in lyrics
