import os
from time import sleep, time
import json
from difflib import SequenceMatcher
import random
import scrapScript











def setCategory(product):
    categories = {'Cannabis':['The Green Room','Cannabis'],
                    'Concentrates':['Concentrates','THC'],
                    'Edibles':['Edibles','Cannabis Edibles'],
                    'vapes':['CBD & THC Vape Pens','Vaporizer','Vapes'],
                    'cbd':['CBD','CBD Oils'],
                    'Accessories':['Accessories','Other Marijuana Products','Gifts','Variety Packs (All)'],
                    'Mushrooms':['Magic Mushrooms']}
    for cat in categories :
        for k in categories[cat]:
            if product['type'].lower() in k.lower():
                product['type']=cat
                return product
    return product


    


def getCategory(category):
    catprods=[]
    with open('brut.json') as json_file:
            lebrut = json.load(json_file)
            for site in lebrut:
                for p in lebrut[site]:

                    if p["type"].lower()==category.lower():

                        catprods.append(p)
                    if category=='Edibles' and p["type"].lower()=='Cannabis Edibles':
                        catprods.append(p)
            
            return catprods
                
def searchtoString(searchres):

    for k in searchres:
        if len(searchres[k])!=0:
            print(f"============== Found in {k}==============\n\n")
            for res in searchres[k]:

                print(res['nom'])
                print("$$$$$$$$$$$")

        else:
            print(f"==============not Found in {k}==============\n\n")

def searchforKw(sa):
    with open('KwDb.json') as json_file:
        data = json.load(json_file)
        #searchInput
        si=sa.strip().lower().split()
        s=[]
        for k in si :
            s+=[x.replace('stock#',"").replace('(','').replace(')','').replace('#','') for x in list(data.keys()) if k in x]
       # print('initial search :')
       # for x in si : 
       #     print(".",x)
       # print('potential kw :')
      #  for x in s : 
      #      print('>',x)

        tempS=[]
        for n in si :
          

            
            tempS+=[(SequenceMatcher(None, n,v).ratio(),v)   for v in s if SequenceMatcher(None, n,v).ratio()>=0.59]
            #print([v for v in s if( v in n and len(n)-1<=len(v)<=len(n)+1)])
        s=[v[1] for v in tempS]
        #for t in tempS:
      #      print("---"+t[1]+" : "+str(t[0]))



        
        indice = len(si)
        res=[]
        resultat={}






        for k in set(s) :
           # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   ',k,'  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            if k in data:
                for prod in data[k]:

                 #   print(">>>>>"+prod['nom'])

                    if prod['lien'] not in resultat   :
                #        print('<<<<<<<<<<<<<<<<<<<<<<< New : '+prod['nom'])
                        resultat[prod['lien']]=[prod,1]
                    else:
                        resultat[prod['lien']][1]+=1
                 #       print('<<<<<<<<<<<<<<<<<<<<<<< up : '+prod['nom'] +"::::::::::::::  ",resultat[prod['lien']][1])
        for resu in resultat:
            if resultat[resu][1]>=len(si):
                res.append(resultat[resu][0])

                    
    


        

        print("========== Found "+str(len(res)) + " items ==========")
        res=sorted(res,key=lambda r: SequenceMatcher(None, r['nom'],sa).ratio(),reverse=True)
        '''
        for r in res :
            print("IIIIIIIIIIIIIIIIIIIIIII "+r['nom']+"  :  ",SequenceMatcher(None, r['nom'],sa).ratio() )
        '''
        
        return res
        
        
def searchApi(rech):
    
    search=searchforKw(rech)
    return search
   
def toJson(donne):

            with open("resultat.json", "w") as outfile:
                for k in donne:
                    x=[]
                    for prod in donne[k] :
                        x.append(prod)

                outfile.write(json.dumps(x))

def sendJson(donne):
    for k in donne:
                    x=[]
                    for prod in donne[k] :
                        x.append(prod)
    return json.dumps(x)


'''

fucnction to set json database with dict of keywords (which are the words in all products )
'''

def getKwdDb(save=False):
    keywords={}
    with open('brut.json') as json_file:
        data = json.load(json_file)
        print("Getting keywords")

    for site in data:

            print("working on "+site)
            for prod in data[site]:
                prod=setCategory(prod)
                try:
                    words= prod['nom'].split()
                except:
                    pass
                for word in words : 
                    if word.strip().lower() in keywords:
                        keywords[word.strip().lower()].append(prod)
                    else : 
                        keywords[word.strip().lower()]=[prod]


    if save : 
        with open('KwDb.json', 'w') as outfile:
            json.dump(keywords, outfile)

    return keywords

def getallprods():
    with open('brut.json') as json_file:
        data = json.load(json_file)
        products=[]
        for site in data:
            products+=data[site]
        print (len(products))
    

        return (random.sample(products,len(products)))
        





start_time = time()

#searchtoString(a)
#getCategory('flower')


searchforKw('og kush')
'''

a=a["brut"]
for r in a:
            print (r["nom"])

'''


print("--- %s seconds ---" % (time() - start_time))

  