from PIL import Image
import numpy as np


def load_image(image_path):
    """Loads an image and converts it into a numpy array."""
    img = Image.open(image_path)
    return np.array(img), img.mode, img.size


def save_image(image_array, mode, size, output_path):
    """Saves the numpy array as an image."""
    img = Image.fromarray(image_array.astype('uint8'), mode)
    img.save(output_path)


def encrypt_image(image_array, key1, key2):
    """Encrypts the image using a combination of XOR, addition, and pixel shuffling."""
    key1 = key1 % 256
    key2 = key2 % 256

    encrypted_image = image_array ^ key1
    encrypted_image = (encrypted_image + key2) % 256

    np.random.seed(key1)
    flat_image = encrypted_image.flatten()
    shuffled_indices = np.random.permutation(len(flat_image))
    encrypted_image = flat_image[shuffled_indices].reshape(image_array.shape)

    return encrypted_image


def decrypt_image(encrypted_image_array, key1, key2):
    """Decrypts the image using the reverse of the encryption process."""
    key1 = key1 % 256
    key2 = key2 % 256

    np.random.seed(key1)
    flat_image = encrypted_image_array.flatten()
    shuffled_indices = np.random.permutation(len(flat_image))
    original_indices = np.argsort(shuffled_indices)
    unshuffled_image = flat_image[original_indices].reshape(encrypted_image_array.shape)

    unshuffled_image = (unshuffled_image - key2) % 256
    decrypted_image = unshuffled_image ^ key1

    return decrypted_image


# Terminal Inputs
input_image_path = input("Enter the path to the input image: ")
encrypted_image_path = input("Enter the path to save the encrypted image: ")
decrypted_image_path = input("Enter the path to save the decrypted image: ")

# Encryption keys
encryption_key1 = int(input("Enter the first encryption key (integer): "))
encryption_key2 = int(input("Enter the second encryption key (integer): "))

# Load the image
image_array, mode, size = load_image(input_image_path)

# Encrypt the image
encrypted_image = encrypt_image(image_array, encryption_key1, encryption_key2)
save_image(encrypted_image, mode, size, encrypted_image_path)
print("Image encrypted and saved!")

# Decrypt the image
decrypted_image = decrypt_image(encrypted_image, encryption_key1, encryption_key2)
save_image(decrypted_image, mode, size, decrypted_image_path)
print("Image decrypted and saved!")
