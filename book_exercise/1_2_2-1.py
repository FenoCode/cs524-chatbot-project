from translate import Translator

translator = Translator(to_lang="es")
translation = translator.translate("What are you trying to say here? I don't understand your engineering jargon.")
print(translation)