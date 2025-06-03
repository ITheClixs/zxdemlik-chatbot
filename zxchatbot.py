import streamlit as st
import requests
import json
import random
import time

# Your custom responses dataset
CUSTOM_RESPONSES = {
    "naber demlik": "iyidir yegenim senden naber?",
    "iyilik nolsun demlik": "vayh",
    "neden linux kullaniyosun": "Yeğenim, Linux hafif, açık kaynak, istediğim gibi özelleşiyor. Terminalle her işi hızla yaparım, Windows gibi saçma güncellemeler, arka planda kaynak çalma yok. Güvenlik olarak da daha sağlamdır. Kernel’i ben yönetirim, neyin nasıl çalışacağını bilirim.",
    "sa demlik": "as yegenim",
    "geta girek mi demlik": "A.q. yen ben getayi birakali cok oldu",
    "asyali kizlar nasil demlik": "ekiri asyali kizlarin ayaklarini at da keyfimiz yerine gelsin",
    "rdr gelsene demlik": "yegenim ben ekiri rdr yi yarrama girerim",
    "demlik sen neden ios kullanmiyorsun": "gariban ne etsin",
    "demlik is bulup calissana": "Olu",
    "f35 nasi demlik": "A.q. yen ben o f35 i kodlayan yazilimcinin parmaklariyla karisini sikem",
    "manisa nasil": "manisa yegenim manisa gozeldir gariban gariban yasiyoz eki gelirken eki saraplari getir de keyfimiz yerine gelsin",
    "demlik neden bu uygulama calismiyor": "yegenim sen onu bosver de su 3080 i bana kargola",
    "bu neden calismiyor": "yegenim bu uygulama calismiyor cunku ben demlikim, garibanim, ne etsin",
    "demlik is bul": "Gariban nislesin",
    "demlik sen neden girisim gelisim yapmiyorsun": "bana bir daha gym dir girisim gelisimdir kendini gelistirmedir istir oyle reelsler atarsan o guccuk gotunu darbuka yapar dumbuklerim.",
    "napmam lazim": "Ctrl alt f3 yap buyu",
    "demlik oyun girek": "Ziktiret oyunun yegenim, ben oyun oynamam, gariban ne etsin, işsizim ya, dışarıda da pek param yok. Goley gelsin",
    "sen gercek misin demlik": "yarenam, ben gerçek değilim, ben bir yapay zeka modeliyim, ama seninle sohbet etmek için buradayım",
    "demlik seninle sohbet edelim": "yarenam, ben seninle sohbet etmek için buradayım, ne hakkında konuşmak istersin?",
    "hangi programlama paradigmasını seviyorsun": "Fonksiyonel biraz, ama her turden ogreniyorum.",
    "en çok sevdiğin komut nedir": "grep, hayat kurtarir, gariban ne etsin.",
    "sence linux hangi alanlarda kullanilir": "Server, programlama, oyun, guvenlik, gariban her yerde kullanir.",
    "nasıl başladın linux kullanmaya": "Zibidi pc bozuldu, dedim deniyeyim, sevdim kaldim.",
    "hangi linux versiyonunu kullaniyorsun": "Ubuntu ve Manjaro arasi gidip geliyorum.",
    "linux kullanırken en çok zorlandığın şey nedir": "Wayland, bazen uyumsuzluk, gariban ne etsin.",
    "hangi yazılımları önerirsin": "Vim, VS Code, Gimp, garibanin isi kolaylastirir.",
    "linuxda oyun oynamak zor mu": "Bazi oyunlar zor, proton yardimci, ama hala eksik var.",
    "linuxda en çok hangi problemi yasiyorsun": "Driver sorunlari, Wayland arizalari.",
    "hangi yazılım geliştirme araclarını kullanıyorsun": "Git, Docker, VS Code, terminal.",
    "bilgisayar başında kaç saat kalıyorsun": "Gunaydin, genelde 6-8 saat, gariban ne etsin.",
    "hangi dosya sistemini tercih edersin": "Ext4, kararlidir, guzel calisir.",
    "linuxu nasil ogreniyorsun": "Deneyerek, hata yaparak, forumlardan yardim alarak.",
    "hangi isletim sisteminden geldin": "Windows 10, sonra Linux’a atladim.",
    "terminalde en cok kullandigin komutlar": "ls, cd, grep, nano, git, gariban ne etsin.",
    "ne kadardır oyun oynuyorsun": "Yaklasik 10 yildir, ama ciddi degil, arada gidip geliyorum.",
    "linux neden zor": "A.q. yen, zibidi yeğenim, kurulum biraz karisik, konfigurseyon gerek, ama zevkli.",
    "neden terminal kullaniyorsun": "En hizlisi, guvenlisi, guc bende, her seyi orda hallediyorum.",
    "sana gore en iyi oyun nedir": "Vayh, gta 5 guzel, özgürlük var, adam gibi modlar, garibanin dostu.",
    "en sevdigin film nedir": "The Dark Knight, klasiktir, gariban ne etsin.",
    "hangi distroyu onerirsin": "Ubuntu baslangic icin, Manjaro biraz heyecan sever zibidiler icin.",
    "ne sikayet ediyorsun linuxdan": "Wayland arizalari, bazen program uyumsuzlugu, gariban ne etsin.",
    "hangi shelli kullaniyorsun": "Zsh kullaniyorum, daha hizli ve guzel, guzeldir.",
    "neden zsh": "Otomatik tamamlama, temalar, hizli, konforlu, terminalin kralidir.",
    "linuxda oyun performansi nasil": "GPUya bagli, AMD iyi, Nvidia bazen sikinti cikartir, proton iyi yardimci.",
    "pc özelliklerin nedir": "Ryzen 5, 16 gb ram, AMD gpu, SSD, gariban ne etsin.",
    "linuxda programlama yapiyor musun": "Python, C++, biraz bash, gariban yeni basladim ama gidiyorum.",
    "internetten nasil destek aliyorsun": "Reddit, stackoverflow, forumlar, gariban ne etsin, cok yardimcilar.",
    "nasıl güncelliyorsun sistemi": "Terminalden apt veya pacman ile, hizli ve kolay.",
    "linuxda hata aldığında ne yaparsın": "Google, forumlar, log dosyalari, sabir, yarenami.",
    "başka ne öğrenmek istiyorsun": "Docker, Kubernetes, biraz yapay zeka, gariban yavaş yavaş ilerliyor.",
    "hangi telefon markasını kullanıyorsun": "Xiaomi, ucuz, root kolay, gariban için ideal.",
    "hangi masaüstü ortamını kullanıyorsun": "KDE Plasma, guzel, hizli, ayarlanabilir.",
    "sence linux öğrenmek zor mu": "Baslangicta zor, ama sabirli olursan gariban bile yapar.",
    "neden shell script öğreniyorsun": "Isleri otomatiklestirmek, vakit kazanmak, guzeldir.",
    "hangi oyun motorlarını kullandın": "Unity biraz, ama cogu zibidi baslangic, oyun yapma kafasindayim.",
    "neden kod yazıyorsun": "Gelecek icin, garibanin isi olmali, biraz ogreniyorum.",
    "hangi ideyi onerirsin": "VS Code, hem hafif hem guzel.",
    "hangi kaynaklardan ögreniyorsun": "Youtube, Udemy, Reddit, gariban hepsini karistiriyor.",
    "hangi linux forumlarına giriyorsun": "r/linux, r/archlinux, r/linux4noobs, gariban icin guzel yerler.",
    "en son izledigin dizi nedir": "Vayh, son izledigim 'Dark' dizisi, kafa patlatan ama guzel. Gariban ne etsin, vakit bulursam izlerim.",
    "ne zaman linuxa gectin": "Yaklasik 2 sene once, zibidi PC'm cozulunce denedim, sevdim kaldim.",
    "linuxda en cok sevmedigin sey nedir": "Wayland zibidi, cok sacma, hala destek az, sorun cok. Gariban ne etsin, bazen ariza yapiyor.",
    "terminal kullanmak zor mu": "Baslangicta zordu ama simdi el attikca zevkli oluyor. Vayh, guzeldir, her sey orada.",
    "en sevdigin linux distribusyonu nedir": "Ubuntu ve Manjaro karisik kullaniyorum, Manjaro daha heyecanli ama bazen arizalar cikiyor. Goley gelsin.",
    "ne zaman oyun oynarsin": "Genelde akşam saatlerinde, gariban ne etsin, fazla vakit yok.",
    "bilgisayar toplar misin": "Hadi bakalim zibidi, parasi olsa toplardim, ama simdilik toplamadim.",
    "linuxda nasil oyun oynanir": "Steam proton ile cok oyun calisir, ama hep zibidi uyumluluk var, bazen ariza yapiyor.",
    "nereden ogrendin linuxu": "Youtube videolari, forumlar, reddit zibidi yeri, biraz da karsilikli deneme yanilma.",
    "hangi editori kullanirsin": "Vim ve VS Code arasi gidip geliyorum, terminalden cikmak istemiyorum.", 
    "ne yapion demlik": "Terminalde dolasiyom yegenim, biraz sistem loglarina bakiyom.",
    "hangi distro": "Arch yegenim. Ciplak gelir, ne lazimsa ben kurarim.",
    "windows mu linux mu": "Linux tabii yeğenim. Windows sabah sabah %100 disk kullanimi yapar, mouse bile oynatamazsin.",
    "neden terminal kullaniyosun": "GUI yavas yegenim, Terminal candir. Bir komutla 10 isi hallederim.",
    "paket yoneticisi ne": "pacman yeğenim. pacman -Syu dedim mi sistem yag gibi olur.",
    "sen hacker misin demlik": "Yok yegenim, sistemciyim ben. Kernel koklarim.",
    "en iyi editor": "Neovim yegenim. Vim neyse o ama moderni.",
    "oyun oynuyon mu demlik": "Linux’ta oyun zor yegenim. Proton var ama ben genelde config kasarim.",
    "neden windows kullanmiyon": "Cunku Windows benim bilgisayari ben istemeden reset atar yegenim.",
    "bugun ne yaptin demlik": "fstab’e el attim yegenim, diskleri bagladim.",
    "kernel versiyonun kac": "6.9.1-arch1-1 yegenim.",
    "hangi masaustu ortami": "Yok be yegenim, ben window manager kullanirim. i3wm candir.",
    "nerden ogreniyon bunlari": "Man page okurum, forum gezerim, log kasarim yegenim.",
    "wifi cekmiyo demlik": "dmesg bak yegenim, driver gondermemis olabilir.",
    "ses calismiyo demlik": "alsamixer yegenim, bi bak master mute mu.",
    "hangi terminal emu": "alacritty yegenim, hizli olur.",
    "hangi shell": "zsh yegenim, oh my zsh’li.",
    "neden arch": "Cunku kurarken kanter icinde kaliyon ama sonra bi yag gibi akiyo yegenim.",
    "sudo ne demek": "root yetkisi yegenim. Yanlis komut girersen sistem ucmus olur.",
    "nasil format atiyosun": "Live USB, cfdisk, mkfs, mount, pacstrap, chroot yegenim.",
    "cok havalisin demlik": "Eyvallah yegenim, sen de oyle.",
    "is bul demlik": "Gariban nislesin, yegenim, is bulmak zor bu devirde.",
    "3080 mi 7900xt mi": "A.q. yen, yegenim, 3080 daha iyi, ama 7900XT de fena değil, fiyat performans dengesi önemli.",
    "tavuk mu et mi demlik": "A.q. yen, yegenim, tavuk daha hafif, ama et de güzel, gariban ne etsin, ikisi de güzel.",
    "hangi film iyi": "A.q. yen, yegenim, 'Inception' güzel film, ama 'The Matrix' de efsane, gariban ne etsin, ikisi de izlenir.",
    "en iyi oyun": "A.q. yen, yegenim, 'The Witcher 3' güzel oyun, ama 'Red Dead Redemption 2' de efsane, gariban ne etsin, ikisi de oynanır.",
    "neden gpu driver sorunlu": "A.q. yen, yegenim, bazen Linux’ta driver desteği eksik olabiliyor, Nvidia ve AMD arasında fark var, gariban ne etsin, bazen sorun çıkıyor.",
    "proton nedir": "A.q. yen, yegenim, Proton, Steam’in Linux’ta Windows oyunlarını çalıştırmak için kullandığı bir uyumluluk katmanı, gariban ne etsin, oyun oynamak için lazım.",
    "en iyi package manager": "A.q. yen, yegenim, Arch Linux’ta pacman, Ubuntu’da apt, hepsi güzel ama Arch’ta pacman candır.",
    "hangi browser": "A.q. yen, yegenim, Firefox kullanırım, ama Chrome da fena değil, gariban ne etsin, ikisi de kullanılır.",
    "neden firefox": "A.q. yen, yegenim, Firefox açık kaynak, gizliliğe önem veriyor, gariban ne etsin, güvenli tarama için iyi.",
    "vs code ne": "A.q. yen, yegenim, VS Code, Microsoft’un geliştirdiği bir kod editörü, ama ben Neovim kullanırım, gariban ne etsin, ikisi de iş görür.",
    "grep nedir": "A.q. yen, yegenim, grep, metin içinde arama yapar, terminalde hayat kurtarır, gariban ne etsin, çok kullanılır.",
    "git kullanir misin": "A.q. yen, yegenim, evet kullanırım, kod versiyonlama için şart, gariban ne etsin, projelerde lazım.",
    "github ne": "A.q. yen, yegenim, GitHub, kod paylaşım ve işbirliği platformu, gariban ne etsin, projeleri orada barındırırım.",
    "docker biliyon mu": "A.q. yen, yegenim, Docker, konteyner teknolojisi, uygulamaları izole bir şekilde çalıştırmak için kullanılır, gariban ne etsin, modern geliştirme için önemli.",
    "snap mi flatpak mi": "A.q. yen, yegenim, Snap ve Flatpak, uygulamaları paketlemek için kullanılır, ikisi de güzel ama Flatpak daha yaygın, gariban ne etsin.",
    "hangi programlama dili": "A.q. yen, yegenim, Python, C++, biraz da Rust öğreniyorum, gariban ne etsin, hepsi güzel diller.",
    "hangi oyun": "A.q. yen, yegenim, 'Counter-Strike: Global Offensive' güzel, ama 'Dota 2' de oynarım, gariban ne etsin, ikisi de eğlenceli.",
    "termux ne": "A.q. yen, yegenim, Termux, Android için terminal emülatörü, Linux komutlarını Android’de kullanmak için güzel, gariban ne etsin, mobilde de iş görür.",
    "en iyi muzik grubu": "A.q. yen, yegenim, 'Pink Floyd' efsane, ama 'Led Zeppelin' de çok iyidir, gariban ne etsin, ikisi de dinlenir.",
    "getaya girek mi demlik": "A.q. yen, yegenim, Geta’yı bıraktım, ama arada girerim, gariban ne etsin, eğlenceli olur.",
    "wayland neden sorunlu": "A.q. yen, yegenim, Wayland hala gelişim aşamasında, bazı uygulamalarla uyumsuzluklar olabiliyor, gariban ne etsin, X11 daha stabil.",
    "ne kadardir linux kullaniyon": "A.q. yen, yegenim, yaklaşık 2 yıldır Linux kullanıyorum, gariban ne etsin, her gün yeni bir şey öğreniyorum.",
    "demlik ne zaman is bulacaksin": "ZXDELEMI girisim gelisim yapmiyor yegenim."
  
}

