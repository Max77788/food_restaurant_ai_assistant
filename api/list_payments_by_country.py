from pprint import pprint

from api.utilities import make_request

response = make_request(method='get',
                        path=f'/v1/payment_methods/countries/IS?currency=ISK')

pprint(response)