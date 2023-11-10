
'''
def substitution_cipher_encryption(input_text, char_mapping):
    encrypted_text = ''.join([char_mapping.get(char, char) for char in input_text])
    return encrypted_text

def create_char_mapping(char_mapping_input):
    char_mapping_list = [pair.split(':') for pair in char_mapping_input.split(',')]
    return {pair[0]: pair[1] for pair in char_mapping_list}


while True:
    try:
        default = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F']
        char_mapping_input =  [0, 2, 2, 3, 4, 5, 6, 7, 8, 9, 'B', 'B', 'C', 'D', 'E', 'F']
        pairs = []

        for d1, d2 in zip(default, char_mapping_input):
            pairs.append(f"{d1}:{d2}")
        
        map = (", ".join(pairs))
        print(map)
        char_mapping = create_char_mapping(map)
        break
    except (ValueError, IndexError):
        print("Invalid format. Please use the format 'a:k,h:x,d:g,y:e' keep going.")

text_to_encrypt = input("Enter the text to encrypt: ")

encrypted_text = substitution_cipher_encryption(text_to_encrypt, char_mapping)
print("Encrypted text:", encrypted_text)
'''
