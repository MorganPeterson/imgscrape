import itertools
import requests
import sys

from bs4 import BeautifulSoup
from functools import partial
from multiprocessing import Pool

if sys.version_info < (3,):
    # faster in all versions python2
    rng = xrange
else:
    # xrange doesn't exist in 3
    rng = range


config = {
    "url": "http://www.google.com/search",
    "user_agent": "mozilla/11.0",
    "processes": "1",
    "pages": "1",
    "link": "gstatic.com",
    "tag": "img",
    "class": "rg_i",
    "kwargs": {
        "prc": "processes",
        "pgs": "pages",
        "trm": "term"
    }
}


def get_urls(search_string, start):
    """ the heavy lifter... grab url and parse """
    url = config['url']
    pay = {'q': search_string, 'tbm': 'isch', 'tbs': 'isz:1'}
    hdr = {'user-agent': config['user_agent']}

    res = requests.get(url, params=pay, headers=hdr)
    sop = BeautifulSoup(res.text, 'html.parser')
    h3t = sop.find_all(config['tag'])
    tmp = []
    # use for loop here due to pickling issues in multiprocessing
    for h3 in h3t:
        try:
            tmp.append(h3['src'])
        except:
            continue
    return tmp


def scanner(search, pages, processes):
    """ scans google pages using multi-processing """
    prcsss = int(processes)
    mk_rqts = partial(get_urls, search)
    pge_lst = [str(x * 10) for x in rng(0, int(pages))]

    p = Pool(prcsss)
    tmp = p.map(mk_rqts, pge_lst)

    result = [x for x in tmp]

    return list(itertools.chain.from_iterable(result))


def imgscrape(**kwargs):
    """ main function """
    pgs = kwargs.get(config['kwargs']['pgs'], config['pages'])
    prc = kwargs.get(config['kwargs']['prc'], config['processes'])

    srch_trm = kwargs.get(config['kwargs']['trm'], '')

    result = scanner(srch_trm, pgs, prc)
    print(result)
