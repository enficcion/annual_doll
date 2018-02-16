# coding: utf-8


import matplotlib.pyplot as plt

get_ipython().magic('matplotlib inline')


import numpy as np
import pandas as pd
import seaborn as sns

dm17=pd.read_excel('dm17.xlsx')


dm17.head()

#Borramos todas las filas que no son inputs de muñequito 
#(un input tiene al menos marca temporal, correo, nombre, círculo y tiempo)
dm17=dm17.dropna(thresh=4)

#Para asegurarnos de tener consistencia en los nombres (es decir, que la misma persona se llama igual todos los meses) creamos una nueva columna que usa el usuario de correo como nombre, porque
dm17['realname']=dm17['Dirección de correo electrónico'].str.split('@').str.get(0)


#No necesitamos el nombre que pusieron ni el correo electrónico así que borramos esas dos columnas
dm17.drop(['Dirección de correo electrónico','Your Name'],axis=1)


#para poder analziar la data de circles y time asignado a cada uno, necesitamos una matriz que tenga cuatro columnas: marca temporal, realname, circle y time
#como en la tabla original los circles y sus respectivos shares de tiempo aparecen en distintas columnas, lo separamos en varias matrices, cada una solo con las columnas que necesitamos 
matriz1=dm17[['Marca temporal','Circle or Task 1','Time %','realname']]
matriz2=dm17[['Marca temporal','Circle or Task 2','Time %.1','realname']]
matriz3=dm17[['Marca temporal','Circle or Task 3','Time %.2','realname']]
matriz4=dm17[['Marca temporal','Circle or Task 4','Time %.3','realname']]
matriz5=dm17[['Marca temporal','Circle or Task 5','Time %.4','realname']]
matriz6=dm17[['Marca temporal','Nice to have 1','Time %.5','realname']]
matriz7=dm17[['Marca temporal','Nice to have 2','Time %.6','realname']]
matriz8=dm17[['Marca temporal','Nice to have 3','Time %.7','realname']]
matriz9=dm17[['Marca temporal','Nice to have 4','Time %.8','realname']]
matriz10=dm17[['Marca temporal','Nice to have 5','Time %.9','realname']]

#Luego, hacemos que las columnas equivalentes se llamen igual en las distintas matrices
matriz1=matriz1.rename(index=str, columns={"Circle or Task 1": "Circle or Task"})
matriz2=matriz2.rename(index=str, columns={"Circle or Task 2": "Circle or Task","Time %.1":"Time %"})
matriz3=matriz3.rename(index=str, columns={"Circle or Task 3": "Circle or Task","Time %.2":"Time %"})
matriz4=matriz4.rename(index=str, columns={"Circle or Task 4": "Circle or Task","Time %.3":"Time %"})
matriz5=matriz5.rename(index=str, columns={"Circle or Task 5": "Circle or Task","Time %.4":"Time %"})
matriz6=matriz6.rename(index=str, columns={"Nice to have 1": "Circle or Task","Time %.5":"Time %"})
matriz7=matriz7.rename(index=str, columns={"Nice to have 2": "Circle or Task","Time %.6":"Time %"})
matriz8=matriz8.rename(index=str, columns={"Nice to have 3": "Circle or Task","Time %.7":"Time %"})
matriz9=matriz9.rename(index=str, columns={"Nice to have 4": "Circle or Task","Time %.8":"Time %"})
matriz10=matriz10.rename(index=str, columns={"Nice to have 5": "Circle or Task","Time %.9":"Time %"})


#Finalmente, juntamos las matrices en una sola matriz de cuatro columnas
matriz1234=matriz1.append(matriz2)
matriz1234=matriz1234.append(matriz3)
matriz1234=matriz1234.append(matriz4)
matriz1234=matriz1234.append(matriz5)
matriz1234=matriz1234.append(matriz6)
matriz1234=matriz1234.append(matriz7)
matriz1234=matriz1234.append(matriz8)
matriz1234=matriz1234.append(matriz9)
matriz1234=matriz1234.append(matriz10)

#Verificamos que haya quedado bien
matriz1234.head()

#Como no todos tienen la misma cantidad de circles o task todos los meses, en algunas de las matrices de 4 columnas que creamos al separarlas había líneas sin información de circle y time. Ahora que las hemos juntado todas en una sola, borramos las líneas sin información (es decir, las que no tienen al menos marca temporal, realname, circle y time) 
matriz1234=matriz1234.dropna(thresh=4)

#Algo que necesitamos hacer para poder uniformizar la data es hacer que un mismo circle se llame igual siempre. Como cada uno tipea el nombre del circle al crear su muñequito mensual, pueden existir discrepancias tanto entre personas como entre meses.

#Para comenzar a uniformizar un poco los nombres, eliminamos los espacios al comienzo y al final de los'circle or task'
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].str.strip()

#Para evitar discrepancias por capitalización, pasamos todos los circles a letras minúsculas
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].str.lower()


#Agrupamos la data por 'Circle or Task' y la ordenamos en orden alfabético para identificar algunos nombres que podrían estar escritos de más de una forma
porcircle=matriz1234.groupby(['Circle or Task'])['Time %'].sum().reset_index()
porcircle.sort_values(['Circle or Task','Time %'],ascending=True)

#Usamos display.max_rows para poder revisar todas las filas
with pd.option_context('display.max_rows', None, 'display.max_columns', 4):
    print(porcircle.sort_values(['Circle or Task','Time %'],ascending=True))


