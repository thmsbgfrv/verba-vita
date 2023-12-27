from src.gtranslator import GoogleTranslator


# this function translate word coming from api view with GoogleTranslator
async def translate(word, to, source):
    result = await GoogleTranslator()(word, to, source, {})
    data = {"word": word, "sl": source, "langs": {}}
    if result:
        data["langs"][to] = {
            "translation": result.get("paraphrase", None),
            "details": result.get("details", {}),
        }
        data["definitions"] = result.get("definitions", {})
        data["examples"] = result.get("examples", {})
        data["synonyms"] = result.get("synonyms", {})
    return data
