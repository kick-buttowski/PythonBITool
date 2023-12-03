import re
from olist_view.models import (Alias, Customer, Seller, Product, ProductTranslation, OrderPayment, OrderReview,
                               Order, OrderItem, Geolocation)


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


def extract_information(query):
    aliases = {alias.aliases.lower(): {"column_name": alias.column_name,
                                       "table_name": alias.table_name,
                                       "model_name": table_to_model_name(alias.table_name)[0]} for alias in
               Alias.objects.all()}

    show_data_pattern = re.compile(r'(show|display)? (\w+(\s\w+)*) (data|results)? by (\w+(\s\w+)*)')
    top_pattern = re.compile(r'(show|display)? top (\d+) (\w+(\s\w+)*) by (\w+(\s\w+)*)')
    filtered_pattern = re.compile(r'(show|display)? (\w+(\s\w+)*) by (\w+(\s\w+)*) (but|where) (\w+(\s\w+)*) is (\w+('
                                  r'\s\w+)*)')
    between_pattern = re.compile(r'(show|display)? (\w+(\s\w+)*) by (\w+(\s\w+)*) between (\d+) and (\d+)')

    show_match = show_data_pattern.match(query)
    top_match = top_pattern.match(query)
    filtered_match = filtered_pattern.match(query)
    between_match = between_pattern.match(query)

    if top_match:
        intent = "show top"
        top_number = int(top_match.group(2))
        aggregate = top_match.group(3)
        group_by = top_match.group(5)
        return {'intent': intent, 'top_number': top_number, 'aggregate': aliases.get(aggregate.lower().strip()),
                'group_by': aliases.get(group_by.lower().strip()), 'x_label': group_by, 'y_label': aggregate}

    elif filtered_match:
        intent = "show filtered"
        aggregate = filtered_match.group(2)
        group_by = filtered_match.group(4)
        filter_column = filtered_match.group(7)
        filter_value = filtered_match.group(9)
        return {'intent': intent, 'aggregate': aliases.get(aggregate.lower().strip()),
                'group_by': aliases.get(group_by.lower().strip()),
                'filter_column': aliases.get(filter_column.lower().strip()),
                'filter_value': filter_value.strip(), 'x_label': group_by, 'y_label': aggregate}

    elif between_match:
        intent = "show between"
        aggregate = between_match.group(2)
        group_by = between_match.group(4)
        range_start = int(between_match.group(6))
        range_end = int(between_match.group(7))
        return {'intent': intent, 'aggregate': aliases.get(aggregate.lower().strip()),
                'group_by': aliases.get(group_by.lower().strip()),
                'range_start': range_start, 'range_end': range_end, 'x_label': group_by, 'y_label': aggregate}

    elif show_match:
        intent = "show"
        print(aliases.get(show_match.group(5)))
        aggregate = show_match.group(2)
        group_by = show_match.group(5)
        return {'intent': intent, 'aggregate': aliases.get(aggregate.lower().strip()),
                'group_by': aliases.get(group_by.lower().strip()), 'x_label': group_by, 'y_label': aggregate}

    else:
        return {'intent': 'unknown'}


queries = [
    "show product cost data by customer state",
    "show top 10 product cost by customer state",
    "display fare data by customer state",
    "display fare by customer state where state is SP",
    "show product cost by customer state between 0 and 400",
]

# Process queries
# for query in queries:
#     result = extract_information(query)
#     print(f"User Query: '{query}'")
#     print(f"Result: {result}\n")