#Luego de leer los nombres de circles que nos arroja la tabla, transformamos los que sean necesarios
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['admin & others','admin (growth, gl, steerings)'],'admin')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['fest','fest 17','fest','fest17'], 'fest_17')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['academy'], 'digital academy')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['alpacas'], 'alpacas pitucas')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['b house'], 'b-house')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['beacon accelerator - oe','beta house - oechsle','beta house - oechsle beacon'], 'accelerator - oechsle beacon')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['beacon playbook po','beacon playbook product ownership','beacon playbook stewardship'], 'beacon playbook')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['beta house	on-boarding','beta house'], 'beta house')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['budget	2018','budget','budget 2017'], 'budget')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['clonning'], 'cloning')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['talent','talent'], 'talent')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['team\'s travel	'], 'team\'s travels')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['vacations','vacaciones'], 'holidays')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['young talent','young talent '], 'young talent')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['beacon accelerator','accelerator'], 'accelerator / beacon program')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['catapult','digital academy/skills','five digital era skills','digital academy','digital skill','digital skillbuilding','digital academy / skills'], 'catapult / skills / digital academy')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['ditto program','ditto strategy'], 'ditto program / strategy')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['diversity','gender','gender sprint','gender prep','diversity sprint','diversity sprint (prep)','gender sprint prep','gender sprint: stewardship'], 'talent diversity')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['eoyr','end of year retreat - attending'], 'end of year retreat')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['experience & strategy (ops sprint)','ops org design sprint','ops sprint'], 'experience & strategy / ops sprint')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['fest_17 (travels arrangement ) ','fest_17 travel\'s arrangements','fest_17 trophies'], 'fest_17')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['future of shopping','future of shopping (espresso shots)','future of shopping / espresso shots'], 'fest_17')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['head of keel','head of keel team','head of ops'], 'head of keel')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['hernan (& lab) support'], 'hernan & lab support')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['holiday: san pedro & san pablo','holidays (tbd)'], 'holidays')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['inkafarma implementation'], 'ikf implementation')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['inkafarma stewardship'], 'ikf stewardship')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['inspiration & learnings',,'inspirations','inspirations & learnings','inspiration'], 'inspiration & learning')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['intelligent networks','intelligent network','idn (intercorp design network)'], 'innovation network')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['interbank beacon','nando','nando (tone of voice)','beacon interbank'], 'ibk beacon')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['interbank stewardship'], 'ibk stewardship')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['intercorp vision + purpose'], 'intercorp purpose')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['laboratoria ws','laboratoria'], 'laboratoria workshop')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['lad fest shareback'], 'ladfest shareback')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['lvl way (ditto vs classic)', 'la victoria way'],'lvl way')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['lvl web videos', 'lvl website (documentaries)'],'lvl website')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['mantemiento'], 'mantenimiento')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['meetup'],'meetups')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['oechsle','oechsle beacon'],'accelerator - oechsle beacon')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['other','others (research / support)','others (circus, gl,etc) ','others /admin'],'others')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['playbook','playbook launch'],'beacon playbook')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['promart (branding)','promart prep','promart branding','promart brand sprint','promart sdl'],'promart')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['provinces trip','trip to pronvinces'],'provincias trip')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['real plaza lab','real plaza prep'],'real plaza')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['sd workhsop',''],'service design workshop')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['seattle'],'seattle trip')
matriz1234['Circle or Task'] =matriz1234['Circle or Task'].replace(['team\'s travels'], 'team\'s travel')


#Agrupamos de nuevo la data por 'Circle or Task' y la ordenamos en orden alfabético para identificar 
#algunos nombres que se nos podrían haber pasado. Si es que falta uniformizar, volvemos al paso anterior.
porcircle=matriz1234.groupby(['Circle or Task'])['Time %'].sum().reset_index()
porcircle.sort_values(['Circle or Task','Time %'],ascending=True)

#Usamos display.max_rows para poder revisar todas las filas
with pd.option_context('display.max_rows', None, 'display.max_columns', 4):
    print(porcircle.sort_values(['Circle or Task','Time %'],ascending=True))


#Agrupamos los muñequitos anuales por labber y reseteamos el índice para poder re ordenarlo
porlabber=matriz1234.groupby(['realname','Circle or Task'])['Time %'].sum().reset_index()
porlabber.sort_values(['realname','Time %'],ascending=True)
with pd.option_context('display.max_rows', None, 'display.max_columns', 4):
    print(porlabber.sort_values(['realname','Time %'],ascending=True))

#Calculamos el share of time/energy de cada circle por persona. Para eso primero creamos
#una columna que sume los porcentajes de todos los circles en los que una persona ha trabajado
porlabber['total']=porlabber.groupby('realname')['Time %'].transform(sum)

#Creamos una columna que calcule el ratio entre el total de 'Time %' dedicado a un circle, y la columna total
porlabber['share']=porlabber['Time %']/porlabber['total']

#Cambiamos el nombre de la columna Circle or Task a circle para evitar problemas por capitalización y espacios
porlabber=porlabber.rename(index=str,columns={"Circle or Task":"circle"})

#Eliminamos las columnas que no nos van a servir
porlabber=porlabber.drop(['Time %','total'],1)

#Guardamos la tabla como csv
porlabber.to_csv('munequito_personal.tsv', sep='\t')


#BACKLOG
#un solo archivo para lab y para names
#no se necesita share, solo time total
#ordenar por time para que los gráficos salgan mejor
