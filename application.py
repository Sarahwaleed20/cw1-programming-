def message_to_binary(message):
    "Convert a string message to a binary string."
    return ''.join(format(ord(char), '08b') for char in message)

def hide_message_in_image(image_path, message, output_path):
    "Hide a message in the least significant bits of the image pixels."
    message += '\0' 
    binary_message = message_to_binary(message)

    with open(image_path, 'rb') as img:
        img_data = bytearray(img.read())

    for i in range(len(binary_message)):
        img_data[54 + i] = (img_data[54 + i] & 0xFE) | int(binary_message[i])

    with open(output_path, 'wb') as img_out:
        img_out.write(img_data)
def retrieve_message_from_image(image_path):
    "Retrieve a hidden message from the least significant bits of the image pixels."
    with open(image_path, 'rb') as img:
        img_data = bytearray(img.read())

    binary_message = ''.join(str(img_data[i] & 1) for i in range(54, len(img_data)))
    message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))
    
    return message.split('\0')[0]  

if __name__ == "__main__":
    action = input("Do you want to (1) hide a message or (2) retrieve a message? ")
    img_path = input("Enter the path of the image: ")
    
    if action == '1':
        secret_message = input("Enter the message to hide: ")
        output_img_path = input("Enter the output image path: ")
        hide_message_in_image(img_path, secret_message, output_img_path)
        print("Message hidden successfully.")
    elif action == '2':
        retrieved_message = retrieve_message_from_image(img_path)
        print("Retrieved message:", retrieved_message)
    else:
        print("Invalid option.")
