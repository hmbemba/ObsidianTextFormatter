import keyboard
import time
import pyperclip
import re
from nltk import tokenize

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])"

hotkey = "ctrl + shift + u"
# Remember that the order in which the hotkey is set up is the order you
# need to press the keys.

def formatSentences(inputArray: list[str]):
  formattedText = ''
  for sentence in inputArray:
    if sentence: # If the sentence is not an empty string like ''
      sentence = sentence.strip()
      sentence = sentence.replace('\n','')
      sentence = sentence.replace('\r',' ')
      sentence = re.sub(' +', ' ', sentence)
      #if sentence[0] == '-':
      if sentence.startswith("-"):
        formattedText+= sentence   +'\n'+ '\n'
      else:
        formattedText+= '- '+sentence   +'\n'+ '\n'
  
  return formattedText

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    if "..." in text: text = text.replace("...","<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

while True:
  if keyboard.is_pressed(hotkey):
    data = tokenize.sent_tokenize(pyperclip.paste())#split_into_sentences(pyperclip.paste()) 
    #print(data)
    formattedData = formatSentences(data)
    #print(formattedData)
    pyperclip.copy(formattedData)
    time.sleep(0.05)
  time.sleep(0.01)
  



