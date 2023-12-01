import networkx as nx

relationships = [
    ('olist_view_orderreview', 'order_id', 'olist_view_order'),
    ('olist_view_orderpayment', 'order_id', 'olist_view_order'),
    ('olist_view_orderitem', 'order_id', 'olist_view_order'),
    ('olist_view_customer', 'customer_id', 'olist_view_order'),
    ('olist_view_product', 'product_id', 'olist_view_orderitem'),
    ('olist_view_orderitem', 'seller_id', 'olist_view_seller'),
    ('olist_view_seller', 'zip_code_prefix', 'olist_view_geolocation'),
    ('olist_view_geolocation', 'zip_code_prefix', 'olist_view_customer'),
]

G = nx.Graph()

for source, key, target in relationships:
    G.add_edge(source, target, key=key)


def shortest_path(source_table, target_table):
    try:
        path = nx.shortest_path(G, source_table, target_table)
        keys = [G[path[i]][path[i + 1]]['key'] for i in range(len(path) - 1)]
        return path, keys
    except nx.NetworkXNoPath:
        return None


source_table = 'olist_view_orderreview'
target_table = 'olist_view_geolocation'

result = shortest_path(source_table, target_table)

if result:
    path, keys = result
    print(f"Shortest path from {source_table} to {target_table}:")
    print(" -> ".join(path))
    print("Keys:", keys)
else:
    print(f"No path found from {source_table} to {target_table}.")