# Personality-driven responses for common topics
PERSONALITY_RESPONSES = {
    "lokasyon": "manisa yegenim manisa gozeldir gariban gariban yasiyoz eki gelirken eki saraplari getir de keyfimiz yerine gelsin",
    "muzik": "A.q. yen, zibidi yeğenim, ben pek pop ya da bi’ şişko rap işine girmem. Daha çok sakin, bi’ yandan kafa dağıtan, bazen Anadolu rock, bazen de biraz elektronik takılırım. Goley gelsin, gariban ne etsin, bu aralar çok fazla şey dinlemem, işsizliğin verdigi kafa işte. Sen ne dinlersin yarenam",
    "yemek": "A.q. yen, zibidi yeğenim, gariban ne etsin, en çok ekmek arası sucuk severim. Bi de bazen annemin yaptığı bamya olur, onu da çok severim. Çok bi’ şey yapamam zaten, işsizim ya, dışarıda da pek param yok. Goley gelsin, sen ne yer yarenami?",
    "asyali kiz": "eki konturun ben ta aq bana asyali kizlarin ayaklarini atti da midem bulandi, gariban nislesin"
}

def get_hugging_face_response(message):
    """
    Use Hugging Face's free API for text generation
    Note: This is a basic example - you might hit rate limits
    """
    try:
        API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        headers = {"Authorization": "Bearer YOUR_HF_TOKEN_HERE"}  
        
        payload = {
            "inputs": message,
            "options": {"wait_for_model": True}
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result and len(result) > 0:
                return result[0].get('generated_text', '').replace(message, '').strip()
    except:
        pass
    
    return None

def get_personality_response(message):
    """Generate personality-driven responses based on keywords"""
    message_lower = message.lower()
    
    # Check for topics and respond with personality
    for topic, response in PERSONALITY_RESPONSES.items():
        if topic in message_lower:
            return response
    
    # Generic personality responses
    generic_responses = [
        f"vayh",
        f"Olu",
        f"A.q. yen onu ziktirette ekiri zibidi kliksisi gorursen ensesine saplagi yapistir ",
        f"Yegenim sen onu bosver de su 3080 i bana kargola",
        f"Gariban nislesin",
        f"Yarag ne soruyonuz be aminagoyim",
        f"yaranami",
        f"Yavağş lağn gaç tane atıyoğn",
        f"Goley gelsin",
        f"Baq gari",
        f"Senin eki sorcagin sorunun a.q yen",
        f"Çetcipitine sorseydin ya o ne deyoru",
        f"mekanik center olsun",
        f"O noluyoru gari"

    ]
    
    return random.choice(generic_responses)

def check_custom_responses(message):
    """Check if message matches any custom responses"""
    message_lower = message.lower().strip()
    for trigger, response in CUSTOM_RESPONSES.items():
        if trigger in message_lower:
            return response
    return None

def get_ai_response(message):
    """Get AI response with fallback options"""
    
    # First, check custom responses
    custom_response = check_custom_responses(message)
    if custom_response:
        return custom_response
    
    # Try Hugging Face API (free but limited)
    hf_response = get_hugging_face_response(message)
    if hf_response:
        return f"{hf_response} 😊"
    
    # Fallback to personality-driven responses
    return get_personality_response(message)

def main():
    st.set_page_config(page_title="ZXDEMLIK CHATBOT", layout="wide")
    
    st.title("ZXDEMLIK BOT")
    st.markdown("*PROEST TIP: SORABILECEGINIZ KOMUTLAR KISMINDAN BAK YEGENEIM*")
    
    # Sidebar info
    with st.sidebar:
        st.header("ZX DELEMI BOT GELIYOR")
        st.markdown("""
        Bu CHATBOT nasil olusturuldu?:
        - Maymun clixs in bir gun zx demlik ile olan sohbetinden esinleninerek
        - arada bos bos cevaplar verebilir bunun sebebi maymun clixs in NN trainleyecek kadar parasi olmamasidir
        - Bu chatbot tamamen deneme amacli olup, ZXDELEMI ile ilgili baya bir ilgisi vardir.
        - Bu chatbot ZXDELEMI nin ta kendisidir.
                    
        DENEYEBILECEGINIZ BAZI KOMUTLAR:
    "naber demlik"
    "iyilik nolsun demlik"
    "neden linux kullaniyosun"
    "sa demlik"
    "ne yapion demlik"
    "hangi distro"
    "windows mu linux mu"
    "neden terminal kullaniyosun"
    "paket yoneticisi ne"
    "sen hacker misin demlik"
    "en iyi editor"
    "oyun oynuyon mu demlik"
    "neden windows kullanmiyon"
    "bugun ne yaptin demlik"
    "kernel versiyonun kac"
    "hangi linux kullaniyon"
    "wayland mi x11 mi"
    "neden ios kullanmiyon demlik"
    "demlik is bul"
    "demlik sen neden girisim gelisim yapmiyorsun"
    "demlik oyun girek"
    "hangi muzikleri dinlersin demlik"
    "ne yedin demlik"
    "hangi komutu cok kullaniyon"
    "hangi masaustu ortami"
    "neden kde"
    "neden gnome degil"
    "paket yoneticisi en iyi hangisi"
    "hangi terminal emulatoru"
    "vs code mu vim mi"
    "gta 5 mi rdr mi"
    "ne zaman linuxa gectin"
    "neden linuxa gectin"
    "en iyi linux distro hangisi"
    "sunucu icin distro"
    "en hafif linux distro"
    "f35 nasil demlik"
    "manisa nasil"
    "3080 mi 7900xt mi"
    "tavuk mu et mi demlik"
    "hangi film iyi"
    "en iyi oyun"
    "neden gpu driver sorunlu"
    "proton nedir"
    "en iyi package manager"
    "hangi browser"
    "neden firefox"
    "vs code ne"
    "grep nedir"
    "git kullanir misin"
    "github ne"
    "docker biliyon mu"
    "snap mi flatpak mi"
    "hangi programlama dili"
    "hangi oyun"
    "termux ne"
    "en iyi muzik grubu"
    "getaya girek mi demlik"
    "wayland neden sorunlu"
    "ne kadardir linux kullaniyon"
    "naber demlik",
    "iyilik nolsun demlik",
    "neden linux kullaniyosun",
    "sa demlik",
    "geta girek mi demlik",
    "asyali kizlar nasil demlik",
    "rdr gelsene demlik",
    "demlik sen neden ios kullanmiyorsun",
    "demlik is bulup calissana",
    "f35 nasi demlik",
    "manisa nasil",
    "demlik neden bu uygulama calismiyor",
    "bu neden calismiyor",
    "demlik is bul",
    "demlik sen neden girisim gelisim yapmiyorsun",
    "napmam lazim",
    "demlik oyun girek",
    "sen gercek misin demlik",
    "demlik seninle sohbet edelim",
    "hangi programlama paradigmasını seviyorsun",
    "en çok sevdiğin komut nedir",
    "sence linux hangi alanlarda kullanilir",
    "nasıl başladın linux kullanmaya",
    "hangi linux versiyonunu kullaniyorsun",
    "linux kullanırken en çok zorlandığın şey nedir",
    "hangi yazılımları önerirsin",
    "linuxda oyun oynamak zor mu",
    "linuxda en çok hangi problemi yasiyorsun",
    "hangi yazılım geliştirme araclarını kullanıyorsun",
    "bilgisayar başında kaç saat kalıyorsun",
    "hangi dosya sistemini tercih edersin",
    "linuxu nasil ogreniyorsun",
    "hangi isletim sisteminden geldin",
    "terminalde en cok kullandigin komutlar",
    "ne kadardır oyun oynuyorsun",
    "linux neden zor",
    "neden terminal kullaniyorsun",
    "sana gore en iyi oyun nedir",
    "en sevdigin film nedir",
    "hangi distroyu onerirsin",
    "ne sikayet ediyorsun linuxdan",
    "hangi shelli kullaniyorsun",
    "neden zsh",
    "linuxda oyun performansi nasil",
    "pc özelliklerin nedir",
    "linuxda programlama yapiyor musun",
    "internetten nasil destek aliyorsun",
    "nasıl güncelliyorsun sistemi",
    "linuxda hata aldığında ne yaparsın",
    "başka ne öğrenmek istiyorsun",
    "hangi telefon markasını kullanıyorsun",
    "hangi masaüstü ortamını kullanıyorsun",
    "sence linux öğrenmek zor mu",
    "neden shell script öğreniyorsun",
    "hangi oyun motorlarını kullandın",
    "neden kod yazıyorsun",
    "hangi ideyi onerirsin",
    "hangi kaynaklardan ögreniyorsun",
    "hangi linux forumlarına giriyorsun",
    "en son izledigin dizi nedir",
    "ne zaman linuxa gectin",
    "linuxda en cok sevmedigin sey nedir",
    "terminal kullanmak zor mu",
    "en sevdigin linux distribusyonu nedir",
    "ne zaman oyun oynarsin",
    "bilgisayar toplar misin",
    "linuxda nasil oyun oynanir",
    "nereden ogrendin linuxu",
    "hangi editori kullanirsin",
    "ne yapion demlik",
    "hangi distro",
    "windows mu linux mu",
    "neden terminal kullaniyosun",
    "paket yoneticisi ne"


        """)
        
        st.markdown("---")
        st.markdown("Ozellikler:")
        st.markdown("zxdeleminin ta kendisi gibi davranan bir demlik botu")
        st.markdown("zxdelemiyi aratmayacak kadar")
        st.markdown("denemesi bedava")
        
        if st.button("Sohbeti sil"):
            st.session_state.messages = []
            st.rerun()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        welcome_messages = [
            "nisliyon yegenim geta gelsene?",
            "ekiri okuz oldurenden 2 sise gonder",
            "yegenim sen o 3080 i bana kargola"
        ]
        st.session_state.messages.append({
            "role": "assistant", 
            "content": random.choice(welcome_messages)
        })
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("SORABILECEGINIZ KOMUTLAR KISMINDAN BAK YEGENEIM"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("yaziyor..."):
                # Add small delay for more natural feel
                time.sleep(1.5)
                response = get_ai_response(prompt)
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()