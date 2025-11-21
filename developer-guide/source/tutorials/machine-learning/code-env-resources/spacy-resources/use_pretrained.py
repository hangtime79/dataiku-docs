import spacy

nlp = spacy.load('en_core_web_sm')
text = nlp(""""
A call for American independence from Britain,
the Virginia Declaration of Rights was drafted
by George Mason in May 1776""")

for word in text.ents:
    print(f"{word.text} --> {word.label_}")