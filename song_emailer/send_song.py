#!/usr/bin/env python3
"""
Send a song to an email address

Does not check for validity of transaction, just deals with distributing song
to the user.
"""
import argparse
import ssl
import smtplib
import configparser

def get_message(links):
    """format proper message"""

    message = 'Subject: Soundbin purchase\n\n'
    message += 'Thank you for purchasing music. Here are the download links:\n\n'
    message += '\n'.join(links)

    return message


def links_from_songs(songs, files_config):
    """go from a song name/id to a url to download song"""
    links = []

    # for now, just combine the base url and the song name
    base = files_config['base_url'] + files_config['song_dir']
    for song in songs:
        links.append(base + song)

    return links

def main():
    """Deal with input (called from command line by other software)"""
    # load config
    config = configparser.ConfigParser()
    config.read('config.ini')

    # parse command line arguments
    parser = argparse.ArgumentParser(description='Send purchased songs to an email')
    parser.add_argument('email', help='email address to which songs are sent')
    parser.add_argument('-s', dest='songs', nargs='+', help='song or songs to send')
    args = parser.parse_args()

    dest_email = args.email
    songs = args.songs

    files_config = config['Files']

    links = links_from_songs(songs, files_config)
    message = get_message(links)

    # load email credentials
    with open('email_credentials.txt', 'r') as f:
        src_email = f.readline()
        password = f.readline()
    
    # establish connection to smtp server
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(src_email, password)
        server.sendmail(src_email, dest_email, message)

if __name__ == '__main__':
    main()
