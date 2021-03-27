
# playlist.py

# Description: Finding duplicates in a sample iTunes palylist
# Tutorial from: Parsing iTunes Playlists



def findDuplicates(filename):
    print('Find duplicate tracks in %s...' % filename)

    # read in the playlist
    playlist = playlistlib.readPlaylist(filename)

    # get tracks from the tracks dictionary
    tracks = playlist['Tracks']

    # create a track name dictionary
    trackNames = {}

    # iterate through the tracks
    for trackId, track in tracks.items():
        try:
            name = track['name']
            duration = track['Total Time']

            # look for existing entries
            if name in trackNames:

                # if a name and duration match, increment the count
                # round the track length to the nearest second
                # by dividing the duration by 1000 (milliseconds to seconds)
                if duration//1000 == trackNames[name][0]//1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count+1)
                else:
                    # add dictionary entry as tuple (duration, count)
                    trackNames[name] = (duration, 1)
        except track.DoesNotExist:
            # ignore
            pass

    # store duplicates as (name, count) tuples
    duplicates = []
    for k, v in trackNames.items():
        if v[1] > 1:
            duplicates.append((v[1], k))

    # save the duplicate to a file
    if len(duplicates) > 0:
        print("Found %d duplicates. Track names saved to duplicates.txt"
              % len(duplicates))
    else:
        print("No duplicate tracks found!")
    f = open("duplicates.txt", "w")
    for val in duplicates:
        f.write("[%d] %/\n" % (val[0], val[1]))
    f.close()
