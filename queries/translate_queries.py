import asyncio
from easygoogletranslate import EasyGoogleTranslate

translator = EasyGoogleTranslate(
    source_language='en',
    target_language='uk',
    timeout=10
)

async def translate_text(text):
    await asyncio.sleep(0.2)
    return translator.translate(text)

