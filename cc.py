import asyncio
from telethon import TelegramClient, events
import random

# Your Telegram API credentials
api_id = 29922143  # Replace with your own API ID
api_hash = 'a3270aeee0b1cc4cee60a9f3e74e71d4'  # Replace with your own API hash

# Create the Telegram client (userbot)
client = TelegramClient("session_name", api_id, api_hash)

# Owner's user ID (only this user can approve others)
OWNER_ID = '7147401720'

# Set of approved user IDs
approved_users = set()

# Stop flag for spam
stop_spam = False

# List of gaalis
galis = [
    "Teri maa ki aakh",
    "Bhosdike",
    "Madarchod",
    "Behenchod",
    "Randi ke bacche",
    "Kutte",
    "Chutiya",
    "Gandu",
    "Teri maa ka bhosda",
    "Baap se panga"
    "Tere baap ka naala 😆",
    "Teri behen ki chatri 🌂",
    "Teri gaand mein danda 🤣",
    "Teri maa ki chut me DJ bass 🔊",
    "Tere baap ki moochon me patakha 🎇",
    "Teri behen ki sari hawa me uda dunga 🎭",
    "Teri maa ka bhosda Gol Gappa banake kha jaunga 😜",
    "Teri gaand me torch dal ke light house bana dunga 🔦",
    "Teri maa ki chut me namak daal dunga 🌊",
    "MADARCHOD TERI MAA KI CHUT ME GHUTKA KHAAKE THOOK DUNGA 🤣🤣", 
    "TERE BEHEN K CHUT ME CHAKU DAAL KAR CHUT KA KHOON KAR DUGA", 
    "TERI MAA K BHOSDE ME AEROPLANE PARK KARKE UDAAN BHAR DUGA ✈️🛫", 
    "TERI MAA KI CHUT ME SUTLI BOMB FOD DUNGA 💣",
    "TERI MAAKI CHUT ME SCOOTER DAAL DUGA👅",  
    "TERE BHAI KI CHUT ME JHAADU LAGA DUNGA", 
    "Bhadhava Maderchod Bhosadike teri bhn ko chodu chutiya gandu scammer chut kay gulaam 😡😡🥵", 
    "Sunn Scammer Mai teri ma ko chodke apna lund chusakay aur tujhe apni jhaat chatake tujhe esa bhai dunga jo meri zindagi mai baar baar choosne ke liye taiyaar hojayenge 😂🥵🤢", 
    "teri maa ki chut me nimbu ka achar daalkr chode dalunga sale scammer kay fate hue condom ki aulad 😡🥵", 
    "jhaatu scammer teri jhant mein kerosene daal kar aag laga dunga Hijde ki kaali gaand 🥵🤢", 
    "Teri Gaand Mein Kutte Ka Lund kutiya ki paidayish scammer 😡🤮", 
    "Teri Jhaatein Kaat Kar Tere Mooh Par Laga Kar Unki scam French Beard Bana Doonga", 
    "Chullu Bhar Muth Mein Doob Mar bhaadu scammer Chut Ke Pasine Main apni kaak gand chuda bhosdike", 
    "kaali gand kay fatey hue lund jhaatu scammer kaas ush din Tera baap condom use kar leta betichod 🤬🤬", 
    "scammer hathi kay lund ka bhsoda bna kar teri kaali gand mai de dunga chhipakali ki choot jesi sakal kay 🤬🖕", 
    "Randi ki Najais lode tere jese chutiya scammer randi k baccho ko bachpan mai maar dena chiye", 
    "Chipkali ki bhigi chut Choot kay baal Chipkali ke jhaat ke paseene",
    "Gote Kitne Bhi Badey Ho, Lund Ke Niche Hi Rehtein Hain",
    "chutiye behenchod lauda madarchod gaandu bhosadikey",
    "Chullu Bhar Muth Mein Doob Mar Kaali Chut Ke Safed Jhaat",
    "chut kay baal nipple ki dhaar teri gaand mai Road roller de dunga 🖕🤬",
    "Teri Gaand Mein Kutte Ka Lund 🖕 Teri Jhaatein Kaat Kar Tere Mooh Par Laga Kar Unki French Beard Bana Doonga!",
    "Phatele Nirodh Ke Natije! 😂😂",
    "Teri maa ki choot gand kay tatto teri maa ka bhosda karke uski gaand mai ping pong kar dunga",
    "GAND KII DHAAR BHOSDIKE FATEE HUE CONDOM KI NAAJAIS PAIDAISH",
    "Teri ma ka bhosda sale maderchod ki aulad 🤬",
    "madarchod chutmarke teri tatti jesi shakl pe pad dunga bhen k lode chutiye",
    "maa k lode tere jese randi k baccho ko bachpan mai maar dena chiye",
    "TERA BAAP JOHNY SINS CIRCUS KAY BHOSDE JOKER KI CHIDAAS 14 LUND KI DHAAR TERI MUMMY KI CHUT MAI 200 INCH KA LUND",
    "teri ma Randi tera baap hizda kaali gaand kay Khade baal jhaatu Randi kay chodu",
    "SALA TARI BHAN KO ROAD PA LAJA KA KA NANGA KAR KA BAACHO SA CHUD VAU",
    "teri maa k bhosde mai MDH CHANA MASALA daal k tere baap ko vo spicy bhosda khila dunga 🥵🤮",
    "GAND MAI VIMAL KI GOLI BNA KAR DE DUNGA BHENCHO TERI GAAND MAI RAILWAY STATION KA FATAK DE DUNGA 😂😂🤬🖕",
    "14 baap ki Najais olad randi kay beez chinnale",
    "TARI MAA KI HARAAMJAALE BHOSDE PE MARUNGA LAATH TO TARI MIYAA CHUDEGI DINO RAAT",
    "Teri ma ki gand me hathi ka lund dalke asa chodunga Na Bacha hojayega Johny sins ,ke lund se chudwaungu bhosdike",
    "madar chod bhosdke esa lagta h apne hii taaate kaat ke chipka diya apni shakal dekh lodee jese shakal aur gand me h aakal",
    "teri ma ki choot randi kay scammer apne baap kay rupye se Jhaat kay baal trim kra lena 😂😂🤢",
    "bhsodike mujhe ye samajh nhi aata scam Karke kya tum jese loog apni mummy ka Randi naach dekhne jaate hoi 😂😂",
    "Jitno ka tunne scam kia na sbb teri maa k bhosde mai momos daal ke tere baap ko vo spicy bhosda khila Dengey 🥵🤮",
    "ek baar tu mill gya na tere scam kay paiso se teri gaand mai ungli de dunga or teri mummy se apna lund chusa kar chod dunga usko 🖕🥵🖕🥵🖕🤬😤🤢",
    "betichod le 100 rs. lele mujhse or apni mummy ki choot dikha de 😤😤 tujhe bhaut sock hai logo kay rupye scam karne ka 🥵🖕",
    "Randi kay scammer bhenchod 🤢 sale tum scammer loog har jagah apni maa kyo chudaane aa naate ho 🥵🤬",
    "scammer randi ki olad Jhatal teri maa ka bhosda sale mia Khalifa ki najais olad 🖕🖕",
    "Jhatal si sikal kay lund ki dhaar bhenchodd or kitne logo kay rupye scam karke apni gaand mai daalta hai 🤬😡",
    "teri bhn ko chodu 🥵 scam kay Paiso se apni mummy kay lie condom khareed lie jhaatu 😂",
    "🖕Scammer maderchod teri maa ka bhosda 🤮🤢 sale 2 koodi kay lund🤬🤬",
    "TARE DADA KE MUH PE MARUNGA LAATH TO TARI MIYAA CHUDEGI DONO RAAT",
    "BAHEN KE LAWDE AWAAZ UTA AWAAZ NHI AA RAHA TARI MAA KA BHOSDA",
    "TARI MAA KA BHOSDA",
    "TARI MAA KI CHUT",
    "Tere baap ka lund ke mooch se violin bajake gali compose kar dunga",
    "Tere baap ka lund ke mooch se violin bajake gali compose kar dunga aur livestream chalu kar dunga",
    "Tere baap ka lund ke mooch se violin bajake gali compose kar dunga aur sab galiyan sunenge",
    "Tere baap ka lund ke mooch se violin bajake gali compose kar dunga bina charger ke",
    "Tere baap ka lund ke mooch se violin bajake gali compose kar dunga bina permission ke",
    "Tere baap ka lund ke mooch se violin bajake gali compose kar dunga bina reboot ke",
    "Tere baap ka lund ke mooch se violin bajake gali compose kar dunga fir usko chaat jaunga",
    "Tere baap ka lund ko Flipkart pe sale pe daal dunga",
    "Tere baap ka lund ko Flipkart pe sale pe daal dunga aur livestream chalu kar dunga",
    "Tere baap ka lund ko Flipkart pe sale pe daal dunga aur usme ad laga dunga",
    "Tere baap ka lund ko Flipkart pe sale pe daal dunga bina charger ke",
    "Tere baap ka lund ko Flipkart pe sale pe daal dunga bina data loss ke",
    "Tere baap ka lund ko Flipkart pe sale pe daal dunga bina permission ke",
    "Tere baap ka lund ko Flipkart pe sale pe daal dunga jise sab report karenge",
    "Tere baap ka lund ko OnlyFans pe daal dunga",
    "Tere baap ka lund ko OnlyFans pe daal dunga aur livestream chalu kar dunga",
    "Tere baap ka lund ko OnlyFans pe daal dunga bina permission ke",
    "Tere baap ka lund ko OnlyFans pe daal dunga bina reboot ke",
    "Tere baap ka lund ko OnlyFans pe daal dunga fir usko chaat jaunga",
    "Tere baap ka lund ko OnlyFans pe daal dunga jise sab report karenge",
    "Tere baap ka lund me AirPods daal ke gaane chala dunga",
    "Tere baap ka lund me AirPods daal ke gaane chala dunga aur livestream chalu kar dunga",
    "Tere baap ka lund me AirPods daal ke gaane chala dunga aur sab galiyan sunenge",
    "Tere baap ka lund me AirPods daal ke gaane chala dunga aur usme ad laga dunga",
    "Tere baap ka lund me AirPods daal ke gaane chala dunga bina charger ke",
    "Tere baap ka lund me AirPods daal ke gaane chala dunga bina reboot ke",
    "Tere baap ka lund me AirPods daal ke gaane chala dunga fir usko chaat jaunga",
    "Tere baap ka lund me AirPods daal ke gaane chala dunga jise sab report karenge",
    "Tere baap ka lund me Bluetooth speaker daal ke gali FM chala dunga",
    "Tere baap ka lund me Bluetooth speaker daal ke gali FM chala dunga aur livestream chalu kar dunga",
    "Tere baap ka lund me Bluetooth speaker daal ke gali FM chala dunga bina charger ke",
    "Tere baap ka lund me Bluetooth speaker daal ke gali FM chala dunga bina data loss ke",
    "Tere baap ka lund me Bluetooth speaker daal ke gali FM chala dunga bina reboot ke",
    "Tere baap ka lund me Bluetooth speaker daal ke gali FM chala dunga jise sab report karenge",
    "Tere baap ka lund me DJ system daal dunga",
    "Tere baap ka lund me DJ system daal dunga aur livestream chalu kar dunga",
    "Tere baap ka lund me DJ system daal dunga aur sab galiyan sunenge",
    "Tere baap ka lund me DJ system daal dunga aur usme ad laga dunga",
    "Tere baap ka lund me DJ system daal dunga bina charger ke",
    "Tere baap ka lund me DJ system daal dunga bina data loss ke",
    "Tere baap ka lund me DJ system daal dunga bina reboot ke",
    "Tere baap ka lund me DJ system daal dunga fir usko chaat jaunga",
    "Tere baap ka lund me Discord server chala dunga bina data loss ke",
    "Tere baap ka lund me Discord server chala dunga bina permission ke",
    "Tere baap ka lund me Discord server chala dunga bina reboot ke",
    "Tere baap ka lund me Discord server chala dunga fir usko chaat jaunga",
    "Tere baap ka lund me Discord server chala dunga jise sab report karenge",
    "Tere baap ka lund me Notepad khol ke code likh dunga",
    "Tere baap ka lund me Notepad khol ke code likh dunga aur livestream chalu kar dunga",
    "Tere baap ka lund me Notepad khol ke code likh dunga bina data loss ke",
    "Tere baap ka lund me Notepad khol ke code likh dunga bina permission ke",
    "Tere baap ka lund me Notepad khol ke code likh dunga bina reboot ke",
    "Tere baap ka lund me Notepad khol ke code likh dunga fir usko chaat jaunga",
    "Tere baap ka lund me Notepad khol ke code likh dunga jise sab report karenge",
    "Tere baap ka lund me RAM stick daal dunga aur livestream chalu kar dunga",
    "Tere baap ka lund me RAM stick daal dunga aur usme ad laga dunga",
    "Tere baap ka lund me RAM stick daal dunga bina charger ke",
    "Tere baap ka lund me RAM stick daal dunga bina data loss ke",
    "Tere baap ka lund me RAM stick daal dunga bina permission ke",
    "Tere baap ka lund me RAM stick daal dunga bina reboot ke",
    "Tere baap ka lund me RAM stick daal dunga fir usko chaat jaunga",
    "Tere baap ka lund me RAM stick daal dunga jise sab report karenge",
    "Tere baap ka lund me SSD daal ke fast access kar lunga aur livestream chalu kar dunga",
    "Tere baap ka lund me SSD daal ke fast access kar lunga aur sab galiyan sunenge",
    "Tere baap ka lund me SSD daal ke fast access kar lunga bina charger ke",
    "Tere baap ka lund me SSD daal ke fast access kar lunga bina data loss ke",
    "Tere baap ka lund me SSD daal ke fast access kar lunga bina permission ke",
    "Tere baap ka lund me SSD daal ke fast access kar lunga fir usko chaat jaunga",
    "Tere baap ka lund me SSD daal ke fast access kar lunga jise sab report karenge",
    "Tere baap ka lund me firewall daal ke secure kar dunga",
    "Tere baap ka lund me firewall daal ke secure kar dunga aur livestream chalu kar dunga",
    "Tere baap ka lund me firewall daal ke secure kar dunga aur sab galiyan sunenge",
    "Tere baap ka lund me firewall daal ke secure kar dunga aur usme ad laga dunga",
    "Tere baap ka lund me firewall daal ke secure kar dunga bina charger ke",
    "Tere baap ka lund me firewall daal ke secure kar dunga bina data loss ke",
    "Tere baap ka lund me firewall daal ke secure kar dunga bina reboot ke",
    "Tere baap ka lund me firewall daal ke secure kar dunga fir usko chaat jaunga",
    "Tere baap ka lund me firewall daal ke secure kar dunga jise sab report karenge",
    "Tere baap ka lund me solar panel laga dunga aur livestream chalu kar dunga",
    "Tere baap ka lund me solar panel laga dunga bina charger ke",
    "Tere baap ka lund me solar panel laga dunga bina data loss ke",
    "Tere baap ka lund me solar panel laga dunga bina reboot ke",
    "Tere baap ka lund me spaghetti bana dunga",
    "Tere baap ka lund me spaghetti bana dunga aur livestream chalu kar dunga",
    "Tere baap ka lund me spaghetti bana dunga aur usme ad laga dunga",
    "Tere baap ka lund me spaghetti bana dunga bina charger ke",
    "Tere baap ka lund me spaghetti bana dunga bina data loss ke",
    "Tere baap ka lund me spaghetti bana dunga bina permission ke",
    "Tere baap ka lund me spaghetti bana dunga bina reboot ke",
    "Tere baap ka lund me spaghetti bana dunga fir usko chaat jaunga",
    "Tere baap ka lund me spaghetti bana dunga jise sab report ke aulad",
    "Tere baap ka lund pe GPS laga dunga bina permission ke",
    "Tere baap ka lund pe GPS laga dunga bina reboot ke",
    "Tere baap ka lund pe GPS laga dunga fir usko chaat jaunga",
    "Tere baap ka lund pe QR code chipka ke scan karwaunga aur livestream chalu kar dunga",
    "Tere baap ka lund pe QR code chipka ke scan karwaunga aur sab galiyan sunenge",
    "Tere baap ka lund pe QR code chipka ke scan karwaunga aur usme ad laga dunga",
    "Tere baap ka lund pe QR code chipka ke scan karwaunga bina charger ke",
    "Tere baap ka lund pe QR code chipka ke scan karwaunga bina data loss ke",
    "Tere baap ka lund pe QR code chipka ke scan karwaunga bina reboot ke",
    "Tere baap ka lund pe QR code chipka ke scan karwaunga fir usko chaat jaunga",
    "Tere baap ka lund pe QR code chipka ke scan karwaunga jise sab report karenge",
    "Tere baap ka lund pe barcode chipka dunga",
    "Tere baap ka lund pe barcode chipka dunga aur livestream chalu kar dunga",
    "Tere baap ka lund pe barcode chipka dunga aur sab galiyan sunenge",
    "Tere baap ka lund pe barcode chipka dunga aur usme ad laga dunga",
    "Tere baap ka lund pe barcode chipka dunga bina data loss ke",
    "Tere baap ka lund pe barcode chipka dunga bina permission ke",
    "Tere baap ka lund pe barcode chipka dunga fir usko chaat jaunga",
    "Tere baap ka lund pe barcode chipka dunga jise sab report karenge",
    "Tere baap ke mooch se violin bajake gali compose kar dunga aur livestream chalu kar dunga",
    "Tere baap ke mooch se violin bajake gali compose kar dunga aur sab galiyan sunenge",
    "Tere baap ke mooch se violin bajake gali compose kar dunga aur usme ad laga dunga",
    "Tere baap ke mooch se violin bajake gali compose kar dunga bina charger ke",
    "Tere baap ke mooch se violin bajake gali compose kar dunga bina data loss ke",
    "Tere baap ke mooch se violin bajake gali compose kar dunga bina reboot ke",
    "Tere baap ke mooch se violin bajake gali compose kar dunga fir usko chaat jaunga",
    "Tere baap ke mooch se violin bajake gali compose kar dunga jise sab report karenge",
    "Tere baap ko Flipkart pe sale pe daal dunga aur livestream chalu kar dunga",
    "Tere baap ko Flipkart pe sale pe daal dunga aur usme ad laga dunga",
    "Tere baap ko Flipkart pe sale pe daal dunga bina permission ke",
    "Tere baap ko Flipkart pe sale pe daal dunga bina reboot ke",
    "Tere baap ko Flipkart pe sale pe daal dunga fir usko chaat jaunga",
    "Tere baap ko Flipkart pe sale pe daal dunga jise sab report karenge",
    "Tere baap ko OnlyFans pe daal dunga",
    "Tere baap ko OnlyFans pe daal dunga aur livestream chalu kar dunga",
    "Tere baap ko OnlyFans pe daal dunga aur sab galiyan sunenge",
    "Tere baap ko OnlyFans pe daal dunga aur usme ad laga dunga",
    "Tere baap ko OnlyFans pe daal dunga bina charger ke",
    "Tere baap ko OnlyFans pe daal dunga bina permission ke",
    "Tere baap ko OnlyFans pe daal dunga bina reboot ke",
    "Tere baap ko OnlyFans pe daal dunga fir usko chaat jaunga",
    "Tere baap me AirPods daal ke gaane chala dunga",
    "Tere baap me AirPods daal ke gaane chala dunga aur livestream chalu kar dunga",
    "Tere baap me AirPods daal ke gaane chala dunga aur sab galiyan sunenge",
    "Tere baap me AirPods daal ke gaane chala dunga aur usme ad laga dunga",
    "Tere baap me AirPods daal ke gaane chala dunga bina permission ke",
    "Tere baap me AirPods daal ke gaane chala dunga jise sab report karenge",
    "Tere baap me Bluetooth speaker daal ke gali FM chala dunga aur livestream chalu kar dunga",
    "Tere baap me Bluetooth speaker daal ke gali FM chala dunga aur sab galiyan sunenge",
    "Tere baap me Bluetooth speaker daal ke gali FM chala dunga aur usme ad laga dunga",
    "Tere baap me Bluetooth speaker daal ke gali FM chala dunga bina charger ke",
    "Tere baap me Bluetooth speaker daal ke gali FM chala dunga bina data loss ke",
    "Tere baap me Bluetooth speaker daal ke gali FM chala dunga bina reboot ke",
    "Tere baap me Bluetooth speaker daal ke gali FM chala dunga fir usko chaat jaunga",
    "Tere baap me Bluetooth speaker daal ke gali FM chala dunga jise sab report karenge",
    "Tere baap me DJ system daal dunga",
    "Tere baap me DJ system daal dunga aur sab galiyan sunenge",
    "Tere baap me DJ system daal dunga aur usme ad laga dunga",
    "Tere baap me DJ system daal dunga bina data loss ke",
    "Tere baap me DJ system daal dunga bina reboot ke",
    "Tere baap me DJ system daal dunga fir usko chaat jaunga",
    "Tere baap me DJ system daal dunga jise sab report karenge",
    "Tere baap me Discord server chala dunga",
    "Tere baap me Discord server chala dunga aur livestream chalu kar dunga",
    "Tere baap me Discord server chala dunga aur sab galiyan sunenge",
    "Tere baap me Discord server chala dunga aur usme ad laga dunga",
    "Tere baap me Discord server chala dunga bina data loss ke",
    "Tere baap me Discord server chala dunga bina permission ke",
    "Tere baap me Discord server chala dunga jise sab report karenge",
    "Tere baap me Notepad khol ke code likh dunga",
    "Tere baap me Notepad khol ke code likh dunga aur sab galiyan sunenge",
    "Tere baap me Notepad khol ke code likh dunga aur usme ad laga dunga",
    "Tere baap me Notepad khol ke code likh dunga jise sab report karenge",
    "Tere baap me RAM stick daal dunga",
    "Tere baap me RAM stick daal dunga aur livestream chalu kar dunga",
    "Tere baap me RAM stick daal dunga aur sab galiyan sunenge",
    "Tere baap me RAM stick daal dunga aur usme ad laga dunga",
    "Tere baap me RAM stick daal dunga bina charger ke",
    "Tere baap me RAM stick daal dunga bina data loss ke",
    "Tere baap me RAM stick daal dunga bina reboot ke",
    "Tere baap me RAM stick daal dunga fir usko chaat jaunga",
    "Tere baap me RAM stick daal dunga jise sab report karenge",
    "Tere baap me SSD daal ke fast access kar lunga",
    "Tere baap me SSD daal ke fast access kar lunga aur livestream chalu kar dunga",
    "Tere baap me SSD daal ke fast access kar lunga aur sab galiyan sunenge",
    "Tere baap me SSD daal ke fast access kar lunga aur usme ad laga dunga",
    "Tere baap me SSD daal ke fast access kar lunga bina charger ke",
    "Tere baap me SSD daal ke fast access kar lunga bina data loss ke",
    "Tere baap me SSD daal ke fast access kar lunga bina permission ke",
    "Tere baap me SSD daal ke fast access kar lunga bina reboot ke",
    "Tere baap me SSD daal ke fast access kar lunga fir usko chaat jaunga",
    "Tere baap me SSD daal ke fast access kar lunga jise sab report karenge",
    "Tere baap me firewall daal ke secure kar dunga",
    "Tere baap me firewall daal ke secure kar dunga aur livestream chalu kar dunga",
    "Tere baap me firewall daal ke secure kar dunga aur sab galiyan sunenge",
    "Tere baap me firewall daal ke secure kar dunga aur usme ad laga dunga",
    "Tere baap me firewall daal ke secure kar dunga bina charger ke",
    "Tere baap me firewall daal ke secure kar dunga bina data loss ke",
    "Tere baap me firewall daal ke secure kar dunga bina reboot ke",
    "Tere baap me firewall daal ke secure kar dunga jise sab report karenge",
    "Tere baap me solar panel laga dunga aur usme ad laga dunga",
    "Tere baap me solar panel laga dunga bina charger ke",
    "Tere baap me solar panel laga dunga bina data loss ke",
    "Tere baap me solar panel laga dunga bina permission ke",
    "Tere baap me solar panel laga dunga jise sab report karenge",
    "Tere baap me spaghetti bana dunga",
    "Tere baap me spaghetti bana dunga aur livestream chalu kar dunga",
    "Tere baap me spaghetti bana dunga aur sab galiyan sunenge",
    "Tere baap me spaghetti bana dunga aur usme ad laga dunga",
    "Tere baap me spaghetti bana dunga bina charger ke",
    "Tere baap me spaghetti bana dunga bina data loss ke",
    "Tere baap me spaghetti bana dunga bina permission ke",
    "Tere baap me spaghetti bana dunga bina reboot ke",
    "Tere baap me torch daal dunga",
    "Tere baap me torch daal dunga aur livestream chalu kar dunga",
    "Tere baap me torch daal dunga aur sab galiyan sunenge",
    "Tere baap me torch daal dunga bina charger ke",
    "Tere baap me torch daal dunga bina data loss ke",
    "Tere baap me torch daal dunga bina permission ke",
    "Tere baap me torch daal dunga bina reboot ke",
    "Tere baap me torch daal dunga fir usko chaat jaunga",
    "Tere baap me torch daal dunga jise sab report karenge",
    "Tere baap pe GPS laga dunga",
    "Tere baap pe GPS laga dunga aur livestream chalu kar dunga",
    "Tere baap pe GPS laga dunga aur usme ad laga dunga",
    "Tere baap pe GPS laga dunga bina charger ke",
    "Tere baap pe GPS laga dunga bina data loss ke",
    "Tere baap pe GPS laga dunga bina permission ke",
    "Tere baap pe GPS laga dunga bina reboot ke",
    "Tere baap pe GPS laga dunga jise sab report karenge",
    "Tere baap pe QR code chipka ke scan karwaunga aur sab galiyan sunenge",
    "Tere baap pe QR code chipka ke scan karwaunga aur usme ad laga dunga",
    "Tere baap pe QR code chipka ke scan karwaunga bina reboot ke",
    "Tere baap pe QR code chipka ke scan karwaunga fir usko chaat jaunga",
    "Tere baap pe barcode chipka dunga aur usme ad laga dunga",
    "Tere baap pe barcode chipka dunga bina reboot ke",
    "Tere baap pe barcode chipka dunga fir usko chaat jaunga",
    "Tere baap pe barcode chipka dunga jise sab report karenge",
    "Tere khandaan ke mooch se violin bajake gali compose kar dunga",
    "Tere khandaan ke mooch se violin bajake gali compose kar dunga aur livestream chalu kar dunga",
    "Tere khandaan ke mooch se violin bajake gali compose kar dunga aur sab galiyan sunenge",
    "Tere khandaan ke mooch se violin bajake gali compose kar dunga aur usme ad laga dunga",
    "Tere khandaan ke mooch se violin bajake gali compose kar dunga bina charger ke",
    "Tere khandaan ke mooch se violin bajake gali compose kar dunga bina permission ke",
    "Tere khandaan ke mooch se violin bajake gali compose kar dunga bina reboot ke",
    "Tere khandaan ke mooch se violin bajake gali compose kar dunga fir usko chaat jaunga",
    "Tere khandaan ke mooch se violin bajake gali compose kar dunga jise sab report karenge",
    "Tere khandaan ko Flipkart pe sale pe daal dunga",
    "Tere khandaan ko Flipkart pe sale pe daal dunga aur sab galiyan sunenge",
    "Tere khandaan ko Flipkart pe sale pe daal dunga bina charger ke",
    "Tere khandaan ko Flipkart pe sale pe daal dunga bina permission ke",
    "Tere khandaan ko Flipkart pe sale pe daal dunga bina reboot ke",
    "Tere khandaan ko Flipkart pe sale pe daal dunga fir usko chaat jaunga",
    "Tere khandaan ko Flipkart pe sale pe daal dunga jise sab report karenge",
    "Tere khandaan ko OnlyFans pe daal dunga",
    "Tere khandaan ko OnlyFans pe daal dunga aur sab galiyan sunenge",
    "Tere khandaan ko OnlyFans pe daal dunga aur usme ad laga dunga",
    "Tere khandaan ko OnlyFans pe daal dunga bina charger ke",
    "Tere khandaan ko OnlyFans pe daal dunga bina data loss ke",
    "Tere khandaan ko OnlyFans pe daal dunga bina permission ke",
    "Tere khandaan ko OnlyFans pe daal dunga bina reboot ke",
    "Tere khandaan ko OnlyFans pe daal dunga fir usko chaat jaunga",
    "Tere khandaan me AirPods daal ke gaane chala dunga",
    "Tere khandaan me AirPods daal ke gaane chala dunga aur usme ad laga dunga",
    "Tere khandaan me AirPods daal ke gaane chala dunga bina charger ke",
    "Tere khandaan me AirPods daal ke gaane chala dunga bina data loss ke",
    "Tere khandaan me AirPods daal ke gaane chala dunga bina permission ke",
    "Tere khandaan me AirPods daal ke gaane chala dunga bina reboot ke",
    "Tere khandaan me AirPods daal ke gaane chala dunga jise sab report karenge",
    "Tere khandaan me Bluetooth speaker daal ke gali FM chala dunga",
    "Tere khandaan me Bluetooth speaker daal ke gali FM chala dunga aur livestream chalu kar dunga",
    "Tere khandaan me Bluetooth speaker daal ke gali FM chala dunga aur sab galiyan sunenge",
    "Tere khandaan me Bluetooth speaker daal ke gali FM chala dunga aur usme ad laga dunga",
    "Tere khandaan me Bluetooth speaker daal ke gali FM chala dunga bina charger ke",
    "Tere khandaan me Bluetooth speaker daal ke gali FM chala dunga bina data loss ke",
    "Tere khandaan me Bluetooth speaker daal ke gali FM chala dunga bina permission ke",
    "Tere khandaan me Bluetooth speaker daal ke gali FM chala dunga fir usko chaat jaunga",
    "Tere khandaan me DJ system daal dunga",
    "Tere khandaan me DJ system daal dunga aur livestream chalu kar dunga",
    "Tere khandaan me DJ system daal dunga aur sab galiyan sunenge",
    "Tere khandaan me DJ system daal dunga aur usme ad laga dunga",
    "Tere khandaan me DJ system daal dunga bina charger ke",
    "Tere khandaan me DJ system daal dunga bina data loss ke",
    "Tere khandaan me DJ system daal dunga bina reboot ke",
    "Tere khandaan me DJ system daal dunga fir usko chaat jaunga",
    "Tere khandaan me DJ system daal dunga jise sab report karenge",
    "Tere khandaan me Discord server chala dunga",
    "Tere khandaan me Discord server chala dunga aur sab galiyan sunenge",
    "Tere khandaan me Discord server chala dunga bina charger ke",
    "Tere khandaan me Discord server chala dunga fir usko chaat jaunga",
    "Tere khandaan me Notepad khol ke code likh dunga aur livestream chalu kar dunga",
    "Tere khandaan me Notepad khol ke code likh dunga aur sab galiyan sunenge",
    "Tere khandaan me Notepad khol ke code likh dunga bina charger ke",
    "Tere khandaan me Notepad khol ke code likh dunga bina data loss ke",
    "Tere khandaan me Notepad khol ke code likh dunga bina permission ke",
    "Tere khandaan me Notepad khol ke code likh dunga fir usko chaat jaunga",
    "Tere khandaan me Notepad khol ke code likh dunga jise sab report karenge",
    "Tere khandaan me RAM stick daal dunga",
]

