DELETE FROM album_artist WHERE album_artist.idAlbum  NOT IN (SELECT album.idAlbum  FROM album WHERE album.idAlbum IS NOT NULL)
ou 
SELECT * FROM album_artist WHERE album_artist.idAlbum  NOT IN (SELECT album.idAlbum  FROM album WHERE album.idAlbum IS NOT NULL)
