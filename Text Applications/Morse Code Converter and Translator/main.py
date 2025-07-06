from art import logo
print(logo)

MORSE_DICT = {
    # Letters
    'a': '.-',
    'b': '-...',
    'c': '-.-.',
    'd': '-..',
    'e': '.',
    'f': '..-.',
    'g': '--.',
    'h': '....',
    'i': '..',
    'j': '.---',
    'k': '-.-',
    'l': '.-..',
    'm': '--',
    'n': '-.',
    'o': '---',
    'p': '.--.',
    'q': '--.-',
    'r': '.-.',
    's': '...',
    't': '-',
    'u': '..-',
    'v': '...-',
    'w': '.--',
    'x': '-..-',
    'y': '-.--',
    'z': '--..',

    # Digits
    '0': '-----',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',

    # Accents & Simbols
    'á': '.-',
    'à': '.-',
    'â': '.-',
    'ã': '.-',
    'ä': '.-',
    'é': '.',
    'è': '.',
    'ê': '.',
    'ë': '.',
    'í': '..',
    'ì': '..',
    'î': '..',
    'ï': '..',
    'ó': '---',
    'ò': '---',
    'ô': '---',
    'õ': '---',
    'ö': '---',
    'ú': '..-',
    'ù': '..-',
    'û': '..-',
    'ü': '..-',
    'ç': '-.-.',
    'ñ': '-.',

    '.': '.-.-.-',
    ',': '--..--',
    ':': '---...',
    '?': '..--..',
    "'": '.----.',
    '-': '-....-',
    '/': '-..-.',
    '(': '-.--.',
    ')': '-.--.-',
    '"': '.-..-.',
    '=': '-...-',
    '+': '.-.-.',
    '@': '.--.-.',

    # Substituted Symbols (no official Morse Code)
    '%': '.--. . .-. -. -. - .',  # "percent"
    '$': '-.. -..- .-.. .-.. .-.',  # "dollar"
    '&': '.- -. -..',  # "and"
    '#': '-. .- -..- -..- .-.',  # "number"
    '*': '',  # omitted
}
def is_ascii_morse_char(c):
    return ord(c) < 128 and (c.isalpha() or c.isdigit() or c in ['.', ',', ':', '?', "'", '-', '/', '(', ')', '"', '=', '+', '@'])

REVERSE_MORSE_DICT = {
    morse: char for char, morse in MORSE_DICT.items()
    if morse and is_ascii_morse_char(char)
}

def morse_code(original_text, function):
    if function == "encode":
        morse_text = ""
        for char in original_text:
            if char in MORSE_DICT:
                morse_text += MORSE_DICT[char] + ' '
            elif char == ' ':
                morse_text += ' / '
            else:
                morse_text += '[?] ' # Unknown Char
        print(f"Here is the Morse Encoded result: {morse_text}")


    elif function == "decode":
        words = original_text.strip().split(' / ')
        decoded_text = ""

        for word in words:
            letters = word.split()
            for symbol in letters:
                if symbol in REVERSE_MORSE_DICT:
                    decoded_text += REVERSE_MORSE_DICT[symbol]
                else:
                    decoded_text += '?'  # Unknown Symbol
            decoded_text += ' '

        print(f"Decoded Morse to Text: {decoded_text.strip()}")
    print("\n")

continue_program = True
while continue_program:
    encode_or_decode = input("Type 'encode' to convert Text into Morse or 'decode' to convert Morse into Text:\n").lower()
    if encode_or_decode == "encode" or encode_or_decode == "decode":
        text = input(f"Type the message you want to {encode_or_decode}:\n").lower()
        morse_code(original_text=text, function=encode_or_decode)

    else:
        print("Sorry, could not understand.\n")

    user_choice = input("\nType \"Yes\" if you want to use the Morse Encoder again, or \"No\" if you want to stop:\n").lower()
    if user_choice == "no":
        continue_program = False
        print("Finishing the Text to Morse Code Program. Goodbye!")
    else:
        print("\n"*5)