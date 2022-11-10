from subprocess import Popen, PIPE
from googletrans import Translator
from PyDictionary import PyDictionary
import os

#to use this, make a custom keyboard shortcut for each language:
#bash -c "python3 /home/lunkwill/projects/small_scripts/selection_translator.py -d"

#get arguments from command line
def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='Translate selected text')
    parser.add_argument('-t', '--turkish', action='store_true', help='translate selected text to turkish')
    parser.add_argument('-e', '--english', action='store_true', help='translate selected text to english')
    parser.add_argument('-d', '--deutsch', action='store_true', help='translate selected text to german')
    parser.add_argument('-s', '--espanol', action='store_true', help='translate selected text to spanish')
    parser.add_argument('-r', '--definition', action='store_true', help='definition of selected text')
    return parser.parse_args()

#use subrocess and xsel to get the clipboard contents
def get_primary_clipboard():
    p = Popen(['xsel', '-o'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    #convert output to a string
    output = output.decode('utf-8')
    return output

#create an notify message
def notify(text):
    #text = "testint \n hfdsufsudidsj \n fsdfahdkjfhdkasjfhkjdashfkj                          \n dfdgddgd"
    print('text')
    
    msg = "notify-send ' ' '"+text+"'"
    os.system(msg)
    #p = Popen(['notify-send', text], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    #notify-send ' ' 'd: title,up/down: zoom,w: win_to_img,</>: rotate,*: orig,Enter/0: blah blah blah'

#get translation from google translate
def get_translation(selected_text, lang_code):
    translator = Translator()
    translation = translator.translate(selected_text, dest=lang_code)
    print(translation.text)
    return translation.text

def get_definition(selected_text):
    dictionary=PyDictionary()
    definition = dictionary.meaning(selected_text)
    first_key = list(definition.keys())[0]
    definition = definition[first_key]
    definition = ', '.join(definition)
    print(str(definition))
    return definition


def main():
    selected_text = get_primary_clipboard()
    args = get_args()
    if args.turkish:
        translation = get_translation(selected_text, 'tr')
    if args.english:
        translation = get_translation(selected_text, 'en')  
    if args.deutsch:
        translation = get_translation(selected_text, 'de')
    if args.espanol:
        translation = get_translation(selected_text, 'es')   
    if args.definition:
        translation = get_definition(selected_text)
     
    notify(translation)

main()