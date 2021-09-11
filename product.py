
class Produit(object):
   
    def __init__(self,nom,prix,lien, siteID,rate,type,imgsrc):

        self.nom=nom
        self.straintype=""
        self.prix=prix
        self.lien=lien
        self.rate=rate
        self.type=type
        self.indexInList=None 
        self.siteID=siteID
        self.imgsrc=imgsrc

    

    def __eq__(self, o):
            return self.lien.strip() == o.lien.strip()
    
    def __hash__(self):
        return hash((self.lien,self.nom))

    def __repr__(self):
        return (f"{self.nom} : {self.prix} : {self.lien} : {self.siteID}  : {self.rate} : {self.type}\n")

    def toString(self):
            print(f'{self.nom} {self.prix} {self.rate}')

    def getString(self):
        return ((f'{self.nom}---------{self.prix}---------{self.rate}---------{self.siteID}'))
    def getInfos(self):
        return(self.nom,self.type,self.prix,self.rate,self.lien,)



    def toDict(self):
        return {"nom":self.nom,"type":self.type,"prix":self.prix,"rate":self.rate,"site":self.siteID,"lien":self.lien,"imgsrc":self.imgsrc}