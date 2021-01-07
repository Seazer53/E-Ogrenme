from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = "Çok gizli"


# giriş yapma ekranını yükler
@app.route('/', methods=["GET", "POST"])
def login():
    return render_template("login.html")


# kayıt olma ekranını yükler
@app.route('/kayit', methods=["GET", "POST"])
def kayit():
    return render_template("kayit.html")


# hesap oluşturur, hata varsa kayıt sayfasını döner
@app.route('/hesapolustur', methods=["GET", "POST"])
def hesapolustur():
    yetki = request.form["yetki"]
    adi = request.form["ad"]
    soyadi = request.form["soyad"]
    dogumtarihi = request.form["dogumtarihi"]
    telefon = request.form["telefon"]
    email = request.form["email"]
    email2 = request.form["email2"]
    sifre = request.form["sifre"]
    sifre2 = request.form["sifre2"]
    hata_var = False

    # email adreslerinin uyuşup uyuşmadığını kontrol eder uyuşmazsa hata mesajını kayıt ekranında gösterir
    if email != email2:
        hata_var = True
        hata = "Email adresleriniz uyuşmuyor!"
        return render_template("kayit.html", hata_var=hata_var, hata=hata)

    # şifrelerin uyuşup uyuşmadığını kontrol eder uyuşmazsa hata mesajını kayıt ekranında gösterir
    elif sifre != sifre2:
        hata_var = True
        hata = "Şifreleriniz uyuşmuyor!"
        return render_template("kayit.html", hata_var=hata_var, hata=hata)

    # kullanıcı bilgilerini dosyaya kaydedip giriş yapılması için giriş sayfasına yönlendirir
    else:
        kullanici_bilgileri = [yetki, adi, soyadi, dogumtarihi, telefon, email, sifre]

        with open('kullanici_bilgileri.txt', 'a') as f:
            f.write('\n'.join(kullanici_bilgileri))
            f.write("\n")

        hata_var = False
        mesaj = "Hesabınız başarıyla oluşturuldu! Lütfen giriş yapın!"

        return render_template("login.html", hata_var=hata_var, mesaj=mesaj)


# giriş bilgilerini kontrol eder uyuşmazsa hata mesajını giriş ekranında gösterir
@app.route('/kontrol', methods=["GET", "POST"])
def kontrol():
    yetki = request.form["yetki"]
    email = request.form["email"]
    sifre = request.form["sifre"]
    basarili = False

    with open('kullanici_bilgileri.txt', 'r') as f:
        bilgiler = f.readlines()
        print(bilgiler)

    yeni_bilgiler = []

    for i in bilgiler:
        line = i.strip('\n')
        yeni_bilgiler.append(line)

    for x in range(0, len(yeni_bilgiler), 7):
        print(x)

        # kullanıcının bilgilerini ve erişim yetkisini doğrula
        if email == yeni_bilgiler[x + 5] and sifre == yeni_bilgiler[x + 6] and yetki == yeni_bilgiler[x]:
            basarili = True
            return render_template("anasayfa.html")

    # başarısız olursa hata mesajını göster
    if basarili is False:
        hatamesaji = "Kullanıcı adı ya da şifre hatalı!"

        return render_template("login.html", hatamesaji=hatamesaji, basarili=basarili)


# siteden çıkış yaparak giriş sayfasını yükler
@app.route('/cikisyap', methods=["GET", "POST"])
def cikisyap():
    return render_template("login.html")


# site duyurularını yükler ve gösterir
@app.route('/duyurular', methods=["GET", "POST"])
def duyurular():
    return render_template("duyurular.html")


# main fonksiyonu uygulamanın çalışmaya başladığı yer
if __name__ == '__main__':
    app.run(host='localhost', debug=True, threaded=True)
