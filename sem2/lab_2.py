def stroim_derevo(text):
    # подсчет частоты у символов
    frequency ={}
    for letter in text:
        frequency[letter]=frequency.get(letter, 0)+1

    #каждый узел - словарь
    nodes =[{'letters':letter, 'freq':freq, 'left':None, 'right':None}
             for letter,freq in frequency.items()]

    while len(nodes)> 1:
        nodes.sort(key=lambda x:x['freq'])
        left =nodes.pop(0)
        right =nodes.pop(0)
        #объединенный узел (тоже словарь)
        merged = {'letters':None,
            'freq':left['freq']+right['freq'],
            'left':left,
            'right': right}
        nodes.append(merged)
    return nodes[0] if nodes else None

def generate_code(root):
    if not root:
        return []
    stack = [(root, "")]
    codes = []
    while stack:
        node,prefix=stack.pop()
        if node['letters'] is not None:
            codes.append((node['letters'], prefix)) # храним (символ, код)
            continue
        if node['right']:
            stack.append((node['right'], prefix + "1"))
        if node['left']:
            stack.append((node['left'],prefix + "0"))
    return codes

def codirovanie(text,codebook):
    temp_dict = {letter: code for letter, code in codebook}
    encoded_text = ""
    for char in text:
        encoded_text += temp_dict[char]
    return encoded_text

def xor_shifrovka(text,key):
    encrypted_text = ""
    key_len = len(key)
    for i in range(len(text)):
        encrypted_text += chr(ord(text[i]) ^ord(key[i % key_len]))
    return encrypted_text

def xor_rasshifrovka(encrypted_text,key):
    return xor_shifrovka(encrypted_text, key)

def decodirovanie(encoded_text,root):
    decoded_text = ""
    current_node = root
    for bit in encoded_text:
        if bit == '0':
            current_node=current_node['left']
        else:
            current_node=current_node['right']

        if current_node['letters']:
            decoded_text +=current_node['letters']
            current_node =root
    return decoded_text

def main():
    text =input("Введите текст для кодирования: ")
    key =input("Введите ключ для xor шифрования: ")
    #кодировка хаффмана
    root =stroim_derevo(text)
    codebook =generate_code(root)
    encoded_text =codirovanie(text, codebook)
    #xor шифрование
    encrypted_text =xor_shifrovka(encoded_text, key)
    decrypted_text =xor_rasshifrovka(encrypted_text, key)
    #декодирование хаффмана
    decoded_text =decodirovanie(decrypted_text, root)
    print("Закодированный текст:",encoded_text)
    print("Зашифрованный текст:",encrypted_text)
    print("Расшифрованный текст:",decrypted_text)
    print("Декодированный текст:",decoded_text)

main()
