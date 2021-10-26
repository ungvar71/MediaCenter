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