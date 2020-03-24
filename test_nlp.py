import spacy

nlp = spacy.load("en_core_web_sm")
for ent in nlp(input("Enter: ")).ents:print(ent.text, ent.label_)