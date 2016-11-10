# conding = utf-8
from urllib import request, parse
from bs4 import BeautifulSoup as bs


class RequestWrap:
    headers = {
        'User-Agent': '"Mozilla/5.0 (X11; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0"',
        'Host': "daily.zhihu.com"
    }

    def __init__(self):
        pass

    def _asbyte(self, raw):
        if raw is None:
            return None
        return bytes(parse.urlencode(raw), encoding='utf-8')

    def _handle_res(self, res, utf8=True):
        data = res.read()
        if utf8:
            data = data.decode('utf-8')
            return bs(data, 'lxml')
        else:
            return data

    def _send(self, url, method='GET', data=None, headers=None, utf8=True):
        if method not in ['GET', 'POST']:
            raise Exception('method is not implemented')

        data = self._asbyte(data)
        _headers = self.headers.copy()
        if headers:
            _headers.update(headers)
        req = request.Request(url, data, _headers, method=method)
        res = request.urlopen(req)
        if res.status != 200:
            raise Exception('the request is failed with status code:%s' % res.status)
        return self._handle_res(res, utf8)

    def get(self, url, query=None, headers=None, utf8=True):
        return self._send(url, 'GET', query, headers, utf8)

    def post(self, url, body=None, headers=None, utf8=True):
        return self._send(url, 'POST', body, headers, utf8)
