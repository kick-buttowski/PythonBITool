import re


def extract_information(query):
    show_pattern = re.compile(r'show (.+?) by (.+?)')
    top_pattern = re.compile(r'show top (\d+) (.+?) by (.+)')
    filtered_pattern = re.compile(r'show (.+?) by (.+?) where (.+?) is (.+?)')
    between_pattern = re.compile(r'show (.+?) by (.+?) between (\d+) and (\d+)')

    top_match = top_pattern.match(query)
    filtered_match = filtered_pattern.match(query)
    between_match = between_pattern.match(query)
    show_match = show_pattern.match(query)

    if top_match:
        top_number = int(top_match.group(1))
        aggregate = top_match.group(2)
        group_by = top_match.group(3)
        return {'query_type': 'show top', 'top_number': top_number, 'aggregate': aggregate, 'group_by': group_by}

    elif filtered_match:
        aggregate = filtered_match.group(1)
        group_by = filtered_match.group(2)
        filter_column = filtered_match.group(3)
        filter_value = filtered_match.group(4)
        return {'query_type': 'show filtered', 'aggregate': aggregate, 'group_by': group_by,
                'filter_column': filter_column, 'filter_value': filter_value}

    elif between_match:
        aggregate = between_match.group(1)
        group_by = between_match.group(2)
        range_start = int(between_match.group(3))
        range_end = int(between_match.group(4))
        return {'query_type': 'show between', 'aggregate': aggregate, 'group_by': group_by,
                'range_start': range_start, 'range_end': range_end}

    elif show_match:
        aggregate = show_match.group(1)
        group_by = show_match.group(2)
        return {'query_type': 'show', 'aggregate': aggregate, 'group_by': group_by}

    else:
        return {'query_type': 'unknown'}


queries = [
    "show top 10 sales by year",
    "show sales by year where product category is mobiles",
    "show sales by year between 200 and 400"
]

# Process queries
for query in queries:
    result = extract_information(query)
    print(f"User Query: '{query}'")
    print(f"Result: {result}\n")
