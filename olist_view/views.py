from django.db.models import Sum
from django.shortcuts import render
import plotly.express as px
from plotly.offline import plot
from .nlp_regex.nlp_model_with_aliases import extract_information
from .utils.olist_tables_graph import shortest_path
from .nlp_regex.nlp_model_with_aliases import table_to_model_name
from django.db.models import Subquery, OuterRef

pre_search = ''
x_axis, y_axis, x_axis_label, y_axis_label = [], [], '', ''
queryset = {}


def generate_plotly_plot(plot_type, search_text):
    global pre_search, x_axis, y_axis, x_axis_label, y_axis_label, queryset

    if pre_search != search_text:
        nlp_result = extract_information(search_text.lower())

        if nlp_result['intent'] == 'unknown':
            return 'DISPLAY ERROR MESSAGE'

        print(nlp_result)
        group_by = nlp_result['group_by']
        aggregate = nlp_result['aggregate']

        result = shortest_path(aggregate['table_name'], group_by['table_name'])

        print("Shortest distance:")

        if result:
            path, keys = result
            queryset = table_to_model_name(path[0])

            if len(keys) > 0:
                for x in range(0, len(path)-1):
                    queryset = queryset.objects.select_related(f'{table_to_model_name(path[x+1])}__{keys[x]}').all()

            print(" -> ".join(path))
            print("Keys:", keys)

        print(queryset)
        if nlp_result['intent'] == 'show top':
            queryset = (queryset.objects.values(group_by['column_name']).
                        annotate(sum=Sum(aggregate['column_name'])).order_by('-sum'))[:nlp_result['top_number']]
        elif nlp_result['intent'] == 'show between':
            queryset = (queryset.objects.values(group_by['column_name']).
                        annotate(sum=Sum(aggregate['column_name'])).
                        filter(sum__gte=nlp_result['range_start'], sum__lte=nlp_result['range_end']).order_by())
        elif nlp_result['intent'] == 'show filtered':
            filter_column_icontains = nlp_result['filter_column']['column_name'] + '__icontains'
            queryset = (queryset.objects.values(group_by['column_name'],)
                        .filter(**{filter_column_icontains: nlp_result['filter_value']})
                        .annotate(sum=Sum(aggregate['column_name'])).order_by())
        elif nlp_result['intent'] == 'show':
            queryset = (queryset.objects.values(group_by['column_name']).
                        annotate(sum=Sum(aggregate['column_name'])).order_by())

        print(queryset)
        x_axis_label, y_axis_label = nlp_result['x_label'], nlp_result['y_label']
        x_axis, y_axis = [x[group_by['column_name']] for x in queryset], [y['sum'] for y in queryset]

    if plot_type == 'bar':
        fig = px.bar(x=x_axis, y=y_axis, title=search_text,
                     labels={'x': x_axis_label, 'y': y_axis_label}, color_discrete_sequence=['green'])
    elif plot_type == 'line':
        fig = px.line(x=x_axis, y=y_axis, title=search_text, labels={'x': x_axis_label, 'y': y_axis_label},
                      color_discrete_sequence=['green'])
    elif plot_type == 'scatter':
        fig = px.scatter(x=x_axis, y=y_axis, title=search_text, labels={'x': x_axis_label, 'y': y_axis_label},
                         color_discrete_sequence=['green'])
    elif plot_type == 'pie':
        fig = px.pie({x_axis_label: x_axis, y_axis_label: y_axis}, names=x_axis_label, values=y_axis_label,
                     title=search_text)
    else:
        fig = None

    pre_search = search_text

    if fig:
        plot_div = plot(fig, output_type='div', auto_open=False, include_plotlyjs=False,
                        config={'displayModeBar': False})
        return plot_div
    else:
        return 'DISPLAY ERROR MESSAGE'


def search_view(request):
    search_text = request.POST.get('search_text', '')

    if search_text == '':
        return render(request, 'olist_view/search_template.html',
                      {'plot_div': '', 'search_text': search_text})
    elif str(search_text).lower().strip() == 'help' or str(search_text).lower().strip() == 'help olist':
        return render(request, 'olist_view/search_template.html',
                      {'plot_div': '', 'search_text': str(search_text).lower().strip()})

    plot_type = request.POST.get('plot_type', 'bar')
    plot_div = generate_plotly_plot(plot_type, search_text)
    return render(request, 'olist_view/search_template.html',
                  {'plot_div': plot_div, 'plot_type': plot_type, 'search_text': search_text.strip()})


def dashboard_view(request):
    return render(request, 'olist_view/dashboard_template.html')


def about_view(request):
    return render(request, 'olist_view/about_template.html')
