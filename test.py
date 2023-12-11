from deep_translator import ChatGptTranslator

translator = ChatGptTranslator(source='en', target='uk', use_free_api=True)

print(translator.translate("Layer in a 2 oz shot glass or pony glass"))