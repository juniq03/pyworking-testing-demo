# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 10:42:11 2018

@author: nettlef
"""

import pandas as pd
import seaborn as sns

keyword = 'rekonstrukc'
blacklist = ['dům', 'domu', 'domě','určen','fasád','po rekonstrukci může',
             'možnost provést', 'možno udělat',
             'připraven', 'vhodn',
             'doporučujeme', 'žádá', 'žádoucí',
             'před', 'vyžaduje', 'potřebuje', 
             'předurčuje k', 'ideální k',
             'střech','demolici']

partlist = ['kuchyn','kuchyň','koupeln','částečn',
            'wc', 'podlah']

def oznac_rekonstrukce(popisek):
    # vycisti a dej do listu
    chunks = []
    popisek = popisek.lower().replace('\n',' ').replace('.',' ').replace(',',' ').replace('"',' ')
    slova = popisek.split()
    p = 0
    for slovo in slova:
        if keyword in slovo:
            start = max(p - 4, 0)
            end = min(p + 4, len(slova))
            chunk = ' '.join(slova[start:end])
            is_black = False
            is_part = False                
            chunks.append(chunk)
        p = p + 1
        
    is_rekonstrukce = False
    is_partrekonstrukce = False
    for chunk in chunks:
        is_black = False
        is_part = False
        for blackword in blacklist:
            if blackword in chunk:
                is_black = True
        if not is_black:
            for partword in partlist:
                if partword in chunk:
                    is_part = True
                    is_partrekonstrukce = True
        
        if (not is_black) and (not is_part):
            is_rekonstrukce = True
    return chunks, len(chunks), is_rekonstrukce, is_partrekonstrukce
        
    
    

filename = 'sreality_2017.csv'
df17 = pd.read_csv(filename, sep=';')

filename = 'sreality_2018.csv'
df18 = pd.read_csv(filename, sep=';')

df17['cena_za_m2'] = df17.cena / df17.uzitna_plocha
df18['cena_za_m2'] = df18.cena / df18.uzitna_plocha


dfpom = df17.popisek.apply(oznac_rekonstrukce).apply(pd.Series)
df17['rekon_mozna'] = dfpom[0]
df17['rekon_mozna_delka'] = dfpom[1]
df17['rekonstrukce'] = dfpom[2]
df17['castecna_rekonstrukce'] = dfpom[3]

df17.loc[(df17.rekonstrukce==False) & (df17.rekon_mozna_delka==0),'rekonstrukce']=None

dfpom = df18.popisek.apply(oznac_rekonstrukce).apply(pd.Series)
df18['rekon_mozna'] = dfpom[0]
df18['rekon_mozna_delka'] = dfpom[1]
df18['rekonstrukce'] = dfpom[2]
df18['castecna_rekonstrukce'] = dfpom[3]

df18.loc[(df18.rekonstrukce==False) & (df18.rekon_mozna_delka==0),'rekonstrukce']=None


df17.loc[df17.castecna_rekonstrukce==True, 'rekonstrukce'] = False
df18.loc[df18.castecna_rekonstrukce==True, 'rekonstrukce'] = False

df17['novy_byt'] = False
df17.loc[df17['rekonstrukce']==False,'novy_byt'] = df17[df17['rekonstrukce']==False].popisek.str.lower().str.contains('nový byt')
df17.loc[(df17['rekonstrukce']==False) & (df17['novy_byt']==False),'novy_byt'] = df17[(df17['rekonstrukce']==False) & (df17['novy_byt']==False)].popisek.str.lower().str.contains('novostavba')

df18['novy_byt'] = False
df18.loc[df18['rekonstrukce']==False,'novy_byt'] = df18[df18['rekonstrukce']==False].popisek.str.lower().str.contains('nový byt')
df18.loc[(df18['rekonstrukce']==False) & (df18['novy_byt']==False),'novy_byt'] = df18[(df18['rekonstrukce']==False) & (df18['novy_byt']==False)].popisek.str.lower().str.contains('novostavba')


#df17.to_excel('sreality2017.xlsx')
#df18.to_excel('sreality2018.xlsx')

byty = ['1+kk','1+1',
        '2+kk','2+1',
        '3+kk','3+1',
        '4+kk','4+1',
        '5+kk','5+1',
        '6 a vice']

df17[(df17.dispozice.isin(byty)) & (df17['typ']=='Pronajem') & (df17['novy_byt']==False)].groupby(['region','rekonstrukce']).cena.median()


df17[(df17.dispozice.isin(byty)) & (df17['typ']=='Prodej') & (df17['novy_byt']==False)].groupby(['region','rekonstrukce']).cena_za_m2.median()
df17[(df17.dispozice.isin(byty)) & (df17['typ']=='Prodej') & (df17['novy_byt']==False)].groupby(['region','rekonstrukce']).cena_za_m2.count()


#df17[(df17.dispozice.isin(byty)) & (df17['typ']=='Prodej') & (df17['novy_byt']==False)].groupby(['region','castecna_rekonstrukce']).cena_za_m2.median().plot()
#df17[(df17.dispozice.isin(byty)) & (df17['typ']=='Prodej') & (df17['novy_byt']==False)].groupby(['region','castecna_rekonstrukce']).cena_za_m2.count()

#
#df17[(df17.dispozice.isin(byty)) & (df17['typ']=='Prodej')].groupby(['region','novy_byt']).cena_za_m2.median()
#df17[(df17.dispozice.isin(byty)) & (df17['typ']=='Prodej')].groupby(['region','novy_byt']).cena_za_m2.count()


df17[(df17.dispozice.isin(byty)) & (df17['typ']=='Prodej') & (df17['novy_byt']==False)].groupby(['region','rekonstrukce']).cena_za_m2.median().unstack().plot(kind='bar',figsize = (20,10))

df18[(df18.dispozice.isin(byty)) & (df18['typ']=='Prodej') & (df18['novy_byt']==False)].groupby(['region','rekonstrukce']).cena_za_m2.median().unstack().plot(kind='bar',figsize = (20,10))

df17[(df17.dispozice.isin(byty)) & (df17['typ']=='Pronajem') & (df17['novy_byt']==False)].groupby(['region','rekonstrukce']).cena.median().unstack().plot(kind='bar',figsize = (20,10))
df18[(df18.dispozice.isin(byty)) & (df18['typ']=='Pronajem') & (df18['novy_byt']==False)].groupby(['region','rekonstrukce']).cena.median().unstack().plot(kind='bar',figsize = (20,10))

dfp = df18[(df18.dispozice.isin(byty)) & (df18['typ']=='Prodej') & (df18['novy_byt']==False) & (df18.region=='stredocesky')]
