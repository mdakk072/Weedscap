from difflib import SequenceMatcher
import datetime
import validators
import requests
import bs4
import re
import datetime
import json
from product import Produit
import pickle
'''

WEEDSCRAP V.02 by Mounir Dakkak

'''

log = open("track.log", "a")

log.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!["+datetime.datetime.now().strftime("%d.%m.%Y %H-%M-%S")+"]!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")



class scrapScript :   
    '''
    init for the script contains :
    link of the website
    Found dict with booleans (to know if we already have the right tag and class )
    Touse dict to store the working tag and class
    also current variable to know where we're working 
    header for the requests 
    '''

    def __init__(self,link):
            print("===============================")
            print(" Welcome to Weed Scraper v 0.2")
            print("===============================")
            self.link=link
            if("www" in link.lower()):
                self.ID=link.split(".")[1]
            else:
                self.ID=link.split("//")[1].split(".")[0]
            log.write("=============================================working on "+ self.ID+" =============================================\n")
            print("working on "+ self.ID)
            self.Found={"name":False,"price":False,"link":False,"rate":False,"prodbox":False,"imgsrc":False}
            self.toUse={"name":None,"price":None,"link":None,"rate":None,"prodbox":None,"imgsrc":None}
            self.a=True
            self.currentCat=""
            self.currentPage=""
            self.currentBox=""
            self.headers = {'User-Agent': 'Chrome/50.0.2661.102'}
            self.prodcuts=[]







    '''

    method to scrap links from a cannabis website since every website is built diffently the best general way to get acces to all products
    is to take categories links  
            
    '''

    def findcategoryLinks(self):

        #here we have 2 lists on for cats and one for subcats
        liens=[]
        subliens=[]
        #here we have the possibilities found on most of weed websites after the .com/
        possibilite = ("product-category","buy-online","shop-online","online-dispensary")
        #here we have the possibilities found on most of weed websites for categories
        terminaison = ("/accessories/","/weed/","/flower/","/concentrates/","/edibles/","/cbd/","/vape/","/vapes/","/cannabis/","/hash/","/pens-vapes/",
        "cannabis-extracts")
        #here is the links that we dont want to get 
        faux=("Alberta","Calgary","Edmonton","Brampton","British Columbia","Guelph","Halifax","Hamilton","Manitoba","Nunavut","Montreal",
        "Oshawa","Prince Edward Island","Kelowna","Vancouver","Mississauga","Ontario",
        "Ottawa","Québec City","Toronto","Yukon","Saint John","Regina",
        "London","Saskatchewan","Saskatoon","St Catharines","Thunder Bay","Northwest Territories"
        ,"Gatineau","Barrie","Windsor","Dartmouth","Cambridge","Winnipeg","Kitchener","grade","brands","new-arrivals","best-seller","new-arrivals","all-products","sale",
        "ounce-specials","mix-and-match",
        "back-in-stock","new","orderby","flash","best","most","merch","happy","clearance","sugar","ounces",'deals')
        #we start by doing a request to the website using fake haders !important 
        #after that we parse with bs4 and we find all the a tags which contains the href links
        resp=requests.get(self.link,headers=self.headers)
        soup=bs4.BeautifulSoup(resp.text,"html.parser")
        em=soup.find_all("a")
        #counter for cats and subcats
        cat , subcat = 0, 0

        #we loops into the found links
        for e in em:

            #we grab the href from the a tag 
            
            try:
                lien=e["href"].strip()
                lien=str(lien)
            except:
                log.write("["+datetime.datetime.now().strftime("%d.%m.%Y %H-%M-%S")+"] "+f"no href found in {self.ID} at\n" )
                log.write(lien)
                log.write('\n')
                continue
            #valid boolean using validators to check if is a working url
            valid=validators.url(lien)
            # i really dunno why i've wrote it this way but its working lol
            #check if url is already here 
            isNotHere=not(lien in (item for sublist in liens+subliens for item in sublist))
           #First statement to check if the url ends with a valid terminaison and is valid and is not already in the list 
            if any(x.lower() in lien.lower() for x in possibilite+terminaison)  and valid and isNotHere :
             #example url :https://lol.cc/product-category/cbd/
             #/product-category/ is in possibilite
             #it has 5 "/" and  there is no faux  in the url
                if any(z.lower() in lien.lower() for z in possibilite) and lien.count("/")==5 and not any(i.lower() in lien.lower() for i in faux):
                    cat+=1
                    #check if is not a suitable category 
                    #write cats and subcats in log file
                    if(not any(i.lower().strip() in e.text.strip().lower() for i in faux)):
                        liens.append([e.text.strip(),lien])
                        log.write("----------------------------------Categorie : "+e.text.strip()+" :  "+lien+"\n")
                    else:
                        log.write("unwanted cat---------------------------------- "+e.text.strip()+" :  "+lien+"\n")


                

                elif(lien.endswith(terminaison) and len([ele for ele in terminaison if(ele in lien)])==1):
                    liens.append([e.text.strip(),lien])
                    cat+=1
                    log.write("----------------------------------Categorie : "+e.text.strip()+" :  "+lien+"\n")
                else:
                    subcat+=1
                    subliens.append([e.text.strip(),lien])
                    log.write("----------------------------------SUB-Categorie : "+str(e.text.strip().encode())+" :  "+str(lien.encode())+"\n")
                   # print("--SUBcategorie : "+e.text.strip()+" :  "+lien)
        print("found "+str(cat)+" categories")
        log.write("found "+str(cat)+" categories \n")
        
        print("found "+str(subcat)+" Sub-categories")
        log.write("found "+str(subcat)+" Sub-categories"+'\n')
        
        #return categories links in  :   [[category,link]]  
        # list of lists with category and link
        return liens 
    
    '''
helps to finds the boxes which contains the products infos (rate, price , picture , name etc...)

input a link and output a list of product boxes 
 we use the list to extract products infos from a page 

    '''
  

    def findprodBox(self,link):

        #here is diffents tags and classes that  most of cannabis websites use for their products
        places=(("div",{"class":"product-wrapper"}),
        ('a',{'class':'prod-box'}),
            ("div", {"class":"product-small box"}),
        ("div", {"class":"product-item-inner"}),
        "ul", {"class":"woo-entry-inner clr"},
        ("div",{"class":"product-meta-wrapper"} ),
        ("div",{"class":"product-information"}),("div",{"class":"content-product-imagin"})
        )
    #we use bs4 to parse the html test
        soup=bs4.BeautifulSoup(link,"html.parser")
    #check if we already know the right tag and class for the website 
        isFound=self.Found["prodbox"]
    # if yes we directly  use the right tag/class which is saved in toUse dict
        if(isFound):
            place=self.toUse["prodbox"]
            box=soup.find_all(*place)
            
            return box
            
    #else we try them all till we find the right one
        else :
            for val,place in enumerate(places):
                box=soup.find_all(*place)
                if(len(box)!=0):
                    self.toUse["prodbox"]=place
                    self.Found["prodbox"]=True
                 
                    return box
                elif(val==len(places)-1):
                    
                    return []
    '''
   check if a link has pagination (page 1 2 3.....) 
   it doesnt gives the number of pagination tho

    '''
    def isIterable(self,link):
        #working with 2  links page 1 and 2 to check for the pagination
        litest=link+"page/2/"
        litestb=link+'page/1/'
 
        #first request for page 2 
        resp=requests.get(litest,headers=self.headers)

        #if request status code for page 2 is not 404 we still have to check for fake pagination
        if(resp.status_code!=404):
            #if not we make a request for page 1 and we check similarity in case of fake pagination
            respb=requests.get(litestb,headers=self.headers)

            # we extract prodbox from pages and we check match ration (generally greater than 0.8 for fake paginations)  
            a=self.findprodBox(resp.text)
            b=self.findprodBox(respb.text)
            match= SequenceMatcher(None,a,b).quick_ratio()

           

            if match>=0.8:
                log.write("WARNING-------- Suspect iteration in "+link+" sequanceMatch is "+'\n')
                
                return False   

            else :   
                return True
        #if request status code for page 2 is 404 there is no pagniation
        elif (resp.status_code==404):
           return False
        '''
         take a  category link and return list of resp texts with paginations 
        '''
    def getIterations(self,link):


        #check if link is iterable 

        if self.isIterable(link):
    #if so , we make requests till we get error 404 on page x

            link=link+"page/"
            i=1
            resp=requests.get(link+str(i),headers=self.headers)
            links=[]
            while resp.status_code!=404:
                links.append(resp.text)
                print(i,end="\r")
                print(f'found {i} pages',end='\r')
                i+=1
                resp=requests.get(link+str(i),headers=self.headers)
            print()

        else :
        #if page is not iterable we simply return the link itself
            links=[requests.get(link,headers=self.headers).text]
        
        return links

        '''
        method to set html texts in a dict so we can use it easily
        '''


    def setscrappingdata(self):
        #starting by finding the categories
        print('finding categories...')
        #storing categories
        catlinks=self.findcategoryLinks()
        # scrapdatas = Dict : {"cat":[iteration links html texts]}
        scrapdatas={}
        for cat in catlinks:
            print(f"getting iterations for {cat[0]}")
            #getting iteration from a link
            scrapdatas[cat[0]]=self.getIterations(cat[1])
            
