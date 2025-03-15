import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

# pour appliquer le filtre Sepia
def apply_sepia(image, intensity):
    np_image = np.array(image)
    tr = [0.393, 0.769, 0.189]
    tg = [0.349, 0.686, 0.168]
    tb = [0.272, 0.534, 0.131]
    sepia_filter = np.array([tr, tg, tb])
    np_image = np.dot(np_image[...,:3], sepia_filter.T).clip(0, 255).astype(np.uint8)
    return Image.fromarray(np_image)

# pour appliquer l'effet Pixelated
def apply_pixelated(image, intensity):
    size = max(1, int(image.width // intensity))
    image = image.resize((size, size), Image.NEAREST)
    return image.resize((image.width, image.height), Image.NEAREST)

#  appliquer un filtre de flou
def apply_blurred(image, intensity):
    return image.filter(ImageFilter.GaussianBlur(radius=intensity))

# convertir l'image en niveaux de gris
def apply_gray(image):
    return image.convert("L")

#  appliquer un contraste
def apply_contrasted(image, intensity):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(intensity)

# appliquer une rotation
def apply_rotation(image, angle):
     return image.rotate(angle, resample=Image.BICUBIC, expand=True)

#  appliquer les contours
def apply_contours(image, intensity):
    return image.filter(ImageFilter.FIND_EDGES).point(lambda p: p * intensity)

#  appliquer un filtre de couleur
def apply_color_filter(image, color):
    np_image = np.array(image)
    if color == "Rouge":
        np_image[:, :, 1:] = 0  
    elif color == "Vert":
        np_image[:, :, [0, 2]] = 0  
    elif color == "Bleu":
        np_image[:, :, :2] = 0  
    return Image.fromarray(np_image)

#  ajuster la luminosité
def adjust_brightness(image, brightness_factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(brightness_factor)

# calculer la luminosité moyenne de l'image
def calculate_brightness(image):
    grayscale_image = image.convert("L")
    np_image = np.array(grayscale_image)
    return np_image.mean() / 255  # Valeur entre 0 et 1

# Chargement de l'image
st.title("Modifications d'Image avec Streamlit")

uploaded_file = st.file_uploader("Choisir une image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Calculer la luminosité de l'image
    brightness_value = calculate_brightness(image)
    st.write(f"Luminosité de l'image : {brightness_value * 100:.2f}%")
    
    # la luminosité pour ajuster la taille
    width = int(image.width * brightness_value)
    height = int(image.height * brightness_value)

    # les dimensions suggérées
    st.write(f"Dimensions ajustées : Largeur = {width}, Hauteur = {height}")
    
    # Paramètres pour la largeur et la hauteur
    width = st.number_input("Nouvelle largeur", min_value=1, value=width)
    height = st.number_input("Nouvelle hauteur", min_value=1, value=height)

    #  les action de modification
    action = st.radio("les parametre des modification", 
                      ("Redimensionner", "Appliquer un flou", "Sepia", "Pixelated", 
                       "Grayscale", "Contrasted", "Rotation", "Blurred", "Contours", "Filtre en couleur"))
    
    # l'intensité avec des sliders pour chaque effet
    if action == "Redimensionner":
        intensity = 1
    elif action == "Appliquer un flou":
        intensity = st.slider("Intensité du flou", 0, 10, 5)
    elif action == "Sepia":
        intensity = st.slider("Intensité du Sepia", 0, 10, 5)
    elif action == "Pixelated":
        intensity = st.slider("Intensité du Pixelated", 1, 20, 10)
    elif action == "Contrasted":
        intensity = st.slider("Intensité du contraste", 0.1, 3.0, 1.5)
    elif action == "Blurred":
        intensity = st.slider("Intensité du flou", 0, 10, 5)
    elif action == "Contours":
        intensity = st.slider("Intensité des contours", 0.1, 2.0, 1.0)
    else:
        intensity = 1  # Par défaut

    # les modification selon l'action choisie avec l'intensité ajustée
    if action == "Redimensionner":
        image = image.resize((width, height))
    
    elif action == "Appliquer un flou":
        image = apply_blurred(image, intensity)
    
    elif action == "Sepia":
        image = apply_sepia(image, intensity)
    
    elif action == "Pixelated":
        image = apply_pixelated(image, intensity)
    
    elif action == "Grayscale":
        image = apply_gray(image)
    
    elif action == "Contrasted":
        image = apply_contrasted(image, intensity)
    
    elif action == "Rotation":
          angle = st.slider("Angle de rotation (degrés)", -360, 360, 90)  
          image = apply_rotation(image, angle) 
    
    elif action == "Blurred":
        image = image.filter(ImageFilter.GaussianBlur(radius=intensity))
    
    elif action == "Contours":
        image = apply_contours(image, intensity)
    
    elif action == "Filtre en couleur":
        color = st.selectbox("Choisir la couleur du filtre", ["Rouge", "Vert", "Bleu","violet"])
        image = apply_color_filter(image, color)
    
    #  l'image modifiée
    st.image(image, caption="Image modifiée", use_column_width=True)




