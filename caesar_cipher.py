from string import ascii_lowercase

alphabet = ascii_lowercase


class CaesarCipher:

    @staticmethod
    def encrypt(data: str, key: int):
        output = ''

        for letter in data.lower():
            if letter in alphabet:
                index = alphabet.find(letter)
                output += alphabet[(index + key) % 26]
            else:
                output += letter

        return output

    @staticmethod
    def decrypt(data: str, key: int):
        return CaesarCipher.encrypt(data, -key)
