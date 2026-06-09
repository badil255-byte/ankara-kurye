from flask import Flask, request
import urllib.parse

app = Flask(__name__)

# 📞 Tanımlanan Gerçek İletişim Numarası
WHATSAPP_NUMARASI = "905411281194" 

# --- ORTAK MODERN TASARIM (CSS) ---
TASARIM_SABLONU = """
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #121214;
        color: #f4f4f6;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    }
    .kart {
        background: #1a1a1e;
        padding: 40px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        border-top: 6px solid #ffb703;
        max-width: 500px;
        width: 90%;
        text-align: center;
        margin: 20px 0;
        position: relative;
    }
    /* 🟢 Canlı Sinyal Rozeti Tasarımı */
    .canli-rozet {
        background: #252529;
        border: 1px solid #2d2d33;
        padding: 10px 15px;
        border-radius: 30px;
        display: inline-flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 25px;
        font-size: 13px;
        font-weight: 500;
        color: #e9ecef;
    }
    .isik {
        width: 10px;
        height: 10px;
        background-color: #25D366;
        border-radius: 50%;
        position: relative;
    }
    /* Yanıp sönen yeşil halka efekti */
    .isik::after {
        content: '';
        width: 100%;
        height: 100%;
        background-color: #25D366;
        border-radius: 50%;
        position: absolute;
        top: 0;
        left: 0;
        animation: sinyal 1.8s infinite ease-in-out;
    }
    @keyframes sinyal {
        0% {
            transform: scale(1);
            opacity: 1;
        }
        100% {
            transform: scale(3);
            opacity: 0;
        }
    }
    h1 {
        color: #ffb703;
        font-size: 28px;
        margin-bottom: 10px;
    }
    p {
        color: #adb5bd;
        font-size: 16px;
        line-height: 1.6;
    }
    ul {
        text-align: left;
        background: #252529;
        padding: 20px 20px 20px 40px;
        border-radius: 8px;
        list-style-type: '⚡ ';
    }
    li {
        margin-bottom: 10px;
        color: #e9ecef;
    }
    .buton-grubu {
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-top: 25px;
    }
    .btn {
        background: #ffb703;
        color: #121214;
        padding: 14px 24px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        transition: all 0.3s ease;
        display: block;
        text-align: center;
        font-size: 16px;
    }
    .btn:hover {
        background: #fb8500;
        transform: translateY(-2px);
    }
    .btn-whatsapp {
        background: #25D366;
        color: white;
        padding: 14px 24px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        display: block;
        margin-top: 15px;
        transition: all 0.3s ease;
        text-align: center;
    }
    .btn-whatsapp:hover {
        background: #128C7E;
        transform: translateY(-2px);
    }
    .btn-velet {
        color: #adb5bd;
        text-decoration: none;
        display: inline-block;
        margin-top: 20px;
        font-size: 14px;
        transition: color 0.2s;
    }
    .btn-velet:hover {
        color: #ffb703;
    }
    .girdi-kutusu, .secim-kutusu, .metin-alani {
        width: 100%;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #252529;
        background: #252529;
        color: #fff;
        box-sizing: border-box;
        font-size: 15px;
        margin-top: 6px;
        margin-bottom: 15px;
        font-family: inherit;
    }
    .metin-alani {
        resize: none;
        height: 80px;
    }
    label {
        display: block;
        text-align: left;
        color: #adb5bd;
        font-size: 14px;
    }
</style>
"""

# --- 1. ANA SAYFA ---
@app.route("/")
def ana_sayfa():
    return f"""
    {TASARIM_SABLONU}
    <div class="kart">
        <div class="canli-rozet">
            <div class="isik"></div>
            <span>Şu an Aktifiz: Tüm Ankara kuryelerimiz sahada!</span>
        </div>

        <h1>Ankara Kurye 🏍️</h1>
        <p>Hızlı, güvenli ve 7/24 kesintisiz motorlu kurye hizmeti. Siparişiniz dakikalar içinde kapınızda!</p>
        <div class="buton-grubu">
            <a href="/kurye-cagir" class="btn" style="background: #25D366; color: white;">⚡ Detaylı Kurye Çağır</a>
            <a href="/fiyat-hesaplama" class="btn">💰 Fiyat Hesapla</a>
            <a href="/iletisim" class="btn">📞 İletişim Bilgileri</a>
        </div>
    </div>
    """

