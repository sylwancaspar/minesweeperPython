# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 10:14:47 2018

@author: Admin
"""
# Programmeringsteknink webbkurs KTH Slutinlämning.
#<Caspar Sylwan>
#2017-02-16

"""Struktur programmet är uppdelat i fem delar:
1.Bibliotek, 2.Globala variabler, 3.klasser och metoder till denna, 4. Övriga klasser, 5. Funktioner.
Klasser börjar med storbokstav, variabler liten bokstav på första ordet men stor på efterföljande ord.
Funktioner är helt med småbokstäver, metoder med bindesträk. lokala variabler i funktioner med små bokstäver."""

from tkinter import *# Skapar knappar och gör det möjligt att spela med musen.
from time import *# Skapar tiden
from random import randint# slumpar ut bomber.

sek=0# Dessa två har jag gjort här för att två spel inte ska spelas samtidtigt.
pågående=False# Därför är de globala.

   
class Minröj:#Här skapas Minröj som en class
    def __init__(self,rader=9,kolumner=9,bomberLiten=9):
        
        """ Här under delar jag upp huvudfönsteret i flera delar så att det ska bli lättare lägga ut olika funktioner."""
        self.master=Tk()
        self.master.title("MINRÖJ av CASPAR SYLWAN")
        self.master.geometry('{}x{}'.format(250, 100))
        
        self.ramupp=Frame(self.master,width=450, height=50, pady=3)#Uppe
        self.rammitt=Frame(self.master,width=50, height=40, padx=3, pady=3)#Mitten
        self.ramner=Frame(self.master, width=450, height=45, pady=3)#Nere
        self.ramupp.grid(row=0, sticky="ew")
        self.rammitt.grid(row=1, sticky="nsew")
        self.ramner.grid(row=3, sticky="ew")


        """ Dessa är variabler handlar om att spara namn och topplistan."""
        
        self.skrivDittNamnrubrik=Label(self.ramupp,text="Skriv ditt namn:  ")
        self.namn=StringVar()# Variabeln som sparar spelarens namn.
        self.skrivDittNamn=Entry(self.ramupp,textvariable=self.namn, width=12,bg="white",fg="black")#Spelaren kan skriva sitt namn.
        self.skrivNamn=Label(self.ramupp, textvariable= self.namn.get())# Sparar Tkintervariabler som string.
        self.knappNamn=Button(self.ramupp, text="Spara",command = self.spara )#Sparar namn
        self.toppListan=[]# Används för att sortera och spara topplistan.
        self.toppAlla=[]# Används för att sortera och spara topplistan.
        self.undoToppAlla=Button(self.ramupp, text="OK", command= self.undo_topp)#Tar bort beskrivningen
        
        self.topplistaKnapp=Button(self.ramupp, text="Topp\n listan",command = self.topp_alla )
        self.topplistaKnapp.grid(row=1,column=2)
        
    
        """ Variabler för vinst och förlust"""
        self.vinstRubrik=Label(self.ramner,text="GRATTIS DU VANN!!!",fg="red" )#Rubriken som skrivs när spelaren vinner.
        self.gameOver=Label(self.ramupp,text="GAME OVER",fg="red" )# Gameover är ett engelsktord men har använts så mycket att det nu mera betraktas som ett svenskt i många ordböker.
        
        self.snabbaste= Text(self.ramner, height=30, width=150, bg="white")#Texten som topplistan skrivsut på.
        
        
        """ Här under samlas variabler om hur spelet går till. Beskrivningen kommer från uppgiftsbeskrivningen."""
        
        info="Trots att det är riskfyllt tänker Osquar sommarjobba som minröjare.\
              \nTillsammans med sin minhund Trofast går inte Osquar på en endaste mina.\
              \nInnan Osquar och Trofast kommer till en plats ger nämligen\
              \nTrofast skall lika många gånger som det ﬁnns minor runt platsen.\
              \nPå så sätt kan Osquar bedöma vart han och Trofast skall gå härnäst.\
              \nTrofast, som är en röjig hund vill gärna känna vittringen av minor.\
              \nSkulle det vara så att det inte ﬁnns någon mina i närheten springer\
              \nhan runt och nosar upp minorna runt omkring.\
              \nHelt tomma ytor genomsöks automatiskt av Trofast.\
              \nOsquar får lugnt vänta på sin röjande kamrat.\n\
              \nDET MÅSTE GÅ FORT!"

        self.beskrivning= Text(self.ramner, height=30, width=150, bg="white")# Texten spelbeskriving.
        self.beskrivning.insert(END,info)#Tömmer beskrivningen på text.
        
        self.knappInfo=Button(self.ramupp, text="INFO \nspelregler",command= self.info)#Knappen som plockar fram spelbeskrivingen.
        self.knappInfo.grid(row=1,column=3)#Placerar knappen på startsidan.   
        
        self.undoBeskrivning=Button(self.ramupp, text="OK", command= self.ta_bort)#Tar bort beskrivningen

        
        """ Här under finns variabler om att starta spelet med topplista. För att spelaren inte ska kunna fuska är topplistan satt till 9x9 matris med 9 bomber."""
        
        self.litenSpelPlanKnapp=Button(self.ramupp, text="Liten\n spelplan", command=self.nytt_parti)#Knappen som startar den lilla spelplanen med topplistan.
        self.litenSpelPlanKnapp.grid(row=1,column=0)
        self.hem=Button(self.ramupp, text="Hem",command=self.hem)#Knappen som tar spelaren tillbaka till start sidan.
        self.rader=rader#Förbestämda rader till topplistan.
        self.kolumner=kolumner#Förbestämda kolumner till topplistan.
        self.bomberLiten=bomberLiten#Förbstämda bomber till topplistan.
        
        """ Här finns variabler för att välja storlek själv. Utan topplista eftersom noll bomber är ett möjligt alternativ."""
        
        self.väljStorlekKnapp=Button(self.ramupp,text="Välj \nstorlek",command=self.välj_storlek)#Knappen som ger möjlighet till att välja storlek själv.
        self.väljStorlekKnapp.grid(row=1,column=1)
        
        self.n= IntVar()# Här lagras variabler om spelaren vill göra en nxm spelplan.
        self.m= IntVar()# Här lagras variabler om spelaren vill göra en nxm spelplan.
        self.bomber=IntVar()#Hur många bomber som spelaren vill lägga ut.
        self.ni=9# Denna variabel sparar antalrader från spelaren, i står fri. 
        self.mi=9# Denna sparar antal kolumner från spelaren, i står fri.
        self.bomberi=9# Denna spelare sparar antal bomber från spelaren, i står fri. 
        self.nRader=Entry(self.ramupp,textvariable=self.n,bg="white",fg="black",width=10)#Där man skriver in antal rader.
        self.mKolumner=Entry(self.ramupp,textvariable=self.m,bg="white",fg="black",width=10)#Där man skriver in antal Kolumner.
        self.skrivBomber=Entry(self.ramupp,textvariable=self.bomber,bg="white",fg="black",width=10)
        self.nRubrik=Label(self.ramupp,text="Skriv hur många rader du vill ha :")#Rubriken till hur många rader.
        self.mRubrik=Label(self.ramupp,text="Skriv hur många kolumner du vill ha :")
        self.bombRubrik=Label(self.ramupp,text="Välj antal bomber:  ")#Rubriken till frågan om hur många bomber som ska läggas ut.
        self.sparaNKnapp=Button(self.ramupp,text="SPARA",command=self.n_spara)#Knappen som sparar det som spelaren skriver in.
        self.sparaMKnapp=Button(self.ramupp,text="SPARA",command=self.m_spara)
        self.bombKnapp=Button(self.ramupp,text="Spara", command=self.bomb_spara)
        self.friStorlekStartKnapp=Button(self.ramupp,text="STARTA", command=self.starta_fri_storlek)
        self.friStorlek=False# Denna gör att programmet vet om det är fri storlek eller med topplista. 
        self.felValavStorlek=Label(self.ramupp, text="Siffra mella 1 och 20 och inte fler minor än rutor!")#Rubriken som skrivs ut om spelaren gör ett otillåtetval.
        
        """ Tid"""
        self.klocka = Label(self.ramupp, text=str(sek), fg="black")# Klockan som en label till litenspelpaln.

        """ Installerar loopen i Classen. """
        self.master.mainloop()# Loopen läggs i klassen. 
        
        
    def spara(self):
        """Sparar namn till topplistan."""
        
        namn=self.namn.get()#Sparar spelarens namn i en lokal variabel.
        self.skrivNamn.grid(row=1,column=1)
        self.skrivDittNamn.delete(0, 'end')#Tar bort all text sedan tidigare.
        tabortfrångrid(self.skrivDittNamn,self.skrivDittNamnrubrik,self.knappNamn,0,0,3)#Funktionen tarbort appar från griden och undviker kod upprepningar.
        topplista(self.toppListan,namn)#Funktionen lägger in namn och tid i topplistan.
        
    
    def info(self):
        """Ger info om spelet"""
        
        self.master.geometry('{}x{}'.format(600, 400))#Ändrar storlek så att spelaren känner att det varit ett sid byte.
        self.beskrivning.grid(row=0,column=0)#Skapar infon
        self.undoBeskrivning.grid(row=1,column=4)# Skapar knappen för att ta bort infon.
        tabortfrångrid(self.knappInfo,self.topplistaKnapp,self.litenSpelPlanKnapp,self.väljStorlekKnapp,0,4)#Funktionen tarbort appar från griden och undviker kod upprepningar.
        
    def ta_bort(self):
        """Tar bort beskrivningen av spelet"""
        
        self.master.geometry('{}x{}'.format(230, 100))#Ändrar storlek så att spelaren känner att det varit ett sid byte.
        self.beskrivning.grid_remove()
        self.undoBeskrivning.grid_remove()
        placeraknappar(1,0,self.litenSpelPlanKnapp,self.väljStorlekKnapp, self.topplistaKnapp,self.knappInfo)#Funktionen undviker kod upprepning och placerar ut knappar.
        
    def välj_storlek(self):
        """ Om spelaren vill välja storlek själv och trycker han in raderna."""
        tabortfrångrid(self.topplistaKnapp,self.knappInfo,self.litenSpelPlanKnapp,self.väljStorlekKnapp,0,4)#Funktionen tarbort appar från griden och undviker kod upprepningar.
        placeraknappar(1,0,self.nRubrik,self.nRader,self.sparaNKnapp,0,3)#För att undvika kodupprepning.
        self.master.geometry('{}x{}'.format(300, 50))#Ändrar storlek så att spelaren känner att det varit ett sid byte.
        
    def n_spara(self):
        """Kontrollerar att raderna är rätt ochs sparar kolumnerna när spelaren får välja själv."""
        try:# Om spelaren matar in något som inte ska vara där så kommer ett felmedelande.
            self.ni=self.n.get() # Lägger in rad storleken i en ny variabel.
            if self.ni > 0 and self.ni < 20:# Rad längden får inte var mer än 20 och under 0.
                tabortfrångrid(self.nRubrik,self.nRader,self.sparaNKnapp,self.felValavStorlek,0,4)#Funktionen tarbort appar från griden och undviker kod upprepningar.
                placeraknappar(1,0,self.mRubrik,self.mKolumner,self.sparaMKnapp,0,3)
                self.master.geometry('{}x{}'.format(500, 50))#Ändrar storlek så att spelaren känner att det varit ett sid byte.
            else:
                self.felValavStorlek.grid(row=0,column=0)
                self.master.geometry('{}x{}'.format(500, 150))#Ger plats åt felmeddelandet.
                
        except:
            self.felValavStorlek.grid(row=0,column=0)
            self.master.geometry('{}x{}'.format(500, 150))#Ger plats åt felmeddelandet.
                
        
    def m_spara(self):
        """Spara raderna när spelaren får välja själv."""
        try:# Om Spelaren skriver in något annat än heltal kommer ett fel medelande upp.
            self.mi=self.m.get()# Lägger in kolumn storleken i en ny variabel.
            if self.mi > 0 and self.mi < 20:#Inte längre än 20 och mindre än noll.
                tabortfrångrid(self.mRubrik,self.mKolumner,self.sparaMKnapp,self.felValavStorlek,0,4)#Funktionen tarbort appar från griden och undviker kod upprepningar.
                placeraknappar(1,0,self.bombRubrik,self.skrivBomber,self.bombKnapp,0,3)
                self.master.geometry('{}x{}'.format(350, 100))#Ger plats åt felmeddelandet.
            else:
                self.felValavStorlek.grid(row=0,column=0)
                self.master.geometry('{}x{}'.format(500, 150))
        except:
            self.felValavStorlek.grid(row=0,column=0)
            self.master.geometry('{}x{}'.format(250, 150))
            
    def bomb_spara(self):
        """Kontrollerar att rätt antal bomber och inga bokstäver."""
        
        try:# Om Spelaren skriver in något annat än heltal kommer ett fel medelande upp.
            self.bomberi=self.bomber.get()# Lägger in bomber i en ny variabel.
            if self.bomberi>=0 and self.bomberi<(self.ni * self.mi):#Om det blir fler bomber än spelrutor.
                tabortfrångrid(self.bombRubrik,self.skrivBomber,self.bombKnapp,self.felValavStorlek,0,4)#Funktionen tarbort appar från griden och undviker kod upprepningar.
                self.friStorlekStartKnapp.grid(row=0,column=0)
            else:
                self.felValavStorlek.grid(row=0,column=0)
        
        except:
            self.felValavStorlek.grid(row=0,column=0)
            self.master.geometry('{}x{}'.format(500, 150))
        
    def starta_fri_storlek(self):
        
        """ Startar parti där spelaren får välja storlek och antal bomber själv. Valen är redan gjorda i metoderna ovan."""
        self.friStorlek=True# Medelar programmet att det är fri allternativet som gäller.
        tabortfrångrid(self.bombKnapp,self.bombRubrik,self.skrivBomber,self.gameOver,self.vinstRubrik)#Funktionen tarbort appar från griden och undviker kod upprepningar.
        self.hem.grid(row=0,column=1)#Om spelaren önskar att gå tillbaka till startsidan
        färg="grey"# Installerar grå som grundfärg. 
        plan=spelplan(self.ni,self.mi)#Funktionen målar upp spelplanen efter valen som spelaren gjort.
        self.master.geometry('{}x{}'.format((self.mi*40+40), self.ni*40+60))#Anpassar storleken efter matris storlek.
        plan=placerabomber(self.bomberi,plan)# Slumpar ut antalet bomber spelaren valt. 
        for i in range(self.ni):
            for j in range(self.mi):#Denna skriver ut knapparna så att spelplanen blir synlig.
                Grid.columnconfigure(self.rammitt, j, weight=0)
                spelruta=Button(self.rammitt,text="   ",bg=färg,fg="black")# Målar upp rutorna, knapparna som är länkade till spelplanens matrisen.
                spelruta.grid(row=i,column=j, padx=1,pady=1,sticky=N+S+E+W)
                spelruta.bind("<Button-1>",lambda e,i=i,j=j: self.minfältet(plan,i,j,e))
                spelruta.bind("<Button-3>",lambda e,i=i,j=j: self.flagga(plan,i,j,e))
                    
                
    def nytt_parti(self):
        """Lägger ut spelplanen, placerar bomber, startar klockan, påbörjar spelet"""
        """Denna startar spel med topplista. Inte fri storlek."""
#        global pågående
        global sek # Tillåter metoden att få tillgång till den globala variabeln.
        self.friStorlek=False # Medelar funktionen att det är standard värden topplista som gäller.
        tabortfrångrid(self.knappInfo,self.väljStorlekKnapp,self.gameOver,self.vinstRubrik,self.skrivDittNamnrubrik,5)#Funktionen tarbort appar från griden och undviker kod upprepningar.
        tabortfrångrid(self.skrivDittNamnrubrik,self.skrivDittNamn,self.knappNamn,self.topplistaKnapp,0,4)#Funktionen tarbort appar från griden och undviker kod upprepningar.
        self.master.geometry('{}x{}'.format(200, 450))
        self.klocka.grid(row=0,column=3)
        nollställ(self.klocka)# Nollställer klockan för ett nytt spel.
        tidrubrik(self.klocka)
        startatiden(self.klocka)
        self.hem.grid(row=0,column=0)#Lägger ut startknappen så att spelaren kan ta sig till första sidan.
        färg="grey"
        plan=spelplan(self.rader,self.kolumner)#Bygger spelplanen!
        plan=placerabomber(self.bomberLiten,plan)#Placerar ut bomber på planen.
        for i in range(self.rader):#Lägger ut knapparna så att planen blir synlig.
            Grid.rowconfigure(self.rammitt, i, weight=0)
            for j in range(self.kolumner):
                Grid.columnconfigure(self.rammitt, j, weight=0)
                spelruta=Button(self.rammitt,text="   ",bg=färg,fg="black")
                spelruta.grid(row=i,column=j, padx=1,pady=1,sticky=N+S+E+W)
                spelruta.bind("<Button-1>",lambda e,i=i,j=j: self.minfältet(plan,i,j,e))
                spelruta.bind("<Button-3>",lambda e,i=i,j=j: self.flagga(plan,i,j,e))
                
                
    def hem(self):
        """ Denna tar användaren till första sidan."""
        stopp(self.klocka)
        nollställ(self.klocka)
        tabortfrångrid(self.felValavStorlek,self.klocka,self.hem,self.vinstRubrik,self.gameOver)#Funktionen tarbort appar från griden och undviker kod upprepningar.
        tabortfrångrid(self.skrivNamn,self.knappNamn,self.skrivDittNamn,self.friStorlekStartKnapp,self.skrivDittNamnrubrik)#Funktionen tarbot kod upprepningar.
        placeraknappar(1,0,self.litenSpelPlanKnapp,self.väljStorlekKnapp, self.topplistaKnapp,self.knappInfo)#Funktionen lägger ut knappar och undviker kod upprepning.
        self.master.geometry('{}x{}'.format(250, 100))
        if self.friStorlek==False: # Om spelet innan var med topplista så skrivs knappar över den tidigare.
            for i in range(self.rader):
                for j in range(self.kolumner):
                    grey=Label(self.rammitt,text=" ")
                    grey.grid(row=i,column=j, padx=1,pady=1,sticky=N+S+E+W)
        else:#Om det var ett fritt val av storlek göms den här.
            for i in range(self.ni):
                for j in range(self.mi):
                    grey=Label(self.rammitt,text=" ")
                    grey.grid(row=i,column=j, padx=1,pady=1,sticky=N+S+E+W)
        
    def minfältet(self,plan,i,j,event):
        """Denna metod som tar hand om minfältet. Den tar hand om varje ruta finns det en bomb,angränsade bomb eller är det vinst. Det är denna metod som är spelet. Den är 46 rader lång och på gränsen till för lång. """ 
        if self.friStorlek==False:
            vinst=ärdetvinst(plan,self.bomberLiten)#Liten spelplan med topplista.
        else:
            vinst=ärdetvinst(plan,self.bomberi)#Utan topplista.
        if plan[i][j].bomb==False: # Om rutan inte innehåller några bomber.
            nbomber=0
            färg="white"
            if räknabomber(i,j,plan)!=0:# Om det finns en bomb bredvid.
                färg="green"#Grön om det finns en angränsande ruta.
                plan[i][j].synlig=True# Ändrar till synlig så att spelet inta ska haka upp sig.
                nbomber=räknabomber(i,j,plan)# Räknar bomber som finns runt och n står för antal.
                spelruta=Button(self.rammitt,text=nbomber,bg=färg,fg="black")#Gör om rutan och skriver hur många bomber den angränsar till.
                spelruta.grid(row=i,column=j)
                
                if self.friStorlek==False:# Med topplista
                    vinst=ärdetvinst(plan,self.bomberLiten)
                    if  vinst==0: #Det finns inga toma rutor kvar                   
                        stopp(self.klocka)
                        self.vinstRubrik.grid(row=2,column=2)
                        placeraknappar(2,0,self.skrivDittNamnrubrik,self.skrivDittNamn,self.knappNamn,0,3)
                elif self.friStorlek==True:# Om spelaren väljer att ha egen storlek
                    vinst=ärdetvinst(plan,self.bomberi)
                    if vinst==0:
                        self.vinstRubrik.grid(row=2,column=2)
            else:
                sök(i,j,plan,self.rammitt)#Söker efter den närmsta bomben!
                if self.friStorlek==False:
                    vinst=ärdetvinst(plan,self.bomberLiten)
                    if vinst==0: #Det finns inga toma rutor kvar.                    
                        stopp(self.klocka)
                        self.vinstRubrik.grid(row=2,column=2)
                        placeraknappar(2,0,self.skrivDittNamnrubrik,self.skrivDittNamn,self.knappNamn,0,3)
                else:#Fri storlek!
                    vinst=ärdetvinst(plan,self.bomberi)
                    if vinst==0:
                        self.vinstRubrik.grid(row=2,column=2)
        elif plan[i][j].bomb==True and self.friStorlek==False:#Med topplista
            """ Bomb game over """           
            stopp(self.klocka)
            färg="red"
            visabomber(self.rader,self.kolumner,plan,self.rammitt)#Visar var bomberna låg.
            self.gameOver.grid(row=2,column=2, padx=1,pady=1,sticky=N+S+E+W)
        elif plan[i][j].bomb==True and self.friStorlek==True:#Fri Storlek
            visabomber(self.ni,self.mi, plan, self.rammitt)#Visar var bomberna låg.
            self.gameOver.grid(row=2,column=2, padx=1,pady=1,sticky=N+S+E+W)
        
        
    def flagga(self,plan,i,j,event):
        """Med ett vänster klick går det att flagga en där det finns en bomb"""
        if plan[i][j].flagga==False:
            event.widget.config(text="B")#B för bomb.
            plan[i][j].flagga=True# Denna tar bort flaggan.
            if self.friStorlek==False:
                
                vinst=rättflagga(plan,self.bomberLiten)#Litenspelplan med topplista.
            
                if vinst==0 and self.friStorlek==False:#Med topplista
                    stopp(self.klocka)# Stoppar klockan så att topplistan kan börja användas.
                    self.vinstRubrik.grid(row=2,column=2)
                    placeraknappar(2,0,self.skrivDittNamnrubrik,self.skrivDittNamn,self.knappNamn,0,3)
                
            elif self.friStorlek==True:# Egen storlek utan topplista.
                 
                vinst=rättflagga(plan,self.bomberi)# Om vinst funtionen är noll betyder det alla bomber är hittade.
                
                if vinst==0:
                    self.vinstRubrik.grid(row=2, column=2)
                
        else:
            event.widget.config(text="   ")
            plan[i][j].flagga=False
            
            
    def topp_alla(self):
        """Denna Metod sorterar och skriver ut topplistan."""
        tabortfrångrid(self.knappInfo,self.topplistaKnapp,self.litenSpelPlanKnapp,self.väljStorlekKnapp,self.topplistaKnapp)
                
        topptio=[]#Två listor används för att sortera.
        self.toppAlla=[]
        try:
                
            with open('C:/Users/Admin/Desktop/Python/topplista1.txt') as f:
                
                for line in f:
                    sek,tid, namn = line.split(',')# Delar upp med komma.
                    sek = float(sek)# Gör om sek float från string.
                    topptio.append((sek,tid, namn))#Lägger in i lista.
    
                topptio.sort(key=lambda s: s[1])#Sorterar på sek.
                for sek, tid, namn in topptio:
                    tidnamn=(tid,namn)#Tid och namn är det som skrivsut.
                    tidnamn=" ".join(tidnamn)
                    self.toppAlla.append(tidnamn)
            self.toppAlla="".join(self.toppAlla)
            self.snabbaste.insert(END,self.toppAlla)
            f.close()
            self.snabbaste.grid(row=0,column=0)
            self.undoToppAlla.grid(row=1,column=4)
            self.master.geometry('{}x{}'.format(230, 400))    
                
        except FileNotFoundError:
            
            file=open('C:/Users/Admin/Desktop/Python/topplista1.txt','w')#Skapar en topplista.
            file.close()
            self.snabbaste.grid(row=0,column=0)
            self.undoToppAlla.grid(row=1,column=4)
            self.master.geometry('{}x{}'.format(230, 400))
            
    def undo_topp(self):
        """Denna Metod tar bort topplistan och sätter tillbaks knapparna."""
        self.snabbaste.delete(1.0,END)#Tömmer topplistanstext.
        placeraknappar(1,0,self.litenSpelPlanKnapp,self.väljStorlekKnapp, self.topplistaKnapp,self.knappInfo)#Funktionen undviker kod upprepning.
        self.snabbaste.grid_remove()
        self.undoToppAlla.grid_remove()
        self.master.geometry('{}x{}'.format(230, 100))
        
class Status:
    def __init__(self):
        """Denna beskriver statusen för varje ruta! Det vill säga om det finns en bomb OSV."""
        self.bomb=False# Denna bestämmer om rutan har en bomb eller inte.
        self.synlig=False# Vid klick på en tom ruta och vid flaggning behöver programmet veta om innehållet är avslöjat eller inte.
        self.flagga=False# Flaggning om spelaren tror att det finns en bomb.
    
def spelplan(n=9,m=9):
    """ Skapar en två dimisionell plan, med 9x9 som bas."""
    
    spelplan = [[Status() for x in range(m)] for y in range(n)]# Genom gående för används x,y-axeln och nxm matris.
    
    return spelplan


def placerabomber(bomber,spelplan):
    """Placerar ut bomber slumpvis. """
    
    bomb=0# Antal bomer som redan slumpats ut.
    n=len(spelplan[0])
    m=len(spelplan)
    while bomb<bomber:# Fortsätter slumpa ut bomber tills alla är ute.
        kol=randint(0,m-1)# Slumpfunktionen för kolumner.
        rad=randint(0,n-1)# Slumpfunktionen för rader.
        if spelplan[kol][rad].bomb==False:# Om det inte finns en bomb där sedan tidigare så placeras en ut.
            spelplan[kol][rad].bomb=True# Ändrar till bomb placerad.
            bomb+=1
            
    return spelplan

def tidrubrik(klocka):
    """ Följande fem fuktioner är klockan """
    
    global pågående# Denna variabel startar spelet.
    starten=time()# tid i millisekunder från 1970-talet
    def tid():
        
        if pågående==True:
            global sek
            
            sek=time()-starten # Tiden nu minus millisekunderna!
            tidStr=sätttid(sek) # Snyggar till utskriften!
            klocka['text']=tidStr #Ändrar tiden på label
            klocka.after(1000,tid) # Uppdaterar funktionen varje sekund.
            
    tid()
    
def sätttid(sek):
    """Denna funktion skriver om millisekundrarna till sekunder och minuter."""
    sekunder=int(sek)%60# Ger resten som blir över vid devision på 60.
    minuter=int(sek/60)# Ger heltalet som blir över vid devision vid 60.
    tidStr= "%02d:%02d" % (minuter, sekunder)# Skriver ut sekunder och minuter.
    return tidStr


def startatiden(klocka):
    """Ändrar status på klockan till start."""
    global pågående
    pågående=True
    tidrubrik(klocka)


def stopp(klocka):
    """Stoppar tiden"""
    global pågående
    pågående=False

def nollställ(klocka):
    """ Nollställer för nyttparti"""
    global sek
    sek=0

def spelplansgränser(x,y, spelplan):
    """Undersöker att rutorna runt är inom spelplanen""" 
    if x >= 0 and x<len(spelplan) and y >= 0 and y < len(spelplan[0]):# För att kontrollera gränser används x-axel och y-axel.
        return True # Om inom gränserna returneras sant.
    return False # Annars falskt! 

def räknabomber(i,j,plan):
    """Räknar hur många bomber som verkligen finns runt"""
    nbomber=0# Antal bomber.
    for (k,l) in [(0,1),(0,-1),(1,1),(-1,-1),(1,0),(-1,0),(-1,1),(1,-1)]:#Cirkel runt punten som klickats på.
                if spelplansgränser(i+k,j+l,plan) and plan[i+k][j+l].bomb==True:# Om det är inom spelplanensgränser och det finns en bomb så fylls en på.
                    plan[i+k][l+j]
                    nbomber=nbomber+1
            
    return nbomber
        

def sök(i,j,plan,ram):
    """Söker efter rutor som inte har bomber runt sig! Detta är en funktion som anropar sig själv."""
    
    nbomber=räknabomber(i,j,plan)#Räknar bomber
    k=0# Denna variabel flyttar en åt sidan.
    l=0# Denna variabel flyttar en åt sidan.
    färg="white"#Grundfärg för rutor som inte angränsar till någon bomb.
    while spelplansgränser(i+k,j+l,plan) and plan[i][j].synlig==False and plan[i][j].bomb==False:
                    """Kollar gränser om det finns bomber i närheten."""
                    nbomber=räknabomber(i+k,j+l,plan)
                    
                    if nbomber!=0 and spelplansgränser(i+k,j+l,plan):#Om det finns en bomb bredvid.
                        plan[i][j].synlig=True
                        färg="green"
                        spelruta=Button(ram,text=str(nbomber),bg=färg,fg="black")
                        spelruta.grid(row=i+k,column=j+l, padx=1,pady=1,sticky=N+S+E+W)
                        
                    
                    elif plan[i][j].synlig==True:#Om jag redan sökt rutan, så att jag inte fastnar.
                        break
                    
                    
                    else:
                        
                        plan[i][j].synlig=True
                        spelruta=Button(ram,text="  ",bg=färg,fg="black")
                        spelruta.grid(row=i+k,column=j+l, padx=1,pady=1,sticky=N+S+E+W)
                        for (k,l) in [(0,1),(0,-1),(1,1),(-1,-1),(1,0),(-1,0),(-1,1),(1,-1)]:#Cirkel runt rutan som tryckts på.
                            sök(i+k,j+l,plan,ram)#Anropar funtionen igen.

def ärdetvinst(spelplan,bomber):
    """Konrollerar om det är vinst via toma rutor"""
    m=len(spelplan)
    n=len(spelplan[0])#n står för rader och m kolumner. Standard att beskriva matriser med nxm inom matematiken.
    vinst=0# Variabel som räknar toma rutor till vinst.
    total=n*m - bomber#Rader gånger kolumner minus bomber föraeta hur många rutor som finns.
    for i in range(m):
        for j in range(n):
            if spelplan[i][j].synlig==True:
                vinst=vinst+1
    total=total-vinst# Om total är 0 så finns det inga toma rutor kvar.
    return total

def rättflagga(spelplan,bomber):
    """ Kontrollerar om det är vinst via flaggorna"""
    vinst=0# Variabel för räkna flaggor till vinst.
    n=len(spelplan[0])#n står för rader och m kolumner. Standard att beskriva matriser med nxm inom matematiken.
    m=len(spelplan)
    total=n*m - bomber#Antal tomma rutor utan bomber.
    fel_flagga=0#Räknar flaggor som inte är rätt placerade.
    for i in range(m):
        for j in range(n):
            if spelplan[i][j].bomb== True and spelplan[i][j].flagga==True:# Om flaggan är korrekt placerad.
                vinst=vinst+1# plusas på en.
            elif spelplan[i][j].bomb==False and spelplan[i][j].flagga==True and spelplan[i][j].synlig==False:# Om flaggan är felplacerad.
                fel_flagga=fel_flagga+1# plusas på en på fel.
    if fel_flagga==0:# Om inga flaggor är fel placerade. 
        
        vinst=vinst-bomber#Räknar antal kvar till att spelet är vunnet.
        return vinst#  Är denna 0 så är det vinst. 
    else:
        return 9# returnerar något som ite är vinst.
        

def topplista(topplistan, namn):
    """Sparar till topplistan.   """
    global sek
    topplistan=[]
        
    text= namn, sätttid(sek)
    try:# Om det finns en topplista så sparas den till den.
        file=open('C:/Users/Admin/Desktop/Python/topplista1.txt','a')
        file.write(str(sek))
        file.write(", ")
        file.write(sätttid(sek))
        file.write(",")
        file.write(namn)
        file.write("\n")
        file.close()
          
    except FileNotFoundError:# Om det inte finns någon så skapas den.
        file=open('C:/Users/Admin/Desktop/Python/topplista1.txt','w')
        file.write(str(sek))
        file.write(", ")
        file.write(sätttid(sek))
        file.write(",")
        file.write(namn)
        file.write("\n")
        file.close()
                
def visabomber(rader,kolumner,plan,ram):
    """Visar bomber vid förlust används för att undvika kodupprepning."""
    färg="red"
    for i in range(rader):
        for j in range(kolumner):
            if plan[i][j].bomb == True:
                spelruta=Button(ram,text="¤",bg=färg,fg="black")
                spelruta.grid(row=i,column=j, padx=1,pady=1)
                
def tabortfrångrid(variabel1,variabel2,variabel3,variabel4,variabel5,antal=5):
    """ Gör knappar och rubriker osynliga för användare. Har som främsta uppgift att undvika kodupprepning."""
    variabel1.grid_remove()
    variabel2.grid_remove()
    variabel3.grid_remove()
    if antal >= 4:# Gör det möjligt att välja antal.
        variabel4.grid_remove()
        if antal >= 5:# Gör det möjligt att välja antal.
            variabel5.grid_remove()
            
def placeraknappar(rad,kolumn,knapp1,knapp2,knapp3,knapp4,antal=4):
    """Placerar ut knappar och andra kontroller. Funktionens huvudsakliga uppgift är att undvika upprepning."""
    knapp1.grid(row=rad,column=kolumn)
    knapp2.grid(row=rad,column=kolumn+2)
    if antal>2:# Gör det möjligt att välja antal.
        knapp3.grid(row=rad,column=kolumn+3)
        if antal>3:# Gör det möjligt att välja antal.
            knapp4.grid(row=rad,column=kolumn+4)
            

Minröj()# Här aktiveras spelet
#%%