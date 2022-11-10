from subprocess import Popen, PIPE


#use subrocess and xsel to get the clipboard contents
def get_primary_clipboard():
    p = Popen(['xsel', '-o'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    #convert output to a string
    output = output.decode('utf-8')
    return output

#use subrocess and xclip to fill the clipboard contents
def fill_clipboard(new_clipboard):
    new_clipboard = new_clipboard+"mine"
    p = Popen(['xclip', '-selection', 'clipboard'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(input=new_clipboard.encode('utf-8'))
    return output




fill_clipboard(get_primary_clipboard())