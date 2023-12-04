from django.shortcuts import render

from .static.olist_view.gamestop_metadata import get_gamestop_measures, get_gamestop_sample_queries, \
    get_gamestop_dimensions
from .static.olist_view.olist_metadata import get_olist_measures, get_olist_dimensions, get_olist_sample_queries
from .utils.olist_utils import generate_plotly_plot, save_to_dashboard, clear_cache, get_dashboards


def search_view(request):
    dashboard_name = request.POST.get('dashboard_name', '')
    search_text = request.POST.get('search_text', '')

    if request.method == 'POST' and len(dashboard_name) > 0:
        # Default public dashboard, private dashboard feature to be added later
        save_to_dashboard('public', dashboard_name)
        clear_cache()
        return render(request, 'olist_view/search_template.html',
                      {'plot_divs': [], 'error': '', 'plot_type': 'bar', 'search_text': ''})
    elif search_text == '':
        return render(request, 'olist_view/search_template.html', {'plot_div': '', 'search_text': ''})
    elif 'help' in str(search_text).lower().strip():
        if str(search_text).lower().strip() == 'help' or str(search_text).lower().strip() == 'help olist':
            return render(request, 'olist_view/search_template.html',
                          {'plot_divs': generate_plotly_plot('bar', search_text)[1], 'plot_div': '',
                           'search_text': str(search_text).lower().strip(),
                           'measures': get_olist_measures(), 'dimensions': get_olist_dimensions(),
                           'sample_queries': get_olist_sample_queries()})
        elif str(search_text).lower().strip() == 'help gamestop':
            return render(request, 'olist_view/search_template.html',
                          {'plot_divs': generate_plotly_plot('bar', search_text)[1], 'plot_div': '',
                           'search_text': str(search_text).lower().strip(),
                           'measures': get_gamestop_measures(), 'dimensions': get_gamestop_dimensions(),
                           'sample_queries': get_gamestop_sample_queries()})
    else:
        plot_type = request.POST.get('plot_type', 'bar')
        error, plot_divs = generate_plotly_plot(plot_type, search_text)
        return render(request, 'olist_view/search_template.html',
                      {'plot_divs': plot_divs, 'error': error, 'plot_type': plot_type,
                       'search_text': search_text.strip()})


def dashboard_view(request):
    dashboard_names, dashboard_content = get_dashboards()
    return render(request, 'olist_view/dashboard_template.html', {'dashboards': dashboard_names})


def ind_dashboard_view(request, dashboard_name):
    dashboard_names, dashboard_content = get_dashboards()
    plot_divs = []
    clear_cache()
    for search_text in dashboard_content[dashboard_name]:
        _, plot_divs = generate_plotly_plot('bar', search_text)
    print(plot_divs)
    return render(request, 'olist_view/ind_dashboard_template.html',
                  {'dashboard_content': plot_divs, 'dashboard_name': dashboard_name})


def about_view(request):
    return render(request, 'olist_view/about_template.html')
