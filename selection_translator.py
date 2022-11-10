from subprocess import Popen, PIPE
from googletrans import Translator

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
    p = Popen(['notify-send', text], stdin=PIPE, stdout=PIPE, stderr=PIPE)

#get translation from google translate
def get_translation(selected_text, lang_code):
    translator = Translator()
    translation = translator.translate(selected_text, dest=lang_code)
    print(translation.text)
    return translation.text

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
    notify(translation)

main()