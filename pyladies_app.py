import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import plotly.graph_objs as go

import os


app = dash.Dash()
#id for heroku
server=app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')


OPTIONS = {
		'Praha17': '2017 Jak se staví sen v Praze?',
		'Praha18': '2018 Jak se staví sen v Praze?',
		'CR17': '2017 Jak se staví sen v ČR',
		'CR18': '2018 Jak se staví sen v ČR'
}



app.layout = html.Div(children=[
	dcc.Markdown('''
## Vyplatí se Vám rekonstrukce?
				  
Podle dat [sreality.cz](https://www.sreality.cz/)
	'''),

	dcc.Graph(
		id='example-graph',
		figure = {
			'data': [],
			'layout': {
				'title': ''
			}
		}
	),
   
	 html.Label('Vyberte typ grafu'),
	dcc.Dropdown(
		id = 'chooser',
		options = [{'label': label, 'value': key} for key, label in OPTIONS.items()],
		value = 'Praha17'
	)
])

@app.callback(
	dash.dependencies.Output(component_id='example-graph', component_property='figure'),
	[dash.dependencies.Input(component_id='chooser', component_property='value')],
)
def update_figure(choice):
	figure = {
			'data': [],
			'layout': go.Layout(title = OPTIONS[choice])
	}
	
	
	if choice == 'Praha17':

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

		df17['cena_za_m2'] = df17.cena / df17.uzitna_plocha

		dfpom = df17.popisek.apply(oznac_rekonstrukce).apply(pd.Series)
		df17['rekon_mozna'] = dfpom[0]
		df17['rekon_mozna_delka'] = dfpom[1]
		df17['rekonstrukce'] = dfpom[2]
		df17['castecna_rekonstrukce'] = dfpom[3]

		df17.loc[(df17.rekonstrukce==False) & (df17.rekon_mozna_delka==0),'rekonstrukce']=None

		df17.loc[df17.castecna_rekonstrukce==True, 'rekonstrukce'] = False
		df17['novy_byt'] = False
		df17.loc[df17['rekonstrukce']==False,'novy_byt'] = df17[df17['rekonstrukce']==False].popisek.str.lower().str.contains('nový byt')
		df17.loc[(df17['rekonstrukce']==False) & (df17['novy_byt']==False),'novy_byt'] = df17[(df17['rekonstrukce']==False) & (df17['novy_byt']==False)].popisek.str.lower().str.contains('novostavba')

		byty = ['1+kk','1+1',
        '2+kk','2+1',
        '3+kk','3+1']

		df3 = df17[(df17.dispozice.isin(byty)) & (df17['typ']=='Prodej') & (df17['novy_byt']==False) & (df17.region=='praha')].groupby(['dispozice','rekonstrukce']).cena_za_m2.median().unstack()



		plot_function = go.Bar
		trace1 = plot_function(x = df3.index, y = df3[0.0], opacity = 0.75, name = 'Před rekonstrukcí', marker = dict(color= 'rgb(255, 77, 77)'))
		trace2 = plot_function(x = df3.index, y = df3[1.0], opacity = 0.75, name = 'Po rekonstrukci', marker = dict(color= 'rgb(77, 136, 255)'))
	

		data = [trace1, trace2]

		figure={
			'data': data,
			'layout': {
				'barmode' : 'group',
				'title': '<b>2017 Jak se staví sen v Praze?</b>',
				'titlefont' : dict(
					size = 20, color = 'black'),
				'xaxis' : dict(
					title = 'Dispozice'),
			},

		}

	elif choice == 'Praha18':
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


		df18['cena_za_m2'] = df18.cena / df18.uzitna_plocha

		dfpom = df18.popisek.apply(oznac_rekonstrukce).apply(pd.Series)
		df18['rekon_mozna'] = dfpom[0]
		df18['rekon_mozna_delka'] = dfpom[1]
		df18['rekonstrukce'] = dfpom[2]
		df18['castecna_rekonstrukce'] = dfpom[3]

		df18.loc[(df18.rekonstrukce==False) & (df18.rekon_mozna_delka==0),'rekonstrukce']=None

		df18.loc[df18.castecna_rekonstrukce==True, 'rekonstrukce'] = False
		df18['novy_byt'] = False
		df18.loc[df18['rekonstrukce']==False,'novy_byt'] = df18[df18['rekonstrukce']==False].popisek.str.lower().str.contains('nový byt')
		df18.loc[(df18['rekonstrukce']==False) & (df18['novy_byt']==False),'novy_byt'] = df18[(df18['rekonstrukce']==False) & (df18['novy_byt']==False)].popisek.str.lower().str.contains('novostavba')

		byty = ['1+kk','1+1',
        '2+kk','2+1',
        '3+kk','3+1']

		df5 = df18[(df18.dispozice.isin(byty)) & (df18['typ']=='Prodej') & (df18['novy_byt']==False) & (df18.region=='praha')].groupby(['dispozice','rekonstrukce']).cena_za_m2.median().unstack()

		plot_function = go.Bar
		trace1 = plot_function(x = df5.index, y = df5[0.0], opacity = 0.75, name = 'Před rekonstrukcí', marker = dict(color= 'rgb(255, 77, 77)'))
		trace2 = plot_function(x = df5.index, y = df5[1.0], opacity = 0.75, name = 'Po rekonstrukci', marker = dict(color= 'rgb(77, 136, 255)'))
	

		data = [trace1, trace2]

		figure={
			'data': data,
			'layout': {
				'barmode' : 'group',
				'title': '<b>2018 Jak se staví sen v Praze?</b>',
				'titlefont' : dict(
					size = 20, color = 'black'),
				'xaxis' : dict(
					title = 'Dispozice'),
			},

		}

	elif choice == 'CR17':
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


		df18['cena_za_m2'] = df18.cena / df18.uzitna_plocha

		dfpom = df18.popisek.apply(oznac_rekonstrukce).apply(pd.Series)
		df18['rekon_mozna'] = dfpom[0]
		df18['rekon_mozna_delka'] = dfpom[1]
		df18['rekonstrukce'] = dfpom[2]
		df18['castecna_rekonstrukce'] = dfpom[3]

		df18.loc[(df18.rekonstrukce==False) & (df18.rekon_mozna_delka==0),'rekonstrukce']=None

		df18.loc[df18.castecna_rekonstrukce==True, 'rekonstrukce'] = False
		df18['novy_byt'] = False
		df18.loc[df18['rekonstrukce']==False,'novy_byt'] = df18[df18['rekonstrukce']==False].popisek.str.lower().str.contains('nový byt')
		df18.loc[(df18['rekonstrukce']==False) & (df18['novy_byt']==False),'novy_byt'] = df18[(df18['rekonstrukce']==False) & (df18['novy_byt']==False)].popisek.str.lower().str.contains('novostavba')

		byty = ['1+kk','1+1',
        '2+kk','2+1',
        '3+kk','3+1']

		df2 = df17[(df17.dispozice.isin(byty)) & (df17['typ']=='Prodej') & (df17['novy_byt']==False)].groupby(['region','rekonstrukce']).cena_za_m2.median().unstack()

		plot_function = go.Bar
		trace1 = plot_function(x = df2.index, y = df5[0.0], opacity = 0.75, name = 'Před rekonstrukcí', marker = dict(color= 'rgb(255, 77, 77)'))
		trace2 = plot_function(x = df2.index, y = df5[1.0], opacity = 0.75, name = 'Po rekonstrukci', marker = dict(color= 'rgb(77, 136, 255)'))
	

		data = [trace1, trace2]

		figure={
			'data': data,
			'layout': {
				'barmode' : 'group',
				'title': '<b>2018 Jak se staví sen v Praze?</b>',
				'titlefont' : dict(
					size = 20, color = 'black'),
				'xaxis' : dict(
					title = 'Dispozice'),
			},

		}
	

	elif choice == 'CR17':
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


		df18['cena_za_m2'] = df18.cena / df18.uzitna_plocha

		dfpom = df18.popisek.apply(oznac_rekonstrukce).apply(pd.Series)
		df18['rekon_mozna'] = dfpom[0]
		df18['rekon_mozna_delka'] = dfpom[1]
		df18['rekonstrukce'] = dfpom[2]
		df18['castecna_rekonstrukce'] = dfpom[3]

		df18.loc[(df18.rekonstrukce==False) & (df18.rekon_mozna_delka==0),'rekonstrukce']=None

		df18.loc[df18.castecna_rekonstrukce==True, 'rekonstrukce'] = False
		df18['novy_byt'] = False
		df18.loc[df18['rekonstrukce']==False,'novy_byt'] = df18[df18['rekonstrukce']==False].popisek.str.lower().str.contains('nový byt')
		df18.loc[(df18['rekonstrukce']==False) & (df18['novy_byt']==False),'novy_byt'] = df18[(df18['rekonstrukce']==False) & (df18['novy_byt']==False)].popisek.str.lower().str.contains('novostavba')

		byty = ['1+kk','1+1',
        '2+kk','2+1',
        '3+kk','3+1']

		df4 = df18[(df18.dispozice.isin(byty)) & (df18['typ']=='Prodej') & (df18['novy_byt']==False)].groupby(['region','rekonstrukce']).cena_za_m2.median().unstack()

		plot_function = go.Bar
		trace1 = plot_function(x = df4.index, y = df4[0.0], opacity = 0.75, name = 'Před rekonstrukcí', marker = dict(color= 'rgb(255, 77, 77)'))
		trace2 = plot_function(x = df4.index, y = df4[1.0], opacity = 0.75, name = 'Po rekonstrukci', marker = dict(color= 'rgb(77, 136, 255)'))
	

		data = [trace1, trace2]

		figure={
			'data': data,
			'layout': {
				'barmode' : 'group',
				'title': '<b>2018 Jak se staví sen v Praze?</b>',
				'titlefont' : dict(
					size = 20, color = 'black'),
				'xaxis' : dict(
					title = 'Dispozice'),
			},

		}
	


	return figure

df17= pd.read_csv("C:/Users/nguye/Documents/pyladies/sreality_2017.csv", sep=';', encoding = 'utf8' )
df18= pd.read_csv("C:/Users/nguye/Documents/pyladies/sreality_2018.csv", sep=';', encoding = 'utf8' )

if __name__ == '__main__':
	app.run_server()