# Author: Tahnasib Gafarov
# This library can be used to translate words via Google Translate Api. It includes, definitions, synonyms, examples, alternatives
# It can be develop more, it can go may faster and efficient.
import json
from dataclasses import dataclass, asdict
from typing import Any

from aiohttp import ClientSession
from aiohttp.client import ClientTimeout
from dataclasses import dataclass, field


@dataclass
class Translation:
    translator: str
    sl: str
    tl: str
    text: str
    paraphrase: str = ""
    explains: dict[str, str] = field(default_factory=dict)
    details: dict[str, dict[str, str]] = field(default_factory=dict)
    alternatives: list[str] = field(default_factory=list)
    definitions: dict[str, dict[str, str]] = field(default_factory=dict)
    examples: dict[str, dict[str, str]] = field(default_factory=dict)
    synonyms: dict[str, dict[str, str]] = field(default_factory=dict)


@dataclass
class GoogleTranslator:
    name: str = "google"
    host: str = "translate.googleapis.com"

    async def __call__(self, text: str, tl: str, sl: str, option: dict[str, Any]):
        res = self.create_translation(text, tl, sl)
        url = f"https://{self.host}/translate_a/single"
        params = {
            "client": "gtx",
            "sl": sl,
            "tl": tl,
            "dt": ["at", "bd", "ex", "ld", "md", "qca", "rw", "rm", "ss", "t"],
            "q": text,
        }
        session = option.get(self.name, {}).get("session", None)
        resp = await self.http_get(url, session, params)
        if not resp:
            return None
        obj = json.loads(resp)
        res.paraphrase = self.get_paraphrase(obj)
        res.explains = self.get_explains(obj)
        res.details, res.definitions, res.examples, res.synonyms = self.get_details(obj)
        res.alternatives = self.get_alternatives(obj)
        return asdict(res)

    @staticmethod
    def get_explains(obj: list[Any]) -> dict[str, str]:
        expls = {}
        if obj[1]:
            for x in obj[1]:
                expls[x[0]] = ""
                for i in x[2]:
                    expls[x[0]] += i[0] + "; "
        return expls

    @staticmethod
    def get_paraphrase(obj: list[Any]) -> str:
        """Get paraphrase.

        :param obj:
        :type obj: list[Any]
        :rtype: str
        """
        paraphrase = ""
        for x in obj[0]:
            if x[0]:
                paraphrase += x[0]
        return paraphrase

    @staticmethod
    def get_explains(obj: list[Any]) -> dict[str, str]:
        """Get explains.

        :param obj:
        :type obj: list[Any]
        :rtype: dict[str, str]
        """
        expls = {}
        if obj[1]:
            for x in obj[1]:
                expls[x[0]] = ""
                for i in x[2]:
                    expls[x[0]] += i[0] + "; "
        return expls

    @staticmethod
    def get_details(resp: list[Any]) -> [dict, dict, dict, dict]:
        result = {}
        get_definitions: dict[str, list[str]] = {}
        get_examples: dict[str, list[str]] = {}
        get_synonyms: dict[str, list[str]] = {}
        if len(resp) < 13 or resp[12] is None:
            return result, get_definitions, get_examples, get_synonyms
        for jj, x in enumerate(resp[12]):
            result[x[0]] = {}
            for ii, y in enumerate(x[1]):
                tt = {"explanation": y[0]}
                if x[0] in get_definitions:
                    get_definitions[x[0]].append(y[0])
                else:
                    get_definitions[x[0]] = [y[0]]
                if len(y) > 2 and isinstance(y[2], str):
                    example = y[2]
                    if x[0] in get_examples:
                        get_examples[x[0]].append(y[2])
                    else:
                        get_examples[x[0]] = [y[2]]
                else:
                    example = ""
                tt["example"] = example
                # TODO this need to upgrade
                try:
                    if (
                        resp[11]
                        and len(resp[11]) > jj
                        and len(resp[11][jj]) > 1
                        and len(resp[11][jj][1]) > ii
                        and len(resp[11][jj][1][ii]) > 1
                        and isinstance(resp[11][jj][1][ii][1], str)
                    ):
                        # synonims
                        tt["synonym"] = resp[11][jj][1][ii][0]
                        if x[0] in get_synonyms:
                            get_synonyms[x[0]].extend(tt["synonym"])
                        else:
                            get_synonyms[x[0]] = [*tt["synonym"]]
                    else:
                        tt["synonym"] = []
                except:
                    tt["synonym"] = []

                result[x[0]][str(ii)] = tt
        return result, get_definitions, get_examples, get_synonyms

    def get_alternatives(self, resp: list[Any]) -> list[str]:
        """Get alternatives.

        :param resp:
        :type resp: list[Any]
        :rtype: list[str]
        """
        if len(resp) < 6 or resp[5] is None:
            return []
        definition = self.get_paraphrase(resp)
        result = []
        for x in resp[5]:
            if x[2] is None:
                continue
            for i in x[2]:
                if i[0] != definition:
                    result.append(i[0])
        return result

    async def http_get(
        self,
        url: str,
        session: ClientSession | None,
        params: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
        cookies: dict[str, Any] | None = None,
        timeout: int = 3,
    ):
        if session is None:
            session = ClientSession()
        text = ""
        try:
            async with session.get(
                url,
                params=params,
                headers=headers,
                cookies=cookies,
                timeout=ClientTimeout(timeout),
            ) as resp:
                text = await resp.text()
        except TimeoutError:
            print("Translator %s timed out, please check your network", self.name)
        await session.close()
        return text

    def create_translation(self, text: str, tl: str, sl: str) -> Translation:
        return Translation(self.name, sl, tl, text)
