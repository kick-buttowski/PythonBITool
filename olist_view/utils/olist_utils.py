import sqlite3

from django.db.models import Sum, Avg
import plotly.express as px
from plotly.offline import plot

from olist_view.models import PublicDashboards
from olist_view.nlp_regex.nlp_model_with_aliases import extract_information, table_to_model_name
from olist_view.utils.olist_tables_graph import shortest_path

ERROR = 'DISPLAY ERROR MESSAGE'
pre_search = ''
x_axis, y_axis, x_axis_label, y_axis_label = [], [], '', ''
plot_divs = []
plot_div_text = set()


def validate_nlp_result(nlp_result):
    if nlp_result['intent'] == 'unknown' or nlp_result['group_by'] is None or nlp_result['aggregate'] is None:
        return ERROR
    return ''


def generate_plotly_plot(plot_type, search_text):
    global pre_search, x_axis, y_axis, x_axis_label, y_axis_label, plot_div_text, plot_divs

    if pre_search != search_text:
        nlp_result = extract_information(search_text.lower())

        if validate_nlp_result(nlp_result) == ERROR:
            return ERROR, plot_divs

        print(nlp_result)

        group_by = nlp_result['group_by']
        aggregate = nlp_result['aggregate']

        result = shortest_path(group_by['table_name'], aggregate['table_name'])

        if result:
            path, keys = result
            print("Shortest distance:")
            print(" -> ".join(path))
            print(keys)

            paths = [table_to_model_name(p)[1] for p in path[1:]]
            agg_prefix = ("__".join(paths) + "__") if len(keys) > 0 else ""
            print(agg_prefix + aggregate['column_name'])

            try:
                queryset = (table_to_model_name(path[0])[0].objects.values(group_by['column_name'])
                            .annotate(sum=Avg(agg_prefix + aggregate['column_name']) if nlp_result['average']
                            else Sum(agg_prefix + aggregate['column_name'])))
            except Exception:
                queryset = (table_to_model_name(path[0])[0].objects.values(group_by['column_name'])
                            .annotate(sum=Avg(agg_prefix + aggregate['column_name']) if nlp_result['average']
                            else Sum(agg_prefix + aggregate['column_name'])))

            if nlp_result['intent'] == 'show top':
                queryset = (queryset.order_by('-sum')[:nlp_result['top_number']])
            elif nlp_result['intent'] == 'show between':
                queryset = (queryset.filter(sum__gte=nlp_result['range_start'], sum__lte=nlp_result['range_end'])
                            .order_by())
            elif nlp_result['intent'] == 'show filtered':
                path_filter, keys_filter = shortest_path(group_by['table_name'],
                                                         nlp_result['filter_column']['table_name'])
                path_keys = [table_to_model_name(p)[1] for p in path_filter[1:]]
                agg_prefix_keys = ("__".join(keys_filter) + "__") if len(path_keys) > 0 else ""
                agg_prefix_path_keys = ("__".join(path_keys) + "__") if len(path_keys) > 0 else ""
                try:
                    filter_column_icontains = agg_prefix_path_keys + nlp_result['filter_column'][
                        'column_name'] + '__icontains'
                    queryset = queryset.filter(**{filter_column_icontains: nlp_result['filter_value']})
                except Exception:
                    filter_column_icontains = agg_prefix_keys + nlp_result['filter_column'][
                        'column_name'] + '__icontains'
                    queryset = queryset.filter(**{filter_column_icontains: nlp_result['filter_value']})
                queryset = queryset.order_by()
                print(queryset)
            elif nlp_result['intent'] == 'show':
                queryset = (queryset.order_by())
            else:
                return ERROR, plot_divs

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

    if fig:
        plot_div = plot(fig, output_type='div', auto_open=False, include_plotlyjs=False,
                        config={'displayModeBar': False})

        if search_text != pre_search:
            plot_divs.insert(0, plot_div)
        else:
            plot_divs[0] = plot_div
        plot_div_text.add(search_text)
        pre_search = search_text
        return '', plot_divs
    else:
        pre_search = search_text
        return ERROR, plot_divs


def save_to_dashboard(dashboard_type, dashboard_name):
    global plot_div_text, plot_divs
    if dashboard_type == "public":
        for search in plot_div_text:
            try:
                PublicDashboards.objects.create(**{'dashboard_name': dashboard_name, 'search_text': search})
            except Exception:
                print(f'Combination of {dashboard_name} and {search} already exists!')
                continue


def get_dashboards():
    queryset = (PublicDashboards.objects.all().values())
    dashboard_names = (set(x['dashboard_name'] for x in queryset))
    dashboard_content = {}
    for x in queryset:
        dashboard_content.setdefault(x['dashboard_name'], []).append(x['search_text'])

    return dashboard_names, dashboard_content


def clear_cache():
    global pre_search, plot_divs, plot_div_text
    pre_search = ''
    plot_divs = []
    plot_div_text = set()
