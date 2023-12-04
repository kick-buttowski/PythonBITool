def get_olist_sample_queries():
    return ['show payment value data by payment type',
            'show average review score data between 3 and 4 grouped by customer state',
            'show top 15 price by customer state',
            'show stock data by shipping limit date',
            'show price by customer state where payment type = credit_card'
            ]


def get_olist_measures():
    return ['price',
            'freight value',
            'payment installments',
            'payment value',
            'review score',
            'product stock',
            'product weight',
            'product length',
            'product width',
            'product height']


def get_olist_dimensions():
    return ['customer zip code',
            'customer city',
            'customer state',
            'latitude',
            'longitude',
            'geolocation city',
            'geolocation state',
            'shipping limit date',
            'payment sequential',
            'payment type',
            'review comment title',
            'review comment message',
            'review creation date',
            'review answer timestamp',
            'order status',
            'order purchase timestamp',
            'order approved at',
            'order delivered carrier date',
            'order delivered customer date',
            'order estimated delivery date',
            'product category name',
            'product name length',
            'product description length',
            'seller zip code',
            'seller city',
            'seller state', ]