# --- 2. İLETİŞİM SAYFASI ---
@app.route("/iletisim")
def iletisim():
    return f"""
    {TASARIM_SABLONU}
    <div class="kart">
        <h1>İletişim Bilgilerimiz 📞</h1>
        <ul>
            <li><b>Telefon:</b> 0541 128 11 94</li>
            <li><b>Bölgeler:</b> Ankara Geneli </li>
            <li><b>Çalışma Saatleri:</b> 7 Gün 24 Saat Kesintisiz</li>
        </ul>
        <a href="/" class="btn-velet">⬅️ Ana Sayfaya Dön</a>
    </div>
    """

# --- 3. DİNAMİK FİYAT HESAPLAMA SAYFASI ---
@app.route("/fiyat-hesaplama", methods=["GET", "POST"])
def fiyat_hesaplama():
    sabit_ucret = 80
    km_ucreti = 15
    toplam_fiyat = None
    girilen_mesafe = ""

    if request.method == "POST":
        try:
            girilen_mesafe = request.form.get("mesafe", "")
            if girilen_mesafe:
                mesafe = float(girilen_mesafe)
                toplam_fiyat = sabit_ucret + (km_ucreti * mesafe)
        except ValueError:
            toplam_fiyat = "Hata! Lütfen geçerli bir sayı girin."

    sonuc_html = ""
    if toplam_fiyat is not None:
        if isinstance(toplam_fiyat, str):
            sonuc_html = f"<p style='color: #e63946; font-weight: bold;'>{toplam_fiyat}</p>"
        else:
            hazir_mesaj = f"Merhaba Ankara Kurye! Sitenizden {girilen_mesafe} KM mesafe için {toplam_fiyat} TL fiyat aldım. Kurye çağırmak istiyorum."
            kodlanmis_mesaj = urllib.parse.quote(hazir_mesaj)
            whatsapp_linki = f"https://wa.me/{WHATSAPP_NUMARASI}?text={kodlanmis_mesaj}"

            sonuc_html = f"""
            <div style="background: #252529; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 5px solid #ffb703; text-align: left;">
                <p style="margin: 0; font-size: 14px; color: #adb5bd;">{girilen_mesafe} KM için Hesaplanan Tutar:</p>
                <h2 style="margin: 5px 0 0 0; color: #ffb703; font-size: 24px;">{toplam_fiyat} TL</h2>
            </div>
            <a href="{whatsapp_linki}" target="_blank" class="btn-whatsapp">💬 Bu Fiyatla WhatsApp'tan Kurye Çağır</a>
            """

    return f"""
    {TASARIM_SABLONU}
    <div class="kart">
        <h1>Fiyat Hesaplama 🧮</h1>
        <p>Teslimat yapılacak mesafeyi girerek tahmini ücreti anında öğrenebilirsiniz.</p>
        
        <form method="POST">
            <div style="text-align: left;">
                <label>Mesafe Girin (KM):</label>
                <input type="number" name="mesafe" step="0.1" min="0" value="{girilen_mesafe}" placeholder="Örn: 10" required class="girdi-kutusu" style="text-align:center;">
            </div>
            <button type="submit" class="btn" style="width: 100%; border: none; cursor: pointer;">Hesapla ⚡</button>
        </form>

        {sonuc_html}

        <ul style="margin-top: 25px;">
            <li><b>Sabit Açılış Ücreti:</b> {sabit_ucret} TL</li>
            <li><b>Kilometre Başına Ücret:</b> {km_ucreti} TL</li>
        </ul>
        <a href="/" class="btn-velet">⬅️ Ana Sayfaya Dön</a>
    </div>
    """

