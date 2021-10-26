#Artist sans images!
select a.idArtist, a.strArtist, b.strAlbum, s.strTitle From artist a,album b,  song s ,song_artist sa  WHERE
sa.idArtist = a.idArtist AND
sa.idSong = s.idSong AND
s.idAlbum = b.idAlbum AND
a.idArtist Not in ( select media_id from  art
                    where media_type = 'artist')
					
#Song avec au moins 2 role pour le même artist
SELECT DISTINCT *
FROM song_artist t1
WHERE EXISTS (
              SELECT *
              FROM song_artist t2
              WHERE t1.idRole <> t2.idRole
              AND   t1.idArtist = t2.idArtist
			  AND   t1.idSong = t2.idSong )

#Song/Album qui n ont pas le même genre
SELECT s.idSong, s.strTitle, b.strAlbum , s.strGenres "Song Genre", b.strGenres "Album Genre"
FROM  song s, song_genre sg, album b, genre g
WHERE  s.idSong = sg.idSong
AND    sg.idGenre = g.idGenre
AND    s.strGenres <> b.strGenres 
AND    s.idAlbum  = b.idAlbum

#Song/artist qui n ont pas le même genre
SELECT s.idSong, s.strTitle, a.strArtist , s.strGenres "Song Genre", a.strGenres "Artist Genre"
FROM  song s, song_genre sg, artist a, genre g
WHERE  s.idSong = sg.idSong
AND    sg.idGenre = g.idGenre
AND    s.strGenres <> a.strGenres 
AND    s.strArtistDisp  = a.strArtist

#Purge album_artist sans lien avec un album
DELETE FROM album_artist WHERE album_artist.idAlbum  NOT IN (SELECT album.idAlbum  FROM album WHERE album.idAlbum IS NOT NULL)
ou 
SELECT * FROM album_artist WHERE album_artist.idAlbum  NOT IN (SELECT album.idAlbum  FROM album WHERE album.idAlbum IS NOT NULL)

#Purge artist sans lien avec album_artist
DELETE FROM artist WHERE artist.idArtist  NOT IN (SELECT album_artist.idArtist  FROM album_artist WHERE album_artist.idArtist IS NOT NULL)
ou
SELECT * FROM artist WHERE artist.idArtist  NOT IN (SELECT album_artist.idArtist  FROM album_artist WHERE album_artist.idArtist IS NOT NULL)
