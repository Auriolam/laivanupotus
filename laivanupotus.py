import random
import sqlite3
import ast
import pygame
import sys
import time

from pygame.locals import *

"""
Tehdään eka yksinkertainen laivanupotus
Tarvitaan:
ok
-pelilogiikka
-pieni koordinaatisto ekana
    a-f(?)
    1-6(?)
    pitäskö ruudut olla jotain laatikoita ■? Vai | | ja "erotetaan rivit __ pitää kokeilla", välimerkki(" ") vaihdetaan laivaksi "a" osumaksi x tai huti o
    pitääks mun tehä "staattiseksi" otsikko linjat(a-f ja 1-6) ja sitte listata ruudun tila muuten
    periaatteessa 4 lautaa 1) ihmisen asettelema 2) koneen asettelema 3)ihmisen arvausalusta 4)koneen arvausalusta
    Pitöskö laivat ja niiden osumat olla listoja
    Pitöskö koordinaatiston ruudut olla listoja ja niissä status?
ok
-pienet laivat
    toistaiseksi laivat voisi olla luokkaa aa,bbb ja cccc, 
    laivat objecteja? funktiot osumalle ja milloinka tuhoutunu? pitääkö laivan tietää sen olevan esim a1,a2,a2 tai a1,b1,c1 vai tietääkö lauta sen olevan siinä?

ok
-pelin aloituksessa pitää kysyä pelaajalta mihin laivat asetetaan
    -laivat pitää osua koordinaatiston sisään
    -tietokone random laivat(?)
ok
-peliä pelatessa kysytään mihin ammutaa tyylillä a1, f7 tai jotain
    -sen jälkeen tietokoneen vuoro
    -vuoron jälkeen piirretään koordinaatisto uudestaan

ok
-pitäskö kokeilla jos sais cpun tekee "järkeviä" päätöksiä
    -pitääkö cpun tietää mikä laiva kyseessä ja sitten randomoida mihinkä siihen vierelle testataan
    -ongelma voin jäädä looppiin missä se "etsii" ympäriltä mahdollista kohtaa mutta jos kaikissa on jo jotain, se jatkaa niiden luuppaamista
    -pitäskö sitte olla sillee et se etsii pelkästää "+" alueen jos on kaikki samat mennää laivan toiseen osaan? etsitään viereltä?
    
ok
-Tallennuksen tekeminen tietokantaan
    -Mitä kaikkea pitää muistaa laittaa. Pitääkö kaikki tehdyt muuttujat tallentaa?. 
        -Pelaaja ja cpu laivat. Ohi, cpuohi. Laivojen määrä? Laivakoko? Cpu osumakohdat.Cpuarvaukset(?)
        -Kaikille näille oma sarake?
    -Cpu vuoro menee niin nopeasti, että aina pelaajan vuoro aloittaa, joten kenen vuoro ei tarvitse tallentaa.
    -Koodia muokattava kysymään alussa ladataanko tallennuksesta vai uusi peli. Poistetaanko tallennettu automaattisesti?
    -Meneekö listat yhtenä elementtinä? 
    -Jos ei ole tallennusta niin mennää pelii

-Varmaan joudun putsaamaan koodia ennen grafiikan tekoa(?)
    -Ongelma. Olen tehnyt pelin niin, että se printtaa suoraan pelin statuksen consolille ulos. Eli todennäköisesti minun pitää tallentaa pelin tilanne johonkin arrayhin
        ja sitten printata array ulos.
    -Hyvin meni graaffista ulostusta
    -Cpu logiikkaa rikkoitui. kaiketi ei tee järkevästi 3. osuman etsimistä. 
    - Unohtu laittaa quitti ja tallennus+quitti toimivaksi
    
-grafiikka?
    -kuinka tehdään
    -?? https://realpython.com/pygame-a-primer/
        -pygame https://www.youtube.com/watch?v=waY3LfJhQLY
        -https://www.youtube.com/watch?v=B6DrRN5z_uU
        -gridin tekoo? https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
        -Jos ei käyttäs ihan suoraa tutoriaalia laivanupotukseen vaan käyttäs miinaharavaa apuna. Näin saattas oppiakkin jotain.
        -?? https://www.youtube.com/watch?v=n0jZRlhLtt0
        -?? https://www.youtube.com/watch?v=RRYgc4YIhEs      
    -?? tkinter
    -onko jokainen koskematon laatta nappula? paitsi ekat rivit/sarakkeet?
    ois pitänä menu tehdä https://www.youtube.com/watch?v=Y52JsDs4cMQ ???

-korjaukset
    -ehkä muutettava tietokoneen logiikkaa.
    -muutetaanko tallennusta?`
    -muita bugeja läjä
    
myöhemmin: Tallennus tietokantaan, grafiikka, äänet
"""
#Graafisen asetuksia------------------------------------------------------
pygame.init()
WIDTH, HEIGHT = 1000, 800
ROW = 20
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.init()
pygame.display.set_caption("Laivanupotus")

#JOSTAINSYYSTÄ PYTHON KOODI ALKAA KANSIOSSA OPIKOODIA2023 EIKÄ KANSIOSSA LAIVANUPOTUS. ETSI MISSÄ VIKA!!
BG = pygame.transform.scale(pygame.image.load("./imgs/tausta.jpg"), (WIDTH,HEIGHT))
grafrivi=[]
grafarray=[]
NUM_FONT = pygame.font.SysFont("Arial", 30)
NUM_COLORS = "Black"
SIZE = WIDTH/HEIGHT
#Graafisen asetuksia------------------------------------------------------

