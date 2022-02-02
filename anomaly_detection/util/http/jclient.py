from requests import Session, Response

from .header import HttpHeader, pack


class JsonClient:
    """
    Simple HTTP client to operate on resources that are expected to have
    a JSON representation.
    """

    def __init__(self, timeout=60, verify=True):
        """
        Create a new instance.

        :param timeout: error out if the request takes longer than this.
        :param verify: verify SSL certificates for HTTPS connections.
        """
        self._timeout = timeout
        self._verify = verify
        self._http = Session()

    @staticmethod
    def _handle_response(r: Response) -> dict:
        r.raise_for_status()
        if r.text:
            return r.json()
        return {}

    @staticmethod
    def _prep_headers(hs: [HttpHeader] = None) -> dict:
        if hs:
            return pack(*hs)
        return {}

    def get(self, url: str, headers: [HttpHeader] = None) -> dict:
        """
        GET the JSON resource identified by ``url``.

        :param url: the resource identifier.
        :param headers: any optional headers to add to the request.
        :return: the JSON representation of the resource.
        """
        response = self._http.get(url=url,
                                  headers=self._prep_headers(headers),
                                  timeout=self._timeout,
                                  verify=self._verify)
        return self._handle_response(response)

    def post(self, url: str, json_payload: dict,
             headers: [HttpHeader] = None) -> dict:
        """
        POST a JSON payload.

        :param url: where to post.
        :param json_payload: the data.
        :param headers: any optional headers to add to the request.
            ('Content-Type: application/json' will be added automatically.)
        :return: JSON returned by the server if any.
        """
        response = self._http.post(url=url,
                                   headers=self._prep_headers(headers),
                                   json=json_payload,
                                   timeout=self._timeout,
                                   verify=self._verify)
        return self._handle_response(response)
    # NOTE. Content-Type header. Requests adds application/json automatically
    # when using the 'json' named argument.

    def put(self, url: str, json_payload: dict,
            headers: [HttpHeader] = None) -> dict:
        """
        PUT a JSON representation of the resource identified by ``url``.

        :param url: the resource identifier.
        :param json_payload: the data.
        :param headers: any optional headers to add to the request.
            ('Content-Type: application/json' will be added automatically.)
        :return: JSON returned by the server if any.
        """
        response = self._http.put(url=url,
                                  headers=self._prep_headers(headers),
                                  json=json_payload,
                                  timeout=self._timeout,
                                  verify=self._verify)
        return self._handle_response(response)
    # NOTE. Content-Type header. Requests adds application/json automatically
    # when using the 'json' named argument.

    def delete(self, url: str, headers: [HttpHeader] = None) -> dict:
        """
        DELETE the resource identified by ``url``.

        :param url: the resource identifier.
        :param headers: any optional headers to add to the request.
        :return: JSON returned by the server if any.
        """
        response = self._http.delete(url=url,
                                     headers=self._prep_headers(headers),
                                     timeout=self._timeout,
                                     verify=self._verify)
        return self._handle_response(response)
