# Soundbin Song Emailer

Uses a python script that takes command line input to send links to a song in an email.

Reads from `email_credentials.txt` to get the username and password for a gmail account.

## Usage: 
`./send_song.py email -s SONG ...`

This will use the email account with the provided credentials to send an email with a link to download the listed songs according to the `config.ini` file.

## Example:

`./send_song.py soundbintest+test1@gmail.com -s asdf1.mp3 asdf2.mp3`

leads to the following recieved email:

```
Subject: Soundbin purchase

Thank you for purchasing music. Here are the download links:

http://localhost:8080/songs/asdf1.mp3
http://localhost:8080/songs/asdf2.mp3
```