print("Hello world")
database = sqlite3.connect("laivasave.db")
#Laivat on listana. Pitääkö listalle tehdä jotain ennen sqliteen laittamista?
#BLOB The value is a blob of data, stored exactly as it was input.
database.execute("CREATE TABLE IF NOT EXISTS Save(ID INT PRIMARY KEY NOT NULL, LAIVAT BLOB, CPULAIVAT BLOB, OHI BLOB, CPUOHI BLOB, CPUARVAUS BLOB, CPUOSU INTEGER, CPUOSU2 INTEGER, CPUOSUMAKOHTA BLOB, CPUOSUMAKOHTA2 BLOB);")
database.commit()
database.close()


kordx = [" ","a","b","c","d","e","f"]
#kordx randomointi cpulle osoittautu vaikeeksi niin tein toisen arrayn 
# mistä otetaan xarvo .-.
kordxr = ["a","b","c","d","e","f"]
kordy = 7
#Tein vähä tymästi, mutta nyt 1 osuttu kohta 0 ei osuttu kohta, ja mones laiva seuraavaksi siinä
#23-08-03 Olen aika varma, että tämä ajattelu vei minut syvään suoho. Ois ehkä ollu helpompi vaa tehdä lista koko kentästä ja pitää kaikki tiedot siinä listassa.
#Tämän mietinnän korjaukseen on joutunu tekemään ihan kauheeta koodia. 
laivatvanhat = [["a1",1,1],["b1",0,1],["c1",1,1],["d2",0,2],["d3",1,2],["d4",0,2]]
laivat = []
cpulaivat = []
#testejä
ohi = ["a4","c5","c6","f3"]
ohi = []
cpuohi = []
cpuviimeksiosu = False
cpuosu2 = False
cpuosumakohta = 0
cpuosumakohta2 = 0
cpuarvaukset = []
osumat = 0
cpuosumat = 0
laivakoko = len(laivat)
lopeta = False
laivojenmäärä = 0
cpulaivojenmäärä = 0
asetetutlaivat = 0

pelialoitettu = False
clicked = False
buttonarray = []
button1 = 0

