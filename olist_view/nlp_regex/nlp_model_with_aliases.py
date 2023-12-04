import re
from olist_view.models import (Alias, Customer, Seller, Product, ProductTranslation, OrderPayment, OrderReview,
                               Order, OrderItem, Geolocation, GameStopStockData, GameStopAlias)

aliases = {}
show_data_pattern, top_pattern, filtered_pattern, between_pattern, extract_dataset_pattern = {}, {}, {}, {}, {}


def table_to_model_name(table_name):
    if table_name == 'olist_view_customer':
        return Customer, 'customer'
    elif table_name == 'olist_view_geolocation':
        return Geolocation, 'geolocation'
    elif table_name == 'olist_view_orderitem':
        return OrderItem, 'orderitem'
    elif table_name == 'olist_view_orderpayment':
        return OrderPayment, 'orderpayment'
    elif table_name == 'olist_view_orderreview':
        return OrderReview, 'orderreview'
    elif table_name == 'olist_view_order':
        return Order, 'order'
    elif table_name == 'olist_view_product':
        return Product, 'product'
    elif table_name == 'olist_view_seller':
        return Seller, 'seller'
    elif table_name == 'olist_view_producttranslation':
        return ProductTranslation, 'producttranslation'
    elif table_name == 'olist_view_gamestopstockdata':
        return GameStopStockData, 'gamestopstockdata'


def extract_dataset_info(dataset):
    if dataset == 'gamestop':
        return GameStopAlias
    return Alias


def compile_regex():
    global show_data_pattern, top_pattern, filtered_pattern, between_pattern, extract_dataset_pattern

    available_datasets = 'gamestop|olist'
    average_alias = 'average|avg'
    group_by_alias = "group by|by|grouped by|divided by"
    aggregator_attach_alias = "data|result|results"
    show_alias = "show|display"
    top_alias = "top|upper"
    multiple_words_capture = r"((?:\w+\s*)*)"
    filter_alias = "where|but"
    filter_bridge_alias = "is|is not|are|are not|>|>=|=|<|<=|!=|greater than|less than|equals"
    between_alias = "between|in the range of"
    between_bridge_alias = "and|,"

    extract_dataset_pattern = re.compile(
        r"(?:(" + show_alias + r")\s+)?(?:(" + available_datasets + r")\s+)?" + multiple_words_capture, re.IGNORECASE)

    show_data_pattern = re.compile(
        r"(?:(" + show_alias + r")\s+)?(?:(" + available_datasets + r")\s+)?(?:(" + average_alias + r")\s+)?((?:(?!("
        + aggregator_attach_alias + '|' + group_by_alias + '|' + top_alias +
        r"))\w+\s*)*)\s+(?:(" + aggregator_attach_alias +
        r")\s+)?(?:(" + group_by_alias + r")\s+)?" + multiple_words_capture, re.IGNORECASE)

    top_pattern = re.compile(
        r"(?:(" + show_alias + r")\s+)?(?:(" + available_datasets + r")\s+)?(?:(" + average_alias + r")\s+)?(?:("
        + top_alias + r")\s+)?(\d+)\s+((?:(?!(" + aggregator_attach_alias + '|'
        + group_by_alias + r"))\w+\s*)*)\s+(?:(" + aggregator_attach_alias +
        r")\s+)?(?:(" + group_by_alias + r")\s+)?" + multiple_words_capture, re.IGNORECASE)

    filtered_pattern = re.compile(
        r"(?:(" + show_alias + r")\s+)?(?:(" + available_datasets + r")\s+)?(?:(" + average_alias + r")\s+)?((?:(?!("
        + aggregator_attach_alias + '|' + group_by_alias +
        r"))\w+\s*)*)\s+(?:(" + aggregator_attach_alias + r")\s+)?(?:(" + group_by_alias + r")\s+)?" + multiple_words_capture +
        r"\s+(" + filter_alias + r")\s+((?:(?!(" + filter_bridge_alias + r"))\w+\s*)*)\s+(?:(" +
        filter_bridge_alias + r")\s+)?" + multiple_words_capture, re.IGNORECASE)

    between_pattern = re.compile(
        r"(?:(" + show_alias + r")\s+)?(?:(" + available_datasets + r")\s+)?(?:(" + average_alias + r")\s+)?((?:(?!("
        + aggregator_attach_alias + '|' + group_by_alias + '|' + between_alias +
        r"))\w+\s*)*)\s+(?:(" + aggregator_attach_alias + r")\s+)?(?:(" + between_alias + r")\s+)?(\d+)\s+(?:("
        + between_bridge_alias + r")\s+)?(\d+)\s+(?:(" + group_by_alias + r")\s+)?" + multiple_words_capture,
        re.IGNORECASE)


