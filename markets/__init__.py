from markets import ozon
from markets import citilink
from markets import beru
from markets import technopoint



def start_parsing_all(url={}):
    return_array = {}

    return_array['ozon'] = start_parsing_ozon(url['ozon'])
    return_array['citilink'] = start_parsing_citilink(url['citilink'])
    return_array['beru'] = start_parsing_beru(url['beru'])
    return_array['dns'] = start_parsing_technopoint(url['dns'])

    return return_array

def start_parsing_ozon(url):
    ozon_market = ozon.Ozon()
    return ozon_market.get_parser_result(url)

def start_parsing_beru(url):
    beru_market = beru.Beru()
    return beru_market.get_parser_result(url)

def start_parsing_citilink(url):
    citilink_market = citilink.Citilink()
    return citilink_market.get_parser_result(url)

def start_parsing_technopoint(url):
    technopoint_market = technopoint.Technopoint()
    return technopoint_market.get_parser_result(url)