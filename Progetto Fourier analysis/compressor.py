from PIL import Image, ImageTk
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from scipy.fftpack import fft, dct, idct


def plot_image(img):
    plt.figure(figsize=(10, 10))
    plt.imshow(img, cmap = 'Greys_r')
    plt.show()

def plot_images_compare(img1, img2, parameters):
    fig = plt.figure()
    ax = fig.add_subplot(1, 2, 1)
    imgplot = plt.imshow(img1, cmap = 'Greys_r')
    ax.set_title('Before', fontsize = 35)

    ax = fig.add_subplot(1, 2, 2)
    imgplot = plt.imshow(img2, cmap = 'Greys_r')
    ax.set_title(f'After - F: {parameters[0]}, d: {parameters[1]}', fontsize = 35)

    plt.show()

def round_values(x): 
    if x < 0:
        return 0 
    elif x > 255:
        return 255 
    else:
        return x

def compress_image(image, F, d):
    # ottenimento dimensioni immagine 
    height = image.shape[0]
    width = image.shape[1]
    # ottenimento dimensioni sulla base della dimensione scelta per i blocchi
    cut_height = F * (height // F)
    cut_width = F * (width // F)
    # allocazione matrici per dct e idct
    dct2_matrix = np.zeros((cut_height, cut_width))
    idct2_matrix = np.zeros((cut_height, cut_width))
    # ridimensionamento matrice
    image = image[:cut_height, :cut_width]
    for r in range(0, cut_height, F): 
        for c in range(0, cut_width, F):
            # calcolo dct sul blocco
            dct2_matrix[r:r+F, c:c+F] = dct(dct(image[r:r+F,c:c+F].transpose(), norm="ortho").transpose(), norm="ortho")
            # taglio delle frequenze
            for x in range(F): 
                lb = d - x
                if x > d: 
                    lb = 0
                for y in range(lb, F): 
                    dct2_matrix[x + r, y + c] = 0
    
    for r in range(0, cut_height, F): 
        for c in range(0, cut_width, F):
            # calcolo idct sul blocco
            idct2_matrix[r:r+F, c:c+F] = idct(idct(dct2_matrix[r:r+F, c:c+F].transpose(), norm="ortho").transpose(), norm="ortho")


    for r in range(cut_height):
        for c in range(cut_width):
            # arrotondamento valori
            idct2_matrix[r, c] = round_values(idct2_matrix[r, c])
    
    return np.array(idct2_matrix, dtype = np.uint8)


def main(path_image, F, d):
    img = Image.open(path_image).convert('L')
    img_c = compress_image(np.array(img), F = F, d = d)
    plot_images_compare(np.array(img), img_c, (F, d))





if __name__ == '__main__':
    main("/Users/daniel/Documents/Università/Esami & oth/Master's degree/Primo anno/Secondo semestre/Metodi del calcolo scientifico/numerical-algorithms-for-mathematical-modeling/Progetto Fourier analysis/Immagini/320x320.bmp", 20.0, 1.0)
    
