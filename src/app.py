from fastapi import FastAPI
import motor.motor_asyncio
from src.settings import settings
from src.helpers import translate

app = FastAPI()
# I am using motor client for supporting async operations via mongo
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.MONGODB_NAME]
words_collection = db.get_collection("words")


@app.get("/word/{word}")
async def get_word_details(word: str, source: str, to: str):
    # check word in database
    word_details = await words_collection.find_one({"word": word})
    if not word_details:
        # if not exists get translation from api
        word_details = await translate(word, to, source)
        await words_collection.insert_one(word_details)
    elif not to in word_details["langs"].keys():
        # if exists but language not exists get the translation for this language and update word
        new_translation = await translate(word, to, source)
        word_details["langs"][to] = new_translation["langs"][to]
        await words_collection.update_one(
            {"_id": word_details["_id"]},
            {"$set": {f"langs.{to}": new_translation["langs"][to]}},
        )
    del word_details["_id"]
    return word_details


@app.get("/words")
async def list_words(
    page: int = 1,
    limit: int = 10,
    word_filter: str = None,
    definitions: bool = False,
    examples: bool = False,
    synonyms: bool = False,
):
    query = {}
    # query for partial match
    if word_filter:
        query["word"] = {"$regex": word_filter, "$options": "i"}

    total_count = await words_collection.count_documents(query)
    words = []
    # get words in async way and check/uncheck which data would be shown
    async for word in words_collection.find(query).skip((page - 1) * limit).limit(
        limit
    ):
        word_details = {"word": word["word"], "sl": word["sl"]}
        if definitions:
            word_details["definitions"] = word["definitions"]
        if synonyms:
            word_details["synonyms"] = word["synonyms"]
        if examples:
            word_details["examples"] = word["examples"]

        words.append(word_details)

    return {
        "total_count": total_count,
        "words": words,
    }


@app.delete("/word/{word}")
async def delete_word(word: str):
    # delete word by word name
    result = await words_collection.delete_one({"word": word})
    if result.deleted_count == 1:
        return {"message": f"Word '{word}' deleted successfully."}
    else:
        return {"message": f"Word '{word}' not found."}, 404
