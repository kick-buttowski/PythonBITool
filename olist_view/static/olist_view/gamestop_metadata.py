def get_gamestop_sample_queries():
    return ['show gamestop high price grouped by business date',
            'show gamestop top 10 high price by date',
            'show gamestop average high price grouped by date',
            'show gamestop volume between 1 and 10000000 by cob date']


def get_gamestop_measures():
    return ['open price',
            'close price',
            'low price',
            'high price',
            'volume']


def get_gamestop_dimensions():
    return ['business date']
