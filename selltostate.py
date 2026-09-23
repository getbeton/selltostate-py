# Generated from OpenAPI. Do not edit methods by hand.
import json
import os
from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "https://app.selltostate.com"


class AuthError(Exception):
    status = 401

    def __init__(self, body):
        super().__init__("unauthorized")
        self.body = body


class PaymentError(Exception):
    status = 402

    def __init__(self, body):
        super().__init__("payment_required")
        self.body = body or {}
        self.payment_link = self.body.get("payment_link") if isinstance(self.body, dict) else None
        self.plan = self.body.get("plan") if isinstance(self.body, dict) else None
        self.machine_payment = self.body.get("machine_payment") if isinstance(self.body, dict) else None


class RateLimitError(Exception):
    status = 429

    def __init__(self, body):
        super().__init__("rate_limited")
        self.body = body


class SellToState:
    def __init__(self, api_key=None, client_id=None, base_url=None, transport=None):
        self.api_key = api_key if api_key is not None else os.environ.get("STS_API_KEY")
        self.client_id = client_id
        self.base_url = (base_url or os.environ.get("STS_API_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.transport = transport

    def request(self, method, path, args, path_params):
        url_path = path
        for name in path_params:
            value = args.get(name)
            if value is None or value == "":
                raise ValueError("missing path param: " + name)
            url_path = url_path.replace("{" + name + "}", quote(str(value), safe=""))
        query = []
        for key, value in args.items():
            if key in path_params or key == "body" or value is None or value == "":
                continue
            query.append((key, str(value)))
        url = self.base_url + url_path
        if query:
            url += "?" + urlencode(query)
        headers = {"accept": "application/json"}
        if self.api_key:
            headers["x-api-key"] = self.api_key
        elif self.client_id:
            headers["authorization"] = "Bearer client:" + self.client_id
        data = None
        if args.get("body") is not None and method != "GET":
            headers["content-type"] = "application/json"
            data = json.dumps(args["body"]).encode()
        if self.transport:
            status, text = self.transport(url, method, headers, data)
        else:
            req = Request(url, data=data, headers=headers, method=method)
            try:
                with urlopen(req) as res:
                    status, text = res.status, res.read().decode()
            except Exception as exc:
                status = getattr(exc, "code", None)
                raw = getattr(exc, "read", lambda: b"")()
                text = raw.decode() if raw else ""
                if status not in (401, 402, 429):
                    raise
        parsed = None
        if text:
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                parsed = text
        if status == 401:
            raise AuthError(parsed)
        if status == 402:
            raise PaymentError(parsed)
        if status == 429:
            raise RateLimitError(parsed)
        if status is None or status >= 400:
            raise RuntimeError("HTTP " + str(status))
        return parsed

    def searchAwards(self, args=None):
        return self.request("GET", "/api/v1/awards", args or {}, [])

    def exportAwardsCsv(self, args=None):
        return self.request("GET", "/api/v1/awards.csv", args or {}, [])

    def getPrice(self, args=None):
        return self.request("GET", "/api/v1/price", args or {}, [])

    def payAutonomously(self, args=None):
        return self.request("POST", "/api/v1/pay", args or {}, [])

    def registerClient(self, args=None):
        return self.request("POST", "/api/oidc/register", args or {}, [])

    def mcp(self, args=None):
        return self.request("POST", "/api/mcp", args or {}, [])

    def protectedResourceMetadata(self, args=None):
        return self.request("GET", "/.well-known/oauth-protected-resource", args or {}, [])

    def authorizationServerMetadata(self, args=None):
        return self.request("GET", "/.well-known/oauth-authorization-server", args or {}, [])

    def whoami(self, args=None):
        return self.request("GET", "/api/v1/whoami", args or {}, [])

    def search(self, args=None):
        return self.request("GET", "/api/v1/search", args or {}, [])

    def listBuyers(self, args=None):
        return self.request("GET", "/api/v1/buyers", args or {}, [])

    def getBuyer(self, args=None):
        return self.request("GET", "/api/v1/buyers/{slug}", args or {}, ["slug"])

    def listSuppliers(self, args=None):
        return self.request("GET", "/api/v1/suppliers", args or {}, [])

    def getSupplier(self, args=None):
        return self.request("GET", "/api/v1/suppliers/{slug}", args or {}, ["slug"])

    def listSectors(self, args=None):
        return self.request("GET", "/api/v1/sectors", args or {}, [])

    def getSector(self, args=None):
        return self.request("GET", "/api/v1/sectors/{slug}", args or {}, ["slug"])

    def getTender(self, args=None):
        return self.request("GET", "/api/v1/tenders/{id}", args or {}, ["id"])

    def getLists(self, args=None):
        return self.request("GET", "/api/v1/lists", args or {}, [])

    def createList(self, args=None):
        return self.request("POST", "/api/v1/lists", args or {}, [])

    def getList(self, args=None):
        return self.request("GET", "/api/v1/lists/{id}", args or {}, ["id"])

    def renameList(self, args=None):
        return self.request("PATCH", "/api/v1/lists/{id}", args or {}, ["id"])

    def deleteList(self, args=None):
        return self.request("DELETE", "/api/v1/lists/{id}", args or {}, ["id"])

    def addToList(self, args=None):
        return self.request("POST", "/api/v1/lists/{id}/items", args or {}, ["id"])

    def removeFromList(self, args=None):
        return self.request("DELETE", "/api/v1/lists/{id}/items", args or {}, ["id"])

    def getSavedSearches(self, args=None):
        return self.request("GET", "/api/v1/saved-searches", args or {}, [])

    def saveSearch(self, args=None):
        return self.request("POST", "/api/v1/saved-searches", args or {}, [])

    def getSavedSearch(self, args=None):
        return self.request("GET", "/api/v1/saved-searches/{id}", args or {}, ["id"])

    def renameSavedSearch(self, args=None):
        return self.request("PATCH", "/api/v1/saved-searches/{id}", args or {}, ["id"])

    def deleteSavedSearch(self, args=None):
        return self.request("DELETE", "/api/v1/saved-searches/{id}", args or {}, ["id"])
