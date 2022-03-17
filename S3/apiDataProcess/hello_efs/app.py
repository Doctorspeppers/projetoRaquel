import json
from pathlib import Path
import pandas
import boto3
import re
import botocore
import pandas as pd
import uuid
import os
import plotly.express as px
import plotly.graph_objects as go
# You can reference EFS files by including your local mount path, and then
# treat them like any other file. Local invokes may not work with this, however,
# as the file/folders may not be present in the container.
FILE = Path("/mnt/lambda/file")

def lambda_handler(message, context):
    print(message)

    returnBucket = ""

    record = message['Records'][0]
    if (record['eventName'] != 'ObjectCreated:Put'):
        print("Event is %s, ignoring" % record['eventName'])
        return {}

    sourceBucket = record['s3']['bucket']['name']
    fileName = record['s3']['object']['key']

    # Only operate on JPG files
    if (not re.match(r'.*\.xlsx$', fileName) or not re.match(r'.*\.xls$', fileName)):
        return {}
    else:
        extension = fileName.split(".")[-1] 

    s3 = boto3.resource('s3')
    id = str(uuid.uuid4())
    fileSavePath = "/tmp/data_%s.%s" % id, extension

    print("Retrieving file %s from ObjectStore 'Uploaded files'" % fileName)

    try:
        s3.Bucket(sourceBucket).download_file(fileName, fileSavePath)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object %s does not exist in bucket %s", (sourceBucket, imageName))
        else:
            raise

### SCRIPT INIT
    if fileSavePath.split(".")[-1] == "xlsx":
        df = pd.read_excel(fileSavePath)
    elif fileSavePath.split(".")[-1] == "csv":
        df = pd.read_csv(fileSavePath)


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

    df.to_csv("/tmp/data_"+id+".csv",index=True)


    fig = px.bar(df_graph, x='Mês', y='COLHEITA_PONTUAL(KG)2020')

    fig.write_html("/tmp/"+id+"/graph_1_"+id+".html")

    fig = go.Figure(data=[
        go.Bar(name='2019', x=df_graph['Mês'], y=df_graph['COLHEITA_PONTUAL(KG)2019']),
        go.Bar(name='2020', x=df_graph['Mês'], y=df_graph['COLHEITA_PONTUAL(KG)2020'])
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')

    fig.write_html("/tmp/graph_2_"+id+".html")

    fig = go.Figure(data=[
        go.Bar(name='2019', x=df_graph['Mês'], y=df_graph['COLHEITA_RECORRENTE(KG)2019']),
        go.Bar(name='2020', x=df_graph['Mês'], y=df_graph['COLHEITA_RECORRENTE(KG)2020'])
    ])
    fig.update_layout(barmode='group')


    fig.write_html("/tmp/graph_3_"+id+".html")

    fig = go.Figure(data=[
        go.Bar(name='2019', x=df_graph['Mês'], y=df_graph['Total_2019']),
        go.Bar(name='2020', x=df_graph['Mês'], y=df_graph['Total_2020'])
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')


    fig.write_html("/tmp/graph_4_"+id+".html")


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

    fig.write_html("/tmp/graph_5_"+id+".html")
    
## FINISH SCRIPT

    bucket = s3.Bucket(returnBucket)
    bucketObjNames = bucket.objects.all().keys()
    files = set(os.listdir("/tmp/"))
    for file in files:
        if file.split(".")[-1] == "csv" or file.split(".")[-1] == "xslx" or file.split("xsl"): local = "files"
        elif file.split(".")[-1] == "html": local = "graph"
        bucket.upload_file("graphs", os.path.join(local, file))
        os.remove(file)


    return {
        "statusCode": 200,
        "body": json.dumps({
            "id":id
        }),
    }
