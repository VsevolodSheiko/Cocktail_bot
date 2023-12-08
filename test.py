from easygoogletranslate import EasyGoogleTranslate

translator = EasyGoogleTranslate(
    source_language='en',
    target_language='uk',
    timeout=10
)
result = translator.translate("""
• Brandy : 2 oz 
• Egg : 1 whole 
• Sugar : 1 tsp superfine 
• Light cream : 1/2 oz 
• Nutmeg : 1/8 tsp grated """)

print(result) 
# Output: Dies ist ein Beispiel.