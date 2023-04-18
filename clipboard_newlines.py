from subprocess import Popen, PIPE


#use subrocess and xsel to get the clipboard contents
def get_primary_clipboard():
    p = Popen(['xsel', '-o'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    #convert output to a string
    output = output.decode('utf-8')
    return output

#use subrocess and xclip to fill the clipboard contents
def fill_clipboard(text):
    p = Popen(['xclip', '-selection', 'clipboard'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(input=text.encode('utf-8'))
    return output

# example = "if most of a particles entanglement is with particles beyond the horizon(https://www.sciencedirect.com/science/article/pii/S037026931200994X), then the space in which the decider lives can be in the newest entanglements. These newest entanglements are the particles which the decider has control of. This is in the same way that we mainly have things in our concious mind that are related to new information. Things we learned long ago and became a part of us long ago would not be as relevant. If a particle that the decider's particles are doesn't physically interact(or get entangled) with another particle for awhile then it loses control over it."



#divide example into lines of about 40 characters each
def divide_into_lines(example):
    example = example.split()
    text_with_lines = []
    this_line = ""
    for word in example:
        previous_word = word
        if len(this_line) + len(word) > 80:
            text_with_lines.append(this_line)
            this_line = ''        
        if len(this_line) <= 80:
            this_line = this_line + previous_word + ' '
    text_with_lines.append(this_line)
    #create a string from text_with_line seperates by new lines
    text_with_lines = '\n'.join(text_with_lines)
    return text_with_lines



fill_clipboard(divide_into_lines(get_primary_clipboard()))