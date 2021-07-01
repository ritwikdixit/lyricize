# lyricize
fast access to song lyrics from my spotify library with twilio &amp; genius

Usage:

[line/verse/verse_n] from [artist/album/song] [name]  
Songs query can only start with a prefix. verse_n will give nth "verse" or paragraph off genius.  
For tiebreaker songs (get song with wrong artist) just use song query and artist after

i.e.
line from song backseat freestyle  
line from album 1989  
verse from song heartless kanye west  
verse_2 from song forever drake (extra details for tiebreaker)  
   
Artist & album nicknames can be set with:  
nickname [nick]=full name  

otherwise for random:  
list N [artists/albums]
