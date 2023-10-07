from django.shortcuts import render
import plotly.express as px
import pandas as pd

from django.shortcuts import render
import plotly.express as px

def index(request):
    # Variables para almacenar los datos
    años = []
    no_smoothing = []
    lowess = []

    # Leer los datos desde el archivo "data.txt"
    with open('clima/data.txt', 'r') as file:
        lines = file.readlines()

    # Procesar las líneas para extraer los datos
    for i, line in enumerate(lines):
        if i >= 5:  # Saltar las primeras 5 líneas de encabezado
            parts = line.strip().split()
            if len(parts) == 3:
                año, no_smooth, lowess_value = parts
                años.append(int(año))
                no_smoothing.append(float(no_smooth.replace(',', '.')))
                lowess.append(float(lowess_value.replace(',', '.')))


    start_year = int(request.GET.get('start_year', 1880))
    end_year = int(request.GET.get('end_year', max(años)))

    if start_year and end_year:

        años_filtrados = []
        no_smoothing_filtrado = []
        lowess_filtrado = []

        for i in range(len(años)):
            if start_year <= años[i] <= end_year:
                años_filtrados.append(años[i])
                no_smoothing_filtrado.append(no_smoothing[i])
                lowess_filtrado.append(lowess[i])

        fig = px.line(
            x=años_filtrados,
            y=[no_smoothing_filtrado, lowess_filtrado],
            title='Índice de temperatura tierra-océano (C) entre {} y {}'
                .format(start_year, end_year),
            labels={'x': 'Año', 'y': 'Temperatura (C)'},
        )
    else:
        fig = px.line(
            x=años,
            y=[no_smoothing, lowess],
            title='Índice de temperatura tierra-océano (C)',
            labels={'x': 'Año', 'y': 'Temperatura (C)'},
        )

    # Convertir el gráfico en HTML
    chart = fig.to_html()

    return render(request, 'clima/reporte_clima.html', {
        'chart': chart,
        'años': años,
        'no_smoothing': no_smoothing,
        'lowess': lowess,
    })



