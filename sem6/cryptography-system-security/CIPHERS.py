import math

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            # Shift character and wrap around alphabet
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result

def playfair_cipher(text, key):
    # 1. Create 5x5 Matrix
    key = key.upper().replace("J", "I")
    matrix = []
    seen = set()
    
    # Add key characters first
    for char in key:
        if char not in seen and char.isalpha():
            matrix.append(char)
            seen.add(char)
            
    # Add remaining alphabet
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in seen:
            matrix.append(char)
            
    # 2. Prepare Text (Digraphs)
    text = text.upper().replace("J", "I")
    clean_text = ""
    for char in text:
        if char.isalpha():
            clean_text += char
            
    digraphs = []
    i = 0
    while i < len(clean_text):
        a = clean_text[i]
        b = ''
        if i + 1 < len(clean_text):
            b = clean_text[i+1]
        
        if a == b:
            digraphs.append(a + 'X')
            i += 1
        elif b:
            digraphs.append(a + b)
            i += 2
        else:
            digraphs.append(a + 'X')
            i += 1

    # 3. Encrypt Digraphs
    cipher_text = ""
    for pair in digraphs:
        r1, c1 = 0, 0
        r2, c2 = 0, 0
        
        # Find positions
        for idx, char in enumerate(matrix):
            if char == pair[0]:
                r1, c1 = divmod(idx, 5)
            if char == pair[1]:
                r2, c2 = divmod(idx, 5)
        
        if r1 == r2: # Same Row
            cipher_text += matrix[r1 * 5 + (c1 + 1) % 5]
            cipher_text += matrix[r2 * 5 + (c2 + 1) % 5]
        elif c1 == c2: # Same Column
            cipher_text += matrix[((r1 + 1) % 5) * 5 + c1]
            cipher_text += matrix[((r2 + 1) % 5) * 5 + c2]
        else: # Rectangle
            cipher_text += matrix[r1 * 5 + c2]
            cipher_text += matrix[r2 * 5 + c1]
            
    return cipher_text

def rail_fence_cipher(text, depth):
    if depth == 1: return text
    
    # Create a grid initialized with empty strings
    rail = [['\n' for i in range(len(text))] for j in range(depth)]
    
    dir_down = False
    row, col = 0, 0
    
    for i in range(len(text)):
        if (row == 0) or (row == depth - 1):
            dir_down = not dir_down
        
        rail[row][col] = text[i]
        col += 1
        
        if dir_down:
            row += 1
        else:
            row -= 1
            
    # Read the matrix to construct cipher
    result = []
    for i in range(depth):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result.append(rail[i][j])
    return("".join(result))

def main():
    while True:
        print("\n--- CIPHER MENU ---")
        print("1. Caesar Cipher")
        print("2. Playfair Cipher")
        print("3. Rail Fence Cipher")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            text = input("Enter Plaintext: ")
            shift = int(input("Enter Shift Key (integer): "))
            print(f"Encrypted Text: {caesar_cipher(text, shift)}")
            
        elif choice == '2':
            text = input("Enter Plaintext: ")
            key = input("Enter Key: ")
            print(f"Encrypted Text: {playfair_cipher(text, key)}")
            
        elif choice == '3':
            text = input("Enter Plaintext: ")
            depth = int(input("Enter Depth (Rails): "))
            print(f"Encrypted Text: {rail_fence_cipher(text, depth)}")
            
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()