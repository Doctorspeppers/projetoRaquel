from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import csv
import os
from pathlib import Path
def relatorio_colheita(request,id):
    print(os.path.join(Path(__file__).resolve().parent.parent,'templates'))
    with open("./web/data/data_"+id+".csv",'r') as fp:
        table_loaded = list(csv.reader(fp))
        rows = []
        for i,row in zip(range(0,len(table_loaded)),table_loaded):
            if i == 0:
                columns = row
            else:
                rows.append(row)       

    template = loader.get_template('relatorio.html')
    graph = []
    for i in range(1,5):
        graph.append("./graph/"+id+"/graph_"+str(i)+"_"+ id +".html")

    context = {
        'id': id,
        'tipo_relatorio': "colheita",
        "rows":rows,
        "columns":columns,
        "graphs":graph
    }
    return HttpResponse(template.render(context, request))