def extract_information(query):
    global aliases, show_data_pattern, top_pattern, filtered_pattern, between_pattern

    dataset_extract = extract_dataset_pattern.match(query)

    dataset_alias = extract_dataset_info(dataset_extract.group(2))

    aliases = {alias.aliases.lower(): {"column_name": alias.column_name,
                                       "table_name": alias.table_name,
                                       "model_name": table_to_model_name(alias.table_name)[0]} for alias in
               dataset_alias.objects.all()}

    top = top_pattern.match(query)
    if top:
        intent = "show top"
        top_number = int(top.group(5))
        aggregate = top.group(6)
        group_by = top.group(10)
        json_return = {'intent': intent, 'top_number': top_number, 'aggregate': aliases.get(aggregate.lower().strip()),
                       'group_by': aliases.get(group_by.lower().strip()), 'x_label': group_by, 'y_label': aggregate,
                       'average': 'average' in str(top.group(3)) or 'avg' in str(top.group(3))}
        validated_json = validate_json(json_return)
        if validated_json['intent'] == 'unknown':
            pass
        else:
            return validated_json

    between = between_pattern.match(query)
    if between:
        intent = "show between"
        aggregate = between.group(4)
        group_by = between.group(12)
        range_start = float(between.group(8))
        range_end = float(between.group(10))
        json_return = {'intent': intent, 'aggregate': aliases.get(aggregate.lower().strip()),
                       'group_by': aliases.get(group_by.lower().strip()),
                       'range_start': range_start, 'range_end': range_end, 'x_label': group_by, 'y_label': aggregate,
                       'average': 'average' in str(between.group(3)) or 'avg' in str(between.group(3))}
        validated_json = validate_json(json_return)
        if validated_json['intent'] == 'unknown':
            pass
        else:
            return validated_json

    show = show_data_pattern.match(query)
    if show:
        intent = "show"
        aggregate = show.group(4)
        group_by = show.group(8)
        json_return = {'intent': intent, 'aggregate': aliases.get(aggregate.lower().strip()),
                       'group_by': aliases.get(group_by.lower().strip()), 'x_label': group_by, 'y_label': aggregate,
                       'average': 'average' in str(show.group(3)) or 'avg' in str(show.group(3))}
        validated_json = validate_json(json_return)
        if validated_json['intent'] == 'unknown':
            pass
        else:
            return validated_json

    filtered = filtered_pattern.match(query)
    if filtered:
        intent = "show filtered"
        aggregate = filtered.group(4)
        group_by = filtered.group(8)
        filter_column = filtered.group(10)
        what_filter = filtered.group(12)
        filter_value = filtered.group(13)
        json_return = {'intent': intent, 'aggregate': aliases.get(aggregate.lower().strip()),
                       'group_by': aliases.get(group_by.lower().strip()),
                       'filter_column': aliases.get(filter_column.lower().strip()), 'what_filter': what_filter,
                       'filter_value': filter_value.strip(), 'x_label': group_by, 'y_label': aggregate,
                       'average': 'average' in str(filtered.group(3)) or 'avg' in str(filtered.group(3))}
        return validate_json(json_return)

    return {'intent': 'unknown'}


def validate_json(json_return):
    result = list(filter(lambda key: json_return[key] is None, json_return))
    if result:
        return {'intent': 'unknown'}
    return json_return


compile_regex()
