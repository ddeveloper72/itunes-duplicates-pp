
# playlist.py

# Description: Finding duplicates in a sample iTunes palylist
# Tutorial from: Parsing iTunes Playlists

import re
import argparse
import sys
import plistlib
import numpy as np
from matplotlib import pyplot


def findDuplicates(fileName):
    print('Find duplicate tracks in %s...' % fileName)

    # read in the playlist
    playlist = plistlib.readPlaylist(fileName)

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


def findCommonTracks(fileNames):
    # a list set oif track names
    trackNameSets = []
    for fileName in fileNames:

        # create a new set
        trackNames = set()

        # read in playlist
        playlist = plistlib.readPlist(fileName)

        # get the tracks
        tracks = playlist['Tracks']

        # iterate through the tracks
        for trackId, track in tracks.items():
            try:
                # add trackname to set
                trackNames.add(track['Name'])

            except trackNames.DoesNotExist:
                # ignore
                pass

        # add to list
        trackNameSets.append(trackNames)
    # get the set of common tracks
    findCommonTracks = set.intersection(*trackNameSets)

    # write connon tracks to file
    if len(findCommonTracks) > 0:
        f = open("common-tracks.txt", "w")
        for val in findCommonTracks:
            s = "%s\n" % val
            f.write(s.encode("UTF-8"))
        f.close()
        print("%d common tracks found. "
              "Track names written to common-tracks.txt"
              % len(findCommonTracks))
    else:
        print("No common tracks!")


def plotStats(fileName):
    # read in playlist
    playlist = plistlib.readPlist(fileName)

    # get the tracks from the playlist
    tracks = playlist['Tracks']

    # create a list of song ratings and track durations
    ratings = []
    durations = []

    # iterate through the tracks
    for trackId, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])

        except ratings.DoesNotExist | durations.DoesNotExist:
            # ignore
            pass
    # ensure valid data was collected
    if ratings == [] or durations == []:
        print("No valid Album Rating/Total Time data in %s." % fileName)
        return

    # scatter plot
    x = np.array(durations, np.int32)

    # convert to minutes
    x = x/60000.0
    y = np.array(ratings, np.int32)
    pyplot.subplot(2, 1, 1)
    pyplot(x, y, 'o')
    pyplot.axis([0, 1.05*np.max(x), -1, 110])
    pyplot.xlabel('Track Duration')
    pyplot.ylabel('Track Rating')

    # plot histogram
    pyplot.subplot(2, 1, 2)
    pyplot.hist(x, bins=20)
    pyplot.xlabel('Track Duration')
    pyplot.ylabel('Count')

    # show plot
    pyplot.show()


def main():
    # crate a parser
    descStr = """
    This program analyzes the (.xml) playlist files exported form iTunes
    """
    parser = argparse.ArgumentParser(description=descStr)

    # add mutually exclusive group of arguments
    group = parser.add_mutually_exclusive_group()

    # add expected arguments
    group.add_argument('--common', nargs='*',
                       dest='playListFiles', required=False)
    group.add_argument('--stats', dest='playListFile', required=False)
    group.add_argument('--dup', dest='playListFileD', required=False)

    # parse args
    args = parser.parse_args()

    if args.playListFiles:

        # find common tracks
        findCommonTracks(args.playListFiles)

    elif args.playlistFile:

        # plot stats
        plotStats(args.playListFile)

    elif args.playlistfileD:

        # find duplicate tracks
        findDuplicates(args.playListFileD)

    else:
        print("These are not the tracks you are looking for")


# main method
if __name__ == '__main__':
    main()