# scrapdatas = Dict : {"cat":[iteration links html texts]}
        print('preparing datas done !')
        return(scrapdatas)
    '''
      find methods to extract datas we need from prodboxes 

      places variable where we store the possible tags and class where we can find the datas 

      isFound variable to check if we've already found the right place

      if so we just use it from toUse dict 
      else we iterate in places  to find the right one

    '''
        
    def findPrice(self,box):
        places=(("span",{"class":"woocommerce-Price-amount amount"}),
            ("span" ,{"class":"price"}),
        ("span",{"class":"woocommerce-Price-amount amount"}),)

        isFound=self.Found["price"]

        if(isFound):
            endroit=self.toUse["price"]
            try:
                em_price = box.find_all(*endroit)
                return em_price[0].text
            except Exception as e:

                #A REVOIR
                print(e)
                log.write("["+datetime.datetime.now().strftime("%d.%m.%Y %H-%M-%S")+"] "+f"can't find price on {self.ID} at {self.currentCat} : but method already found  why? \n" )
                return "N/A"
        else:
            

            for val ,endroit in enumerate(places):
                try:
                    em_price = box.find_all(*endroit)
                    if(len(em_price)!=0):

                        self.toUse["price"]=endroit
                        self.Found["price"]=True
                     #   print("had le site khdem feh prix :" )
                        return em_price[0].text

                except Exception as e :
                    if(val==len(places)-1):
                        log.write("["+datetime.datetime.now().strftime("%d.%m.%Y %H-%M-%S")+"] "+f"can't find price on {self.ID} at {self.ID}  endroit not found \n" )
                 #       print(e)
              #          print(traceback.format_exc())
                        return "N/A"
                    
    def findName(self,box):
        places=[("a",{"class":"woocommerce-LoopProduct-link woocommerce-loop-product__link"}),
        ("li",{"class":"title"}),
        ("h3",)]


        if self.Found["name"]==True:
            endroit=self.toUse["name"]
            try:
                
                em_price = box.find_all(*endroit)

                
                return em_price[0].text
            except  :
                log.write("["+datetime.datetime.now().strftime("%d.%m.%Y %H-%M-%S")+"] "+f"can't find NAME on {self.ID}  \n" )
                log.write(self.currentPage+"\n")
                return "N/A"

        else:




            for val ,endroit in enumerate(places):
                try:
                    em_price = box.find_all(*endroit)
                    if (len(em_price)!=0):
                        self.toUse["name"]=endroit
                        self.Found["name"]=True
                        print("had le site khdem feh nom :")
                        return em_price[0].text

                except Exception as e :
                    print (e)
                    if(val==len(places)-1):
                        print("method pas found ")
                        log.write("["+datetime.datetime.now().strftime("%d.%m.%Y %H-%M-%S")+"] "+f"can't find name on {self.ID} at {self.currentCat} : no endroit ? \n" )
                        log.write(self.currentPage+"\n")
                        return "N/A"

    def findLink(self,box):
        try:
            em_link = box.find_all("a",href=True)
            return em_link[0]['href']
        except:
            log.write("["+datetime.datetime.now().strftime("%d.%m.%Y %H-%M-%S")+"] "+f"can't find link on {self.ID} at {self.currentCat}  " )
            log.write(self.currentPage+"\n")

    def findRating(self,box):
        places=[("span",{"class":"stamped-badge"}),
        ("strong",{"class":"rating"}),]

        if self.Found["rate"]==True:
            endroit=places[self.toUse["rate"]]
            try:
                em_price = box.find_all(*endroit)
                return em_price[0].text
            except:
                log.write("["+datetime.datetime.now().strftime("%d.%m.%Y %H-%M-%S")+"] "+f"can't find rate on {self.ID} at {self.currentCat} :  \n" )
                log.write(self.currentPage+"\n")
                return "0"

        else:
            

            for val ,endroit in enumerate(places):
                try:
                    em_price = box.find_all(*endroit)
                    self.toUse["rate"]=val
                    self.Found["rate"]=True
             #       print("had le site khdem feh rate :" + endroit)
                    return em_price[0].text

                except :
                    if(val==len(places)-1):
                        log.write("["+datetime.datetime.now().strftime("%d.%m.%Y %H-%M-%S")+"] "+f"can't find rate on {self.ID} at {self.currentCat} :  no endroit\n" )
                        log.write(self.currentPage+"\n")
                        return "0"

    def findimglink(self,box):
        places=[("div",{"class":"product-image-link"}),
        ("div",{"class":"box-image"}),
        ("div",{'class':"product-thumb-primary 1"}),
        ("div",{'class':'image-none'}),
        ('div',{'class':'thumbnail-wrapper'})]


        if self.Found["imgsrc"]==True:
            endroit=self.toUse["imgsrc"]
            try:

                box=box.find_all(endroit)
                box=box[0].find_all("img")


                if re.search("(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|png)",box[0]["src"]) :
                   # print("found src on "+self.ID)

                    return box[0]["src"]   



                if re.search("(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|png)",box[0]["data-src"]):
                  #  print("found data-src on "+self.ID)
                    return box[0]["data-src"]     

                #print("not found on "+self.ID)



                return ""
            except  :
                log.write("["+datetime.datetime.now().strftime("%d.%m.%Y %H-%M-%S")+"] "+f"can't find img on {self.ID} at {self.currentCat} :  no endroit\n" )
                log.write(self.currentPage+"\n")
                return ""

        else:




            for val ,endroit in enumerate(places):
                try:
                    
                    em_price = box.find_all(*endroit)
                    if (len(em_price)!=0):
                        self.toUse["imgsrc"]=endroit
                        self.Found["imgsrc"]=True
                        #print("had le site khdem feh img :")
                        box=box.find_all(self.toUse["imgsrc"])
                        box=box[0].find_all("img")
                        if re.search("(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|png)",box[0]["src"]) :
                       # print("found src on "+self.ID)

                            return box[0]["src"]   



                        if re.search("(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|png)",box[0]["data-src"]):
                  #  print("found data-src on "+self.ID)
                            return box[0]["data-src"]     

                #print("not found on "+self.ID)



                        return ""   

                except Exception as e :
                    print (e)
                    if(val==len(places)-1):
                        print("img method pas found ")
                        log.write("["+datetime.datetime.now().strftime("%d.%m.%Y %H-%M-%S")+"] "+f"can't find imgsrc on {self.ID} at xx :  no endroit ? \n" )
                        log.write(self.currentPage+"\n")
                        return "N/A"
        '''
        method to get all the datas with the previous find methods 

        datas is a dict we get from setscrappingdata() => ( scrapdatas = Dict : {"cat":[iteration links html texts]})
        '''

    def scrapDataPage(self,datas):

        print("getting products...") 


        #list where we store the products
        products=[]


        for cat in datas:
            print(f"working on {cat}")
            for page in datas[cat]:
                
                prodboxes=self.findprodBox(page)

                for box in prodboxes:
                    name= self.findName(box)
                    price=self.findPrice(box)
                    link=self.findLink(box)
                    rate=self.findRating(box)
                    imgsrc=self.findimglink(box)
                    products.append(Produit(name,price,link,self.ID,rate,cat,imgsrc))
                    
                   
                    
            
            log.write("found")
            print("Done "+cat+ f" on {self.ID}")

        print(len(set(products)))
        print("Succes!")

        return sorted(set(products), key=lambda prod: prod.type)




def scrapsites():
    sites=['https://greensociety.cc/',
'https://greenleafexpress.io/',
'https://ganjawest.co/','https://getkush.io/',
'https://www.bulkbuddy.co/']

    brut={}

    for link in sites:
        script=scrapScript(link)
        datas=script.setscrappingdata()
        products=script.scrapDataPage(datas)
        brut[script.ID]=[]

        print('saving datas...')
        print(script.ID)
        
        for d in products:
            
            brut[script.ID].append(d.toDict())

    print('saving json')



    with open("brut.json", "w") as outfile:    
                
            outfile.write(json.dumps(brut))

    file_to_store = open("Products.pickle", "wb")
    pickle.dump(brut, file_to_store)

    file_to_store.close()