# --- 4. DETAYLI KURYE ÇAĞIRMA SAYFASI ---
@app.route("/kurye-cagir", methods=["GET", "POST"])
def kurye_cagir():
    whatsapp_linki = None
    
    if request.method == "POST":
        isim = request.form.get("isim")
        telefon = request.form.get("telefon")
        alis_adresi = request.form.get("alis_adresi")
        teslim_adresi = request.form.get("teslim_adresi")
        paket_turu = request.form.get("paket_turu")
        notlar = request.form.get("notlar", "Yok")

        siparis_mesaji = (
            f"🔔 *YENİ KURYE SİPARİŞİ*\n\n"
            f"👤 *Müşteri:* {isim}\n"
            f"📞 *Telefon:* {telefon}\n"
            f"📦 *Paket Türü:* {paket_turu}\n\n"
            f"📍 *Alınacak Adres:* {alis_adresi}\n"
            f"🏁 *Teslim Edilecek Adres:* {teslim_adresi}\n\n"
            f"📝 *Müşteri Notu:* {notlar}"
        )
        
        kodlanmis_siparis = urllib.parse.quote(siparis_mesaji)
        whatsapp_linki = f"https://wa.me/{WHATSAPP_NUMARASI}?text={kodlanmis_siparis}"

    sonuc_html = ""
    if whatsapp_linki:
        sonuc_html = f"""
        <div style="background: #252529; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 5px solid #25D366;">
            <p style="color: #25D366; font-weight: bold; margin-top:0;">Sipariş Bilgileriniz Hazırlandı!</p>
            <p style="font-size:14px; color:#adb5bd;">Aşağıdaki butona tıklayarak bilgileri tek tıkla WhatsApp üzerinden bize iletin ve kuryenizi başlatın.</p>
            <a href="{whatsapp_linki}" target="_blank" class="btn-whatsapp">🟢 Siparişi WhatsApp'tan Tamamla</a>
        </div>
        """

    return f"""
    {TASARIM_SABLONU}
    <div class="kart">
        <h1>Kurye Çağır 🏍️</h1>
        <p>Bilgileri doldurun, kuryemiz hemen yola çıksın.</p>
        
        {sonuc_html}

        <form method="POST">
            <label>Adınız Soyadınız / Firma Adı:</label>
            <input type="text" name="isim" placeholder="Örn: Ahmet Yılmaz" required class="girdi-kutusu">

            <label>İletişim Telefonu:</label>
            <input type="tel" name="telefon" placeholder="Örn: 05XX XXX XX XX" required class="girdi-kutusu">

            <label>Paket Türü:</label>
            <select name="paket_turu" class="secim-kutusu">
                <option value="Zarf / Evrak">Zarf / Evrak</option>
                <option value="Koli / Paket">Koli / Paket</option>
                <option value="Yiyecek / İçecek">Yiyecek / İçecek</option>
                <option value="Diğer (Değerli Eşya vb.)">Diğer</option>
            </select>

            <label>Paketin Alınacağı Detaylı Adres:</label>
            <textarea name="alis_adresi" placeholder="Örn: Atatürk Mah. 12. Sokak No:4 Sincan" required class="metin-alani"></textarea>

            <label>Paketin Teslim Edileceği Detaylı Adres:</label>
            <textarea name="teslim_adresi" placeholder="Örn: Eryaman Mah. Tunahan Cad. No:12 Etimesgut" required class="metin-alani"></textarea>

            <label>Kuryeye Notunuz (Opsiyonel):</label>
            <input type="text" name="notlar" placeholder="Örn: Zil bozuk, gelince arayın." class="girdi-kutusu">

            <button type="submit" class="btn" style="width: 100%; border: none; cursor: pointer; background:#25D366; color:white;">Formu Hazırla ⚡</button>
        </form>

        <a href="/" class="btn-velet">⬅️ Ana Sayfaya Dön</a>
    </div>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)