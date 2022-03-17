import pandas as pd
import uuid
import plotly.express as px
import os
import plotly.graph_objects as go


file = "./data/banco de alimentos excel.xlsx"


id = str(uuid.uuid4())
os.rename(file,"./data/"+"data_"+id+"."+file.split(".")[2])
file = "data_"+id+"."+file.split(".")[2]
if file.split(".")[1] == "xlsx":
    df = pd.read_excel('data/'+file)
elif file.split(".")[1] == "csv":
    df = pd.read_csv("data/"+file)


df['Total_2019'] = df['COLHEITA_RECORRENTE(KG)2019'] + df['COLHEITA_PONTUAL(KG)2019']
df['Total_2020'] = df['COLHEITA_RECORRENTE(KG)2020'] + df['COLHEITA_PONTUAL(KG)2020']

df['Comparativo_recorrente'] =df['COLHEITA_RECORRENTE(KG)2020'] - df['COLHEITA_RECORRENTE(KG)2019']
df['Comparativo_pontual'] =df['COLHEITA_PONTUAL(KG)2020'] - df['COLHEITA_PONTUAL(KG)2019']
df_graph = df.drop(12)



media_pontual_2019 = round(df.at[12,"COLHEITA_PONTUAL(KG)2019"] / (len(df)-1))
media_recorrente_2019 = round(df.at[12,"COLHEITA_RECORRENTE(KG)2019"] / (len(df)-1))
media_pontual_2020 = round(df.at[12,"COLHEITA_PONTUAL(KG)2020"] / (len(df)-1))
media_recorrente_2020 = round(df.at[12,"COLHEITA_RECORRENTE(KG)2020"] / (len(df)-1))
media_total_2019  = round((df.at[12,"COLHEITA_PONTUAL(KG)2019"] + df.at[12,"COLHEITA_RECORRENTE(KG)2019"]) / (len(df)-1))
media_total_2020  = round((df.at[12,"COLHEITA_PONTUAL(KG)2020"] + df.at[12,"COLHEITA_RECORRENTE(KG)2020"]) / (len(df)-1))


df = df.append({"Mês":"MEDIA",
 	 "COLHEITA_RECORRENTE(KG)2019":media_recorrente_2019,
   "COLHEITA_RECORRENTE(KG)2020":media_recorrente_2020,
   "COLHEITA_PONTUAL(KG)2019" :media_pontual_2019,
   "COLHEITA_PONTUAL(KG)2020":media_pontual_2020,
   "Total_2019":media_total_2019,
   "Total_2020":media_total_2020,
   "Comparativo_recorrente":media_pontual_2020 - media_pontual_2019,
   "Comparativo_pontual":media_recorrente_2020 - media_recorrente_2019
 },ignore_index=True)


df = df.set_index("Mês")

df.to_csv("./relatorios/web/data/data_"+id+".csv",index=True)


fig = px.bar(df_graph, x='Mês', y='COLHEITA_PONTUAL(KG)2020')

os.mkdir("./relatorios/templates/graph/"+id)



fig.write_html("./relatorios/templates/graph/"+id+"/graph_1_"+id+".html")

fig = go.Figure(data=[
    go.Bar(name='2019', x=df_graph['Mês'], y=df_graph['COLHEITA_PONTUAL(KG)2019']),
    go.Bar(name='2020', x=df_graph['Mês'], y=df_graph['COLHEITA_PONTUAL(KG)2020'])
])
# Change the bar mode
fig.update_layout(barmode='group')

fig.write_html("./relatorios/templates/graph/"+id+"/graph_2_"+id+".html")

fig = go.Figure(data=[
    go.Bar(name='2019', x=df_graph['Mês'], y=df_graph['COLHEITA_RECORRENTE(KG)2019']),
    go.Bar(name='2020', x=df_graph['Mês'], y=df_graph['COLHEITA_RECORRENTE(KG)2020'])
])
# Change the bar mode
fig.update_layout(barmode='group')


fig.write_html("./relatorios/templates/graph/"+id+"/graph_3_"+id+".html")

fig = go.Figure(data=[
    go.Bar(name='2019', x=df_graph['Mês'], y=df_graph['Total_2019']),
    go.Bar(name='2020', x=df_graph['Mês'], y=df_graph['Total_2020'])
])
# Change the bar mode
fig.update_layout(barmode='group')


fig.write_html("./relatorios/templates/graph/"+id+"/graph_4_"+id+".html")


fig = go.Figure()
fig.add_trace(go.Bar(x=df_graph['Mês'], y=df_graph['Comparativo_recorrente'],
                base=0,
                marker_color='crimson',
                name='Comparativo_recorrente'))
fig.add_trace(go.Bar(x=df_graph['Mês'], y=df_graph['Comparativo_pontual'],
                base=0,
                marker_color='lightslategrey',
                name='Comparativo_pontual'
                ))

fig.write_html("./relatorios/templates/graph/"+id+"/graph_5_"+id+".html")