#Ohjeita käytetty buttoneihin Coding with russ https://www.youtube.com/watch?v=G8MYGDf_9ho , LemasterTech https://www.youtube.com/watch?v=16DM5Eem0cI
class Gridbutton():
    button_col = (25, 190, 225)
    hover_col = (75, 75, 55)
    click_col = (50, 150, 255)
    text_col = (255, 255, 255)
    
    global button1

    def __init__(self, size, x, y,text):
        self.size = size
        self.x = x
        self.y = y
        self.text = text


    def draw_button(self):
        global clicked
        action = False

        pos = pygame.mouse.get_pos()

        button_rect = Rect(self.x, self.y, 50, 50)
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                action = False
                pygame.draw.rect(WIN, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(WIN, self.hover_col, button_rect)
        else:
            pygame.draw.rect(WIN, self.button_col, button_rect)
        text1 = NUM_FONT.render(str(self.text), 1, NUM_COLORS)
        pygame.draw.rect(WIN, "aqua", (self.x , self.y, self.size, self.size))
        pygame.draw.rect(WIN, "black", (self.x , self.y, self.size, self.size), 2)
        WIN.blit(text1, (self.x +(self.size/2 -text1.get_width()/2), self.y + (self.size/2 - text1.get_height()/2)))
        #print("BUTTONIN SELF TEXT ON TÄSSÄ", self.text)
        if action == True:
            print("RETURNATAAN self.text", self.text)
            return self.text
        

#piirros tehty Tech with Tim:in johdolla osaksi. 
def draw():
    global kordx
    WIN.blit(BG, (0, 0))
    size = WIDTH//ROW
    global buttonarray
    for i, row in enumerate(grafarray):
        y=size *i
        for j, value in enumerate(row):
            x = size * j
            button = 0
            #Teen ekana keltasella värillä niin nään mitä tapahtuu
            pygame.draw.rect(WIN, "cadetblue1", (x, y, size, size))
            pygame.draw.rect(WIN, "black", (x , y, size, size), 2)

            text = NUM_FONT.render(str(value), 1, NUM_COLORS)
            WIN.blit(text, (x +(size/2 -text.get_width()/2), y + (size/2 - text.get_height()/2)))

            if value == "A":
                pygame.draw.rect(WIN, "Grey", (x, y, size, size))
                pygame.draw.rect(WIN, "black", (x , y, size, size), 2)
                WIN.blit(text, (x +(size/2 -text.get_width()/2), y + (size/2 - text.get_height()/2)))
            elif value == "X":
                pygame.draw.rect(WIN, "red", (x, y, size, size))
                pygame.draw.rect(WIN, "black", (x , y, size, size), 2)
                WIN.blit(text, (x +(size/2 -text.get_width()/2), y + (size/2 - text.get_height()/2)))
            elif value == "o":
                pygame.draw.rect(WIN, "Green", (x, y, size, size))
                pygame.draw.rect(WIN, "black", (x , y, size, size), 2)
                WIN.blit(text, (x +(size/2 -text.get_width()/2), y + (size/2 - text.get_height()/2)))
            #TYHJISTÄ PITÄÄ TEHDÄ NAPPULOITA. MUUT OIKEESTAAN TURHIA!
            elif value == "t":
                if i < 8:
                    gkoordi = str(kordx[j])+str(i)
                else:
                    gkoordi = "0"
                button = Gridbutton(size,x,y,gkoordi)
                button.draw_button()
                #pygame.draw.rect(WIN, "black", (x , y, size, size), 2)
                #button = pygame.Rect(x,y,size,size)
                pos = pygame.mouse.get_pos()
                 
            else:
                pass

            #koordbutton = Gridbutton(rect, x,y)
            if button == 0:
                pass
            else:
                buttonarray += [button]  
    #nopeet exit ja tallennusnappulat blokki. Jos täytyy ohjelman olla jokseenkin näytettävissä
    y = 400 
    x = 500
    button = Gridbutton(size,x,y,"Exit")
    button.draw_button()
    buttonarray += [button]
    if pelialoitettu == True:
        y = 450 
        x = 500
        button = Gridbutton(size,x,y,"Tallenna ja Lopeta")
        button.draw_button()
        buttonarray += [button]
        pygame.display.update()
draw()

def drawaloitus(numero):
    global kordx
    global pelialoitettu
    WIN.blit(BG, (0, 0))
    size = WIDTH//ROW
    global buttonarray
    y = size
    x = size
    if numero == 2:
        
        for num in range(2):
            y=size*2 
            x = size*num+20
            if num == 0:
                gkoordi = "y"
            else:
                gkoordi = "n"
            button = Gridbutton(size,x,y,gkoordi)
            button.draw_button()
            buttonarray += [button]
    elif numero == 4:
        
        for num in range(4):
            y=size*2 
            x = size*num+20
            gkoordi = num+1
            button = Gridbutton(size,x,y,gkoordi)
            button.draw_button() 
            buttonarray += [button]
    elif numero == 3:
        for num in range(2):
            y=size*2 
            x = size*num+20
            if num == 0:
                gkoordi = "p"
            else:
                gkoordi = "v"
            button = Gridbutton(size,x,y,gkoordi)
            button.draw_button()
            buttonarray += [button]
    pygame.display.update()

def get_grid_pos(mouse_pos):
    mx, my = mouse_pos
    row = int(my)//SIZE
    col = int(mx)//SIZE
    return row, col

def laudanpiirto():
    #tein niin perkeleen vaikeesti tämän, että graafiseen ulkoasuun tehdessä kostautu. 
    #Voisinko tehdä niin, että teen arrayn, mihin lisään rivin tiedot. Rivien array lisätään sitten Laudan arrayhin. Graafisessa sitten luetaa lauta array kuvaksi(?)
    global grafrivi
    global grafarray
    print("Pelaajalauta")
    print("  a b c d e f ")
    grafarray +=[kordx]
    for num in range(1,kordy): 
        for char in kordx:
            tarkistus = False
            for elem in laivat:
                if char+str(num) == elem[0]:
                    if elem[1] == 0:
                        print("A|",end="")
                        tarkistus = True
                        grafrivi += "A"
                    else:
                        print("X|",end="")
                        tarkistus = True
                        grafrivi += "X"

            for elem in cpuohi:
                if char+str(num) == elem:
                    print("o|",end="")
                    tarkistus = True
                    grafrivi += "o"

            if tarkistus == False:        
                if char == " ":
                    print(str(num)+"|", end="")
                    grafrivi += str(num)
                else:
                    print("■|",end="")
                    grafrivi += "t"
            #print(f"{num}","■|"*kordy)
        #Lisätään rivi array laudan arrayhin tulisi tänne.
        grafarray += [grafrivi]
        print("") 
        grafrivi =[]

def cpulaudanpiirto():
    print("CPU LAUTA")
    print("  a b c d e f ")
    global grafrivi
    global grafarray
    grafarray +=[kordx]
    for num in range(1,kordy): 
        for char in kordx:
            tarkistus = False
            for elem in cpulaivat:
                if char+str(num) == elem[0]:
                    if elem[1] == 0:
                        #käytetään A| kun halutaan tarkistella cpu laivoja 
                        # ja ■| kun normaali toiminta
                        #print("A|",end="")
                        print("■|",end="")
                        tarkistus = True
                        grafrivi += "t"
                    else:
                        print("X|",end="")
                        tarkistus = True
                        grafrivi += "X"

            for elem in ohi:
                if char+str(num) == elem:
                    print("o|",end="")
                    tarkistus = True
                    grafrivi += "o"

            if tarkistus == False:        
                if char == " ":
                    print(str(num)+"|", end="")
                    grafrivi += str(num)
                else:
                    print("■|",end="")
                    grafrivi += "t"
            #print(f"{num}","■|"*kordy)
        grafarray += [grafrivi]
        print("") 
        grafrivi =[]

#tehdään tallennus omana funktiona, poistetaan vanhat tiedot tallennetaan uudet
def tallennus():
    global laivat
    laivat = str(laivat)
    global cpulaivat
    cpulaivat = str(cpulaivat)
    global ohi
    ohi = str(ohi)
    global cpuohi
    cpuohi = str(cpuohi)
    global cpuviimeksiosu
    global cpuosu2 
    global cpuosumakohta
    cpuosumakohta = str(cpuosumakohta)
    global cpuosumakohta2 
    cpuosumakohta2 = str(cpuosumakohta2)
    global cpuarvaukset 
    cpuarvaukset = str(cpuarvaukset)
    id = 1
    database = sqlite3.connect("laivasave.db")
    #pitääkö drop tablettaa, vai voiko clearata tablen? Periaatteessa jos pidän vain yhtä id 1 tallennusta, niin pitäskö poistaa pelkästään se?
    database.execute("DROP TABLE IF EXISTS Save;")
    database.execute("CREATE TABLE IF NOT EXISTS Save(ID INT PRIMARY KEY NOT NULL, LAIVAT BLOB, CPULAIVAT BLOB, OHI BLOB, CPUOHI BLOB, CPUARVAUS BLOB, CPUOSU INTEGER, CPUOSU2 INTEGER, CPUOSUMAKOHTA BLOB, CPUOSUMAKOHTA2 BLOB);")
    #ID INT PRIMARY KEY NOT NULL, LAIVAT BLOB, CPULAIVAT BLOB, OHI BLOB, CPUOHI BLOB, CPUARVAUS BLOB, CPUOSU INTEGER, CPUOSU2 INTEGER)
    req=("INSERT INTO Save (ID, LAIVAT, CPULAIVAT, OHI, CPUOHI, CPUARVAUS, CPUOSU, CPUOSU2, CPUOSUMAKOHTA, CPUOSUMAKOHTA2) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
    areq=(id, laivat, cpulaivat, ohi, cpuohi, cpuarvaukset, cpuviimeksiosu, cpuosu2, cpuosumakohta, cpuosumakohta2)
    database.execute(req,areq) 
    database.commit()
    database.close()

#haluan tehdä laivojen asettelun ja laivojen rajojen tarkistuksen täällä
def laivojenasettelu(laivat):
    global grafarray
    asetus = True
    global buttonarray
    buttonarray = []
    while asetus ==True:
        #käytetään aloutusfunktion funktiota 4 kysyessä 4 laivaa. (Vaihtoehtoja 4)
        laivojenmäärä = int(aloitusloop(4))
        #laivojenmäärä = int(input("Montako laivaa?(1-4): "))
        global cpulaivojenmäärä 
        cpulaivojenmäärä=laivojenmäärä
        laivannumero=0
        buttonarray = []
        grafarray = []
        laudanpiirto()
        draw()
        go = True
        lopeta = False
        toiminto = 0

        #Pitää todennäköisesti tehdä taas pygame rakenne? Ois varmaan kannattanu tehdä hyvä looppi vaan alkuuuuu.
        while laivojenmäärä > 0:
            while lopeta==False:
                if go == True:
                    laudanpiirto()
                    draw()
                    go=False
                #Pygame looppaa eventtiä niin kauan kunnes jotain tapahtuu
                for event in pygame.event.get():
                    tekstinaytto("Mihin laiva asetetaan?", 400, 50)
                    for but in buttonarray:
                        if but.draw_button():
                            toiminto = but.text
                            print("BUTTONIN SELF TEXTIÄ PAINETTU", toiminto)
                            tekstinaytto("Mihin laiva asetetaan?", 400, 50)
                    
                    if event.type == pygame.quit:
                        lopetaaloitus = True
                        lopeta = True
                        break 
                    if toiminto == "Exit":
                        lopeta = True
                        pygame.quit()
                        sys.exit()
                    if toiminto != 0 and toiminto != None:
                    #go pitää mennä napin painalluksen taakse
                        lopeta = True
                        go = True
            
            laivasamassa=False
            laiva=[]
            koordinaatti = toiminto
            toiminto = 0
            lopeta = False
            go = True
            buttonarray = []
            grafarray = []
            #koordinaatti = input("Anna koordinaatti muodossa xy: ")
            laivansuunta = drawaloitus(3)
            while lopeta==False:
                if go == True:
                    draw()
                    go=False
                #Pygame looppaa eventtiä niin kauan kunnes jotain tapahtuu
                for event in pygame.event.get():
                    tekstinaytto("Suunta pystyyn vai vaakaan?(p/v)")
                    for but in buttonarray:
                        if but.draw_button():
                            toiminto = but.text
                            print("BUTTONIN SELF TEXTIÄ PAINETTU", toiminto)
                            tekstinaytto("Mihin laiva asetetaan?", 400, 50)
                    
                    if event.type == pygame.quit:
                        lopetaaloitus = True
                        lopeta = True
                        break 
                    if toiminto != 0 and toiminto != None:
                    #go pitää mennä napin painalluksen taakse
                        lopeta = True
                        go = True

            
            #print("Laivansuunta drawaloituksesta", toiminto)
            laivansuunta = toiminto
            #toiminnot nollataan
            toiminto = 0
            lopeta = False
            go = True
            buttonarray = []
            grafarray = []
            #laivansuunta = input("Pystyyn vai vaakaan?(p/v): ") 
            koordinaattix = koordinaatti[0]
            koordinaattiy = int(koordinaatti[1])
            if laivansuunta != "p" and laivansuunta != "v":
                laivansuunta = "v"

            rajojenulkona=True
            
            for kordxarvo in kordx:
                for kordyarvo in range(kordy):
                    if koordinaatti==kordxarvo+str(kordyarvo):
                        rajojenulkona=False
            #täytyykin viel tehdä erikseen             
            if kordx.index(kordxarvo) > len(kordx):
                rajojenulkona = True

            if laivansuunta == "p" and rajojenulkona == False:
                for osa in range(3):
                    if koordinaattiy+osa > kordy:
                        rajojenulkona = True     
                    #laivat += [[koordinaattix +str(koordinaattiy+osa), 0, laivannumero]]
                    if rajojenulkona != True:
                        laiva += [[koordinaattix +str(koordinaattiy+osa), 0, laivannumero]]
                    print(laivat)
            elif laivansuunta == "v" and rajojenulkona == False:
                kirjainindex = kordx.index(koordinaattix)
                print("kirjaimen indexi", kirjainindex)
                
                for osa in range(3):
                    if kirjainindex+osa > len(kordx)-1:
                        rajojenulkona = True
                    #laivat += [[kordx[kirjainindex+osa]+str(koordinaattiy), 0, laivannumero]]
                    if rajojenulkona != True:
                        laiva += [[kordx[kirjainindex+osa]+str(koordinaattiy), 0, laivannumero]]
                    print(laivat)

            for elem in laivat:
                for osa in laiva:
                    print("printataan saman ruudun tarkistus",elem,osa)
                    if elem[0] == osa[0]:
                        laivasamassa=True
            for elem in laiva:
                for kordxarvo in kordx:
                    for kordyarvo in range(kordy):
                        if elem==kordxarvo+str(kordyarvo):
                            rajojenulkona=True

            if rajojenulkona == True :
                print("rajojen ulkopuolella ")
                print(laivansuunta)
            elif laivasamassa == True:
                print("laivat samassa ruudussa")
            else:
                print("laivan keula ok")
                print(laivansuunta)
                laivat += laiva
                laivannumero += 1
                laivojenmäärä -= 1
                print(laiva)
                print("Laivojen listan tarkistus", laivat)
        if laivojenmäärä == 0:
            asetus = False
        
    grafarray = []

def cpulaivojenasettelu(cpulaivat):
    print("CPU LAIVOJEN ASETTELU ALKANUT")
    global cpulaivojenmäärä
    laivannumero=0
    cpulaudanpiirto()
    
    while cpulaivojenmäärä > 0:
        print("CPULAIVA MÄÄRÄ")
        laivasamassa=False
        cpulaiva=[]
        #koordinaatti = input("Anna koordinaatti muodossa xy")
        #koordinaatti täytyy randomoida jotenkin, mullahan on se tyhjä siinä kordx alussa voiko poistaa vai teenkö tarkistuksen?
        
        #laivansuunta = input("Pystyyn vai vaakaan?(p/v)") 
        laivanrand=random.randint(0,1)
        #täällä voidaan suoraan eliminoida koneen laivojen yli laittamiset
        if laivanrand == 0:
            laivansuunta ="p"
            koordinaatti = random.choice(kordxr)+str(random.randint(1,kordy-3))
        else:
            laivansuunta = "v"
            koordinaatti = random.choice(kordxr)+str(random.randint(1,kordy))
        koordinaattix = koordinaatti[0]
        koordinaattiy = int(koordinaatti[1])
        if laivansuunta != "p" and laivansuunta != "v":
            laivansuunta = "v"

        rajojenulkona=True
        #TÄMÄ ON TODENNÄKÖISESTI VÄÄRIN 3.7.2023
        for kordxarvo in kordxr:
            for kordyarvo in range(kordy):
                if koordinaatti==kordxarvo+str(kordyarvo):
                    rajojenulkona=False

        if kordx.index(kordxarvo) > len(kordx):
            rajojenulkona = True

        if laivansuunta == "p" and rajojenulkona == False:
            for osa in range(3):
                if koordinaattiy+osa > kordy:
                    rajojenulkona = True
                #laivat += [[koordinaattix +str(koordinaattiy+osa), 0, laivannumero]]
                if rajojenulkona != True:
                    cpulaiva += [[koordinaattix +str(koordinaattiy+osa), 0, laivannumero]]
                print(cpulaivat)
        elif laivansuunta == "v" and rajojenulkona == False:
            kirjainindex = kordx.index(koordinaattix)
            print("kirjaimen indexi", kirjainindex)

            for osa in range(3):
                if kirjainindex+osa > len(kordx)-1:
                    rajojenulkona = True    
                #laivat += [[kordx[kirjainindex+osa]+str(koordinaattiy), 0, laivannumero]]
                if rajojenulkona != True:
                    cpulaiva += [[kordx[kirjainindex+osa]+str(koordinaattiy), 0, laivannumero]]
                print(cpulaivat)

        for elem in cpulaivat:
            for osa in cpulaiva:
                print("printataan saman ruudun tarkistus",elem,osa)
                if elem[0] == osa[0]:
                    laivasamassa=True

        if rajojenulkona == True :
            print("rajojen ulkopuolella ")
            print(laivansuunta)
        elif laivasamassa == True:
            print("laivat samassa ruudussa")
        else:
            print("laivan keula ok")
            print(laivansuunta)
            cpulaivat += cpulaiva
            laivannumero += 1
            cpulaivojenmäärä -= 1
            print(cpulaiva)
            print("CPU Laivojen listan tarkistus", cpulaivat)
        cpulaudanpiirto()

def cpuarvausfunk():
    arvausok = False
    global cpuohi
    global cpuosumat
    cpuosumat = 0
    arvaus = 0
    global cpuviimeksiosu
    global cpuosu2
    global cpuosumakohta
    global cpuosumakohta2
    global cpuarvaukset
    
    while arvausok == False:
        sama = False
        osui = False
        samaboat = False
        #tehdään randomi varmasti laudan sisällä
        koordinaattix = random.choice(kordx)
        koordinaattiy = str(random.randint(1,kordy))
        #yritän miettiä mitenkä saisin cpun tekemään vähän "parempia" valintoja
        #mitenkä jos se onkin viimenen osa laivasta?
        if cpuviimeksiosu == True:
            osumax = cpuosumakohta[0]
            osumay = int(cpuosumakohta[1])
            osumaxindex = kordxr.index(osumax)
            osumaxindex0 = osumaxindex-1
            osumaxindex2 = osumaxindex+1
            osumay0 = osumay-1
            osumay2 = osumay+1
            cpuarvaukset = []
            #testataan onko kordinaatit ulkona alueesta
            #onko järkeä? voe helvetti varmaan pitäs tehdä vaan kordinaatit ja katsoa sen jälkeen onko laudalla
            #ja voihan joku näistä olla mutta ei kaikki, esim a1 osuttu, a0 ei olemassa -a0 ei olemassa, mutta a2 ja b1 legittejä
            #pitäskö tehdä toisinpäin ja sitte suoraa lisätä hyväksyttävä naatti johonki arvaus arrayhin?
            # tosiaan
            if len(cpuarvaukset)==0 or cpuosu2==True:
                if osumaxindex0<0:
                    #tuleeko joku tarkistus tänne
                    kordxi0 = False
                else:
                    cpuarvaukset += [kordxr[osumaxindex0]+str(osumay)]

                if osumaxindex2 > len(kordxr)-1:
                    kordxi2 = False
                else:

                    cpuarvaukset += [kordxr[osumaxindex2]+str(osumay)]

                if osumay0 <= 0:
                    kordy0 = False
                else:
                    cpuarvaukset += [osumax+str(osumay0)]
                if osumay2 >kordy:
                    kordy2 = False
                else:
                    cpuarvaukset += [osumax+str(osumay2)]
                cpuosu2 = False
            okarvaukset = []
            #print("cpu arvaukset osuman jälkeen", cpuarvaukset)
            #tämän muotoa muutettava nyt tulee duplikaatteja okarvaukset listaan!!!!!!!!!!!!!!!!!!
            #tulee myös vanhat arvaukset, vai turhaa ja 
            for elem in cpuohi:
                for tehtyarvaus in cpuarvaukset:
                    if elem == tehtyarvaus:
                        arvausok == False
                        sama = True
                        index = cpuarvaukset.index(tehtyarvaus)
                        del cpuarvaukset[index]
                   
            #print("ok arvaukset", cpuarvaukset)

            #tarvitsen arvauksen randomoituna hyvien arvausten listasta
            arvaus = random.choice(cpuarvaukset)

            for elem in cpuohi:
                if elem == arvaus:
                    arvausok == False
                    sama = True
        
            for laiva in laivat:
                if laiva[0] == arvaus:
                    if laiva[1] == 1:
                        print("Sama naatti")
                        samaboat = True
                    #PITÄÄKÖ TEHDÄ UUDESTAAN OSU KOHTA MISSÄ SE LOOPPAA TAKAS TÄHÄN SAMAAN PAIKKAA? vai pitääkö tehdä erikohtaan funktio missä otetaan huomioon, että osuttu uudestaan
                    #tälläkertaa laivan keskelle tai reunalle. Reunalla pitää hypätä keskuskohdan yli takaisin tai jos keskellä niin yrittää seuraavaan. Tyhmästi 3 vaihtoehtoa(?)
                    else:
                        laiva[1] = 1
                        osui = True
                        arvausok = True
                        #pitääkö tehdä osumakohta 2 ja osumakohta1 ja osumakohta2 erotus katsoa? Saako siitä suunnan miten laiva on?
                        #cpuosumakohta = arvaus
                        cpuosumakohta2 = arvaus
                        #pitääkö vaihtaa toiseen osu viimeksi ? katsoa osumakohta ja sen perusteella  on 2 vaihtoehtoa
                        cpuviimeksiosu = False
                        cpuosu2 = True
                        print("CPU OSUI TOISEN KERRAN JA CPUOSU2 on nyt TRUE")
            if osui == False:
                sama = False
                if samaboat == True:
                    sama=True
                for elem in cpuohi:
                    if arvaus == elem:
                        print("Sama naatti")
                        sama = True
                        index = cpuarvaukset.index(arvaus)
                        del cpuarvaukset[index]
                if sama == False:       
                    cpuohi += [arvaus]
                    arvausok = True
            cpuosumat = 0
            print(cpuohi)
            for laiva in laivat:
                if laiva[1] == 1:
                    print(laiva[0])
                    cpuosumat += 1
            indeksi = cpuarvaukset.index(arvaus)
            del cpuarvaukset[indeksi]
            #print("tehtyä arvauslistaa osuman jälkeen olemassa", cpuarvaukset)
            if len(cpuarvaukset)==0:
                cpuviimeksiosu = False
            #print("cpuosumat",cpuosumat)
            #print("VIIMEKSI OSU", cpuviimeksiosu)

        #OK kopio cpuosumasta, --------------------------------------------------------------------------------------------------------------------------------------------
        elif cpuosu2 == True:
            #tehdään vertailu osumakohtien kanssa, että koordinaateista saadaan ulos jotain tyyppii 1,0 -1,0 tai 0,1 0,-1, näillä saadaan selville laivan suunta
            #hetkinen pitääkö ekana selvittää kumpi on suurempi ja sitten tehdä vertailu niin sais aina "positiiviset luvut". Näin saisi ankkuroitua kordinaatin ja siitä sitten laskea
            #missä on seuraavaksi laivaa jälellä. Toisaalta on vain 4 vaihtoehtoa. Voisin eliminoida 2 vaihtoehtoa koska ne ovat samat mihin on jo osuttu.
            #Keskiviikko: Ehkä huomattu bugi täällä, missä cpuvaihtoehdoissa menee jokin pieleen. En ole osunut siihen toistakertaa testauksien yhteydessä.
            
            osumax = cpuosumakohta[0]
            osumay = int(cpuosumakohta[1])
            osumaxindex = kordxr.index(osumax)

            osumax2 = cpuosumakohta2[0]
            osumay2 = int(cpuosumakohta2[1])
            osumaxindex2 = kordxr.index(osumax2)

            delttax = osumaxindex - osumaxindex2
            delttay = osumay - osumay2

            suunta = str(delttax) + str(delttay)
            #print("osuma2 suunta tarkastelu aloitettu",suunta)
            #pitääkö laskut katsoa, että ne on loogisia? Osuvat arrayn sisälle? Vai poistuuko ne luonnollisesti 
            #Vihkoon piirtely onnistunu?
            #print("CPU ARVAUKSIEN PITUUS ENNEN IF LEN(CPUARVAUKSET)",len(cpuarvaukset))
            if len(cpuarvaukset)==0:
                if suunta == "10" or suunta == "-10":
                    index1 = osumaxindex - 1
                    index2 = osumaxindex + 1
                    index3 = osumaxindex2 - 1
                    index4 = osumaxindex2 + 1
                    if index2 >= len(kordx)-1 and index4 >= len(kordx)-1: 
                        cpuarvaukset = [kordxr[index1]+str(osumay),kordxr[index3]+str(osumay)]

                    elif index2 >= len(kordx)-1:
                        cpuarvaukset = [kordxr[index1]+str(osumay),kordxr[index3]+str(osumay),kordxr[index4]+str(osumay)]

                    elif index4 >= len(kordx)-1:
                        cpuarvaukset = [kordxr[index1]+str(osumay),kordxr[index2]+str(osumay),kordxr[index3]+str(osumay)]

                    else:
                        cpuarvaukset = [kordxr[index1]+str(osumay),kordxr[index2]+str(osumay),kordxr[index3]+str(osumay),kordxr[index4]+str(osumay)]
                    #print("CPU arvaukset tehty osuma2 tarkastelussa",cpuarvaukset)
                elif suunta =="01" or suunta == "0-1":
                    yosa1 = osumay - 1
                    yosa2 = osumay + 1
                    yosa3 = osumay2 - 1
                    yosa4 = osumay2 + 1
                    cpuarvaukset = [osumax+str(yosa1),osumax+str(yosa2),osumax+str(yosa3),osumax+str(yosa4),]
                    #print("CPU arvaukset tehty osuma2 tarkastelussa",cpuarvaukset)
            elif len(cpuarvaukset)==1:
                cpuosu2=False
                cpuviimeksiosu=False

            okarvaukset = []
            #print("cpu arvaukset osuman jälkeen2", cpuarvaukset)
            
            for elem in cpuohi:
                for tehtyarvaus in cpuarvaukset:
                    if elem == tehtyarvaus:
                        arvausok == False
                        sama = True
                        index = cpuarvaukset.index(tehtyarvaus)
                        del cpuarvaukset[index]
                   
            #print("ok arvaukset2", cpuarvaukset)

            #tarvitsen arvauksen randomoituna hyvien arvausten listasta
            arvaus = random.choice(cpuarvaukset)

            for elem in cpuohi:
                if elem == arvaus:
                    arvausok == False
                    sama = True
        
            for laiva in laivat:
                if laiva[0] == arvaus:
                    if laiva[1] == 1:
                        #Tulikin ongelma kuinka kirjoitin ohjelman. Koska laitoin "laivoihin" tiedon milloin osuttu, nyt jos 
                        print("Sama naatti cpuosuma2",arvaus)
                        samaboat = True
                        index = cpuarvaukset.index(arvaus)
                        del cpuarvaukset[index]
                    
                    else:
                        laiva[1] = 1
                        osui = True
                        arvausok = True
                        cpuosumakohta = arvaus
                        #pitääkö vaihtaa toiseen osu viimeksi ? katsoa osumakohta ja sen perusteella  on 2 vaihtoehtoa
                        #Pitääkö lopulta iskee falseksi, jos oletetaan laivan tuhoutuneen? 
                        cpuviimeksiosu = True
                        cpuosu2 = False
                        
            if osui == False:
                sama = False
                if samaboat == True:
                    sama=True
                for elem in cpuohi:
                    if arvaus == elem:
                        print("Sama naatti2")
                        sama = True
                if sama == False:       
                    cpuohi += [arvaus]
                    arvausok = True
            cpuosumat = 0
            print(cpuohi)
            for laiva in laivat:
                if laiva[1] == 1:
                    print(laiva[0])
                    cpuosumat += 1
            if arvaus in cpuarvaukset:
                indeksi = cpuarvaukset.index(arvaus)
                del cpuarvaukset[indeksi]
            #print("tehtyä arvauslistaa osuman jälkeen olemassa 2", cpuarvaukset)
            if len(cpuarvaukset)==0:
                cpuviimeksiosu = False
            #print("cpuosumat 2",cpuosumat)
            #print("VIIMEKSI OSU 2", cpuviimeksiosu)

        #alkuperäinen randomilla etsittävä, muutettu randomia. Vähän hassu mutta en koske vielä
        elif koordinaattix != " ":
            arvaus = koordinaattix+koordinaattiy
            for elem in cpuohi:
                if elem == arvaus:
                    arvausok == False
                    sama = True
        
            for laiva in laivat:
                if laiva[0] == arvaus:
                    if laiva[1] == 1:
                        #print("Sama naatti")
                        samaboat = True
                    else:
                        laiva[1] = 1
                        osui = True
                        arvausok = True
                        cpuviimeksiosu = True
                        cpuosumakohta = arvaus
            if osui == False:
                sama = False
                if samaboat == True:
                    sama=True
                for elem in cpuohi:
                    if arvaus == elem:
                        #print("Sama naatti")
                        sama = True
                if sama == False:       
                    cpuohi += [arvaus]
                    arvausok = True
            cpuosumat = 0
            print(cpuohi)
            for laiva in laivat:
                if laiva[1] == 1:
                    print(laiva[0])
                    cpuosumat += 1
            #print("cpuosumat",cpuosumat)


def tallennusfunk(toiminto):
    global ohi
    global laivat
    global cpulaivat
    global cpuviimeksiosu 
    global cpuosu2 
    global cpuosumakohta
    global cpuosumakohta2
    global cpuarvaukset 
    global cpuohi
    print("Toiminto saatu", toiminto)
    #tallennuksenlataus = input("Aloitetaanko tallennuksesta?y/n")
    if toiminto == "y":
        pygame.event.get()
        database = sqlite3.connect("laivasave.db")
        cursor = database.cursor()
        cursor.execute("SELECT * FROM Save")
        rows = cursor.fetchall()
        #muistiksi missä järjestyksessä rowit on
        #(0ID INT, 1 LAIVAT BLOB, 2 CPULAIVAT, 3 OHI, 4 CPUOHI ,5 CPUARVAUS ,6 CPUOSU INTEGER,7 CPUOSU2 INTEGER,8 CPUOSUMAKOHTA BLOB,9 CPUOSUMAKOHTA2);")
        print("Seuraavaksi luetut tallenteet")
        print(rows)
        laivat = ast.literal_eval(rows[0][1])
        print("laivojen lista",laivat)
        print(type(laivat))
        cpulaivat = ast.literal_eval(rows[0][2])
        print("cpulaivojen lista",cpulaivat)
        ohi = ast.literal_eval(rows[0][3])
        print(ohi)
        cpuohi = ast.literal_eval(rows[0][4])
        #ongelma ei ymmärrä mennä kohtaan cpuosu2 kohtaan onko vika täällä? Pitääkö ottaa mukaan joku 3. muuttuja jota en muistanut?
        cpuviimeksiosu = rows[0][6]
        cpuosu2 = rows[0][7]
        cpuosumakohta = rows[0][8]
        cpuosumakohta2 = rows[0][9]
        cpuarvaukset = ast.literal_eval(rows[0][5])
        database.close()
    else:
        laivojenasettelu(laivat)   
        cpulaivojenasettelu(cpulaivat)

def tekstinaytto(nayttoteksti, x= 0, y= 0):
    teksti = NUM_FONT.render(nayttoteksti, True, (0, 0, 0))
    WIN.blit(teksti,(x ,y))
    pygame.display.flip()


def aloitusloop(funk):
        lopetaaloitus = False
        global lopeta
        toiminto = 0
        go = False
        if funk == 2:
            drawaloitus(2)
            teksti = "Aloitetaanko tallennuksesta?"
        elif funk == 4:
            drawaloitus(4)
            teksti = "Montako laivaa?"
        #jos vois jälleenkäyttää tätä?
        elif funk == 1:
            go = True

        while lopetaaloitus==False:
            if go == True:
                laudanpiirto()
                draw()
                go=False
            #Pygame looppaa eventtiä niin kauan kunnes jotain tapahtuu
            for event in pygame.event.get():
                tekstinaytto(teksti)
                for but in buttonarray:
                    if but.draw_button():
                        toiminto = but.text
                        print("BUTTONIN SELF TEXTIÄ PAINETTU", toiminto)
                if toiminto == "Exit":
                    lopeta = True
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.quit:
                    lopetaaloitus = True
                    lopeta = True
                    break 
                if toiminto != 0 and toiminto != None:
                #go pitää mennä napin painalluksen taakse
                    return toiminto
                    go = True


#tehdään pisteytys "laivakoko", ja ...

def main():
    global ohi
    global grafarray
    global laivat
    global cpulaivat
    global cpuviimeksiosu 
    global cpuosu2 
    global cpuosumakohta
    global cpuosumakohta2
    global cpuarvaukset 
    global cpuohi
    global lopeta
    global buttonarray
    global arvaus
    arvaus1 = 0
    global pelialoitettu
    #aloitus funktio johonkin tähän
    
    tallennusfunk(aloitusloop(2))
    grafarray = []
    buttonarray = []
    #laivojen asettelu tänne
    pelialoitettu = True
    laivakoko=len(laivat)
    pygame.event.clear()
    go = True
    while lopeta==False:
        
        if go == True:
            cpulaudanpiirto()
            laudanpiirto()
            draw()
            go=False
        #asodjknasidub täänne jos laittaa liia monta drawia niin se jää hengaa looppiia dsad asdasdas
        
        for event in pygame.event.get():
            tekstinaytto("Klikkaa koordinaattia", 400, 50)
            for but in buttonarray:
                if but.draw_button():
                    arvaus1 = but.text
                    print("BUTTONIN SELF TEXTIÄ PAINETTU", arvaus1)
            
            if event.type == pygame.quit:
                lopeta = True
                pygame.quit()
                sys.exit()
            #tämäpä ohje ei saata toimia. Jospa tekis drawissa nappuloita laatikoista?
            #MITÄ HELVETTIÄÄ NYT SAAN TEKSTIÄ NAPPULOIHI MUTTA KUINKA SAAN NAPPULAN RETURNAA ASUOIDHASIUDHASIOUYGHD
            if arvaus1 != 0 and arvaus1 != None:

                #TÄYTYY LÖYTÄÄ OIKEA BUTTONI LISTASTA?
                print("arvauksen tyyppi",type(arvaus1))
                #pudotetaan vanha buttonarray pois koska sitä ei enää tarvita! Tehdään uusi ettei pysty painamaan samoja näppäimiä
                buttonarray = []
                arvaus = arvaus1
                osumat = 0
                samaboat = False
                print("ARVAUS KLICKIN jälkeen", arvaus)
                
                """
                print("button array", buttonarray)
                for but in buttonarray:
                    print(but.text)
                print("grafarray", grafarray)
                """

                grafarray = []
                #arvaus = input("Anna koordinaatti muodossa kirjain numero (a1)(Lopetus 0, Tallennus ja Lopetus 1)")
                
                if arvaus == "Exit":
                    lopeta = True
                    pygame.quit()
                    sys.exit()
                elif arvaus == "Tallenna ja Lopeta":
                    tallennus()
                    lopeta = True
                    pygame.quit()
                    sys.exit()
                else:
                    osui = False
                    for laiva in cpulaivat:
                        if laiva[0] == arvaus:
                            if laiva[1] == 1:
                                print("Sama naatti")
                                samaboat = True
                            else:
                                laiva[1] = 1
                                osui = True
                    if osui == False:
                        sama = False
                        if samaboat == True:
                            sama=True
                        for elem in ohi:
                            if arvaus == elem:
                                print("Sama naatti")
                                sama = True
                        if sama == False:       
                            ohi += [arvaus]


                    print(ohi)
                    #täällä lasketaan pisteet kuinka monta osunu
                    for laiva in cpulaivat:
                        if laiva[1] == 1:
                            print(laiva[0])
                            osumat += 1
                    print("osumat",osumat)
                    cpuarvausfunk()
                    if osumat >= laivakoko:
                        lopeta = True
                        print("voitit pelin")
                        grafarray = []
                        cpulaudanpiirto()
                        laudanpiirto()
                        draw()
                        tekstinaytto("VOITIT PELIN", 400, 50)
                        time.sleep(3)
                        break
                    if cpuosumat >= laivakoko:
                        lopeta = True
                        print("Tietokone voitti pelin")
                        grafarray = []
                        cpulaudanpiirto()
                        laudanpiirto()
                        draw()
                        tekstinaytto(" Tietokone VOITTI PELIN", 400, 50)
                        time.sleep(3)
                        break
                go = True
                arvaus1 = 0

            
main()
cpulaudanpiirto()
laudanpiirto()

print(len(laivat))