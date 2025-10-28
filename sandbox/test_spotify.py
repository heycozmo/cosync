import spotify_control

def main():
    print("pause:")
    print(spotify_control.spotify_pause())

    input("press enter to resume... ")
    print(spotify_control.spotify_resume())

    input("press enter to skip... ")
    print(spotify_control.spotify_next())

    print("done.")

if __name__ == "__main__":
    main()