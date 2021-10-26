DELETE FROM artist WHERE artist.idArtist  NOT IN (SELECT album_artist.idArtist  FROM album_artist WHERE album_artist.idArtist IS NOT NULL)
ou
SELECT * FROM artist WHERE artist.idArtist  NOT IN (SELECT album_artist.idArtist  FROM album_artist WHERE album_artist.idArtist IS NOT NULL)