# Function to spam target with gaalis
async def spam(target, username):
    global stop_spam
    for gali in galis:
        if stop_spam:
            break
        await client.send_message(target, f"{username} {gali}")
        await asyncio.sleep(0.0)

# Command: /fuck @username
@client.on(events.NewMessage(pattern="/fuck"))
async def start(event):
    global stop_spam
    sender_id = str(event.sender_id)

    if sender_id not in approved_users:
        await event.reply("You're not approved to use this command.")
        return

    parts = event.message.text.split()
    if len(parts) != 2:
        await event.reply("Usage: /fuck <@username>")
        return

    username = parts[1]
    try:
        user = await client.get_entity(username)
    except:
        await event.reply("Couldn't find this user.")
        return

    chat = event.chat_id
    stop_spam = False
    await event.reply(f"Starting ultra-fast spam on {username}!")
    asyncio.create_task(spam(chat, username))

# Command: /stop
@client.on(events.NewMessage(pattern="/stop"))
async def stop(event):
    global stop_spam
    stop_spam = True
    await event.reply("Spam stopped!")

# Command: /approve <user_id>
@client.on(events.NewMessage(pattern="/approve"))
async def approve_user(event):
    if str(event.sender_id) != OWNER_ID:
        await event.reply("You're not authorized to approve users.")
        return

    parts = event.message.text.split()
    if len(parts) != 2:
        await event.reply("Usage: /approve <user_id>")
        return

    user_id = parts[1]
    approved_users.add(user_id)
    await event.reply(f"User {user_id} approved!")

# Command: /disapprove <user_id>
@client.on(events.NewMessage(pattern="/disapprove"))
async def disapprove_user(event):
    if str(event.sender_id) != OWNER_ID:
        await event.reply("You're not authorized to disapprove users.")
        return

    parts = event.message.text.split()
    if len(parts) != 2:
        await event.reply("Usage: /disapprove <user_id>")
        return

    user_id = parts[1]
    approved_users.discard(user_id)
    await event.reply(f"User {user_id} disapproved.")

# Start the client
client.start()
print("Userbot is running...")
client.run_until_disconnected()