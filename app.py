import streamlit as st
import pandas as pd
import random
import time
import base64
import os
from PIL import Image

# 1. Configuración de la página centrada (debe ser el primer comando de Streamlit)
st.set_page_config(
    page_title="Wild Cards RPG",
    page_icon="🃏",
    layout="centered"
)

# Asegurarse de que openpyxl está instalado
try:
    import openpyxl
except ImportError:
    st.error("La librería openpyxl no está instalada. Por favor instálala usando 'pip install openpyxl'.")

# CSS para centrar contenido y ajustar estilos (sin bullets)
st.markdown(
    """
    <style>
    body {
        background-color: #1a1a1a;
        color: #e0e0e0;
        text-align: center;
    }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #ff5555 !important;
    }
    .stButton>button {
        background-color: #333333;
        color: #e0e0e0;
        border: 2px solid #ff5555;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #444444;
        color: #ffaaaa;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Wild Cards RPG")
st.write("Una Carta marca tu destino...")

# 2. Lectura del archivo Excel (usando ruta relativa)
excel_path = "cartas_list.xlsx"
try:
    df_cartas = pd.read_excel(excel_path)
except Exception as e:
    st.error(f"No se pudo leer el archivo de Excel: {e}")
else:
    df_cartas.columns = [col.strip() for col in df_cartas.columns]

    # 3. Textos narrativos generales y de muerte
    narrative_texts = [
        "Dicen que el Virus no elige… pero miente quien lo dice. Algunos despiertan con fuego en las venas, otros con sombras en los huesos. Y unos pocos… simplemente no despiertan.",
        "A esta hora, solo los necios y los poderosos caminan sin miedo. Los Jokers se esconden entre las sombras de los callejones, y los Aces patrullan desde las alturas.",
        "Un hombre encapuchado te da una baraja. \"Escoge\", dice con una sonrisa sin labios. No importa qué carta saques; ya estás perdido. En esta ciudad, el destino se reparte con cada carta."
    ]

    death_texts = [
        "El virus te atraviesa como un rayo helado. En cuestión de segundos, tus venas se ennegrecen, y cada célula de tu cuerpo se descompone. No hay gritos, solo un instante de agonía.",
        "Incapaz de respirar. Tus órganos fallan en una sinfonía de agonía interna, cada latido de tu corazón un martillazo final. El mundo se oscurece, y te sumerges en la nada.",
        "Sientes el fuego crecer dentro de ti. Intentas gritar, pero solo sale aire ardiente de tus labios. En segundos, tu piel se agrieta como tierra seca y te desmoronas en ceniza.",
        "Tu reflejo en el charco de sangre frente a ti es lo último que ves. Tu cuerpo se colapsa como un edificio demolido, piel destrozada, huesos que ceden bajo su propio peso. La oscuridad te envuelve.",
        "Un escalofrío recorre tu espalda. De pronto, el mundo parece distante, borroso. Intentas moverte, pero ya no puedes. En un susurro, el virus toma su premio. El suelo se acerca rápidamente.",
        "Cada célula de tu cuerpo se vuelve frágil como vidrio. Un movimiento más y colapsas en mil pedazos, un artefacto roto de una historia sin final. Solo queda el sonido del cristal al romperse."
    ]

    # 4. Diccionario de modificaciones (Quantum, Dones, Mega-Atributos)
    modifications = {
        'Ace': {'Quantum': 7, 'Dones': 2, 'Mega-Atributos': 1},
        'Joker': {'Quantum': 7, 'Dones': 2, 'Mega-Atributos': 1},
        '2': {'Quantum': 4, 'Dones': 2, 'Mega-Atributos': 1},
        '3': {'Quantum': 3, 'Dones': 2, 'Mega-Atributos': 1},
        '4': {'Quantum': 0, 'Dones': 0, 'Mega-Atributos': 0},
        'J': {'Quantum': 0, 'Dones': 0, 'Mega-Atributos': 0},
        'K': {'Quantum': 4, 'Dones': 2, 'Mega-Atributos': 1},
        'Q': {'Quantum': 3, 'Dones': 2, 'Mega-Atributos': 1},
    }

    # 5. Diccionario de mapeo para las pintas (normalización)
    suit_mapping = {
        'corazones': 'Corazones',
        'diamantes': 'Diamantes',
        'espadas': 'Espadas',
        'treboles': 'Tréboles'
    }

    # 6. Diccionario de bonus por valor de carta y pinta
    bonus_table = {
        "JOKER": {
            "Espadas": "+3 en habilidades de combate, resistencia y estrategia.",
            "Corazones": "+3 en persuasión, empatía y regeneración.",
            "Diamantes": "+3 en negociación, suerte y tecnología.",
            "Tréboles": "+3 en sigilo, conocimiento oculto y supervivencia."
        },
        "A": {
            "Espadas": "+3 en habilidades de combate, resistencia y estrategia.",
            "Corazones": "+3 en persuasión, empatía y regeneración.",
            "Diamantes": "+3 en negociación, suerte y tecnología.",
            "Tréboles": "+3 en sigilo, conocimiento oculto y supervivencia."
        },
        "K": {
            "Espadas": "+2 en combate, liderazgo y tácticas.",
            "Corazones": "+2 en influencia social y manipulación.",
            "Diamantes": "+2 en riqueza, estatus y estrategia.",
            "Tréboles": "+2 en infiltración y adaptación."
        },
        "2": {
            "Espadas": "+2 en combate, fortaleza y reflejos.",
            "Corazones": "+2 en persuasión y carisma.",
            "Diamantes": "+2 en comercio y planeación.",
            "Tréboles": "+2 en instinto de supervivencia."
        },
        "Q": {
            "Espadas": "+1 en planificación y ataque táctico.",
            "Corazones": "+1 en manipulación y liderazgo social.",
            "Diamantes": "+1 en influencia y astucia.",
            "Tréboles": "+1 en ocultismo y resistencia."
        },
        "3": {
            "Espadas": "+1 en combate y aguante físico.",
            "Corazones": "+1 en seducción e intuición emocional.",
            "Diamantes": "+1 en negocios y diplomacia.",
            "Tréboles": "+1 en discreción y rastreo."
        },
        "J": {
            "Espadas": "+0 (habilidades básicas sin mejora)",
            "Corazones": "+0 (habilidades básicas sin mejora)",
            "Diamantes": "+0 (habilidades básicas sin mejora)",
            "Tréboles": "+0 (habilidades básicas sin mejora)"
        },
        "4": {
            "Espadas": "Esta carta puede comprar un solo punto de poder en un poder con los puntos adicionales de creación del personaje.",
            "Corazones": "Esta carta puede comprar un solo punto de poder en un poder con los puntos adicionales de creación del personaje.",
            "Diamantes": "Esta carta puede comprar un solo punto de poder en un poder con los puntos adicionales de creación del personaje.",
            "Tréboles": "Esta carta puede comprar un solo punto de poder en un poder con los puntos adicionales de creación del personaje."
        }
    }

    # 7. Diccionario de características base de cada pinta (parte narrativa)
    suit_characteristics = {
        "Corazones": (
            "Representan la pasión, el heroísmo y la fuerza de voluntad. "
            "Los personajes con cartas de esta pinta tienen facilidad para el liderazgo, relaciones interpersonales "
            "y una mayor resistencia al miedo."
        ),
        "Diamantes": (
            "Simbolizan el ingenio, la inteligencia y la ambición. "
            "Son innovadores, estratégicos y carismáticos, expertos en negociación y conocimientos avanzados."
        ),
        "Espadas": (
            "Simbolizan la determinación, la disciplina y el sacrificio. "
            "Son guerreros forjados en la lucha, con una voluntad férrea que les permite superar cualquier obstáculo."
        ),
        "Tréboles": (
            "Representan la suerte, la adaptabilidad y la capacidad de sobrevivir en condiciones adversas. "
            "Dotados de intuición y resiliencia, se recuperan rápidamente de la adversidad y abrazan lo caótico."
        )
    }

    # 8. Función para normalizar el valor de la carta
    def normalize_card_value(value: str) -> str:
        val_upper = value.upper()
        if val_upper in ["AS"]:
            return "A"
        elif val_upper == "REY":
            return "K"
        elif val_upper == "REINA":
            return "Q"
        elif val_upper == "JOTA":
            return "J"
        elif val_upper == "JOKER":
            return "JOKER"
        return val_upper

    # 9. Función para obtener el video como HTML embebido (usando Base64)
    def get_video_html(file_path, width=300):
        try:
            with open(file_path, "rb") as video_file:
                video_bytes = video_file.read()
            encoded_video = base64.b64encode(video_bytes).decode()
            video_html = f'''
            <div style="text-align: center;">
                <video width="{width}" autoplay muted playsinline>
                    <source src="data:video/mp4;base64,{encoded_video}" type="video/mp4">
                    Tu navegador no soporta el video.
                </video>
            </div>
            '''
            return video_html
        except Exception as e:
            return f"<p>Error cargando video: {e}</p>"

    # 10. Lógica principal de la aplicación
    if st.button("Extraer Carta"):
        # Mostrar el video para generar expectación durante 5 segundos
        video_path = r"mazo.mp4"  # Ruta relativa (el archivo debe estar en la raíz del repositorio)
        video_placeholder = st.empty()
        video_html = get_video_html(video_path, width=300)
        video_placeholder.markdown(video_html, unsafe_allow_html=True)
        time.sleep(5)
        video_placeholder.empty()  # Eliminar el video antes de mostrar la carta
        
        # Extraer una carta aleatoria
        carta = df_cartas.sample(n=1).iloc[0]
        # Suponiendo que en el Excel se guarda la ruta completa
        ruta_relativa = carta['Ruta Completa']
        
        # Valor de la carta
        numero_original = str(carta['Carta']).strip()
        valor_carta = normalize_card_value(numero_original)
        
        # Pinta: normalizar usando suit_mapping
        pinta_original = str(carta['Pinta']).strip()
        pinta_lower = pinta_original.lower()
        pinta = suit_mapping.get(pinta_lower, "Desconocida")
        
        # Mostrar imagen de la carta centrada
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        try:
            imagen = Image.open(os.path.join("cartas_naipes", ruta_relativa))
            st.image(imagen, caption=f"Carta: {numero_original} de {pinta_original}", width=300, use_container_width=True)
        except Exception as e:
            st.error(f"No se pudo cargar la imagen: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Verificar si la carta indica muerte (valores numéricos entre 5 y 10)
        is_death_card = False
        if numero_original.isdigit():
            num_int = int(numero_original)
            if 5 <= num_int <= 10:
                is_death_card = True
        
        if is_death_card:
            st.error("¡El personaje ha muerto por el virus!")
            death_message = random.choice(death_texts)
            st.markdown(f"<p style='font-size: 1.5em; text-align: center;'>{death_message}</p>", unsafe_allow_html=True)
        else:
            # Narrativa (tamaño del texto reducido a 1.3em)
            narrativa = random.choice(narrative_texts)
            st.markdown(f"<p style='font-size: 1.3em; text-align: center;'>{narrativa}</p>", unsafe_allow_html=True)
            
            # Mostrar la descripción narrativa por pinta (sin bonus) con título de la carta
            desc_suit = suit_characteristics.get(pinta, "Descripción no disponible.")
            st.markdown(f"<h4 style='text-align: center;'>{numero_original} de {pinta_original}</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 1.2em; text-align: center;'>{desc_suit}</p>", unsafe_allow_html=True)
            
            # Mostrar modificaciones de creación de personaje (centrado, sin bullets)
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.markdown("<h4>Creación de personaje:</h4>", unsafe_allow_html=True)
            if valor_carta == "A":
                mod_key = "Ace"
            elif valor_carta == "JOKER":
                mod_key = "Joker"
            else:
                mod_key = valor_carta
            mod = modifications.get(mod_key, None)
            if mod:
                st.markdown(f"<p style='font-size: 1.2em;'>Quantum Máx: {mod['Quantum']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 1.2em;'>Dones: {mod['Dones']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 1.2em;'>Mega-Atributos: {mod['Mega-Atributos']}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size: 1.2em;'>No se han definido modificaciones para este valor de carta.</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Mostrar características base del personaje (centrado)
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.markdown("<h4>Características Base del Personaje:</h4>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 1.2em;'>Atributos Base: Mente: 6, Cuerpo: 4, Carácter: 3</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 1.2em;'>Habilidades Base: 9 puntos + 6 en grupo favorito</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 1.2em;'>Puntos Extra: 15</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Mostrar bonus por valor de carta y pinta (centrado) con explicación incluida
            bonus_text = bonus_table.get(valor_carta, {}).get(pinta, "Sin bonus definido")
            bonus_explicacion = f"{bonus_text} Este bonus se aplicará a una de las tres habilidades disponibles, a elección del jugador."
            st.markdown(f"<p style='font-size: 1.2em; text-align: center;'>Bonus por valor de carta y pinta: {bonus_explicacion}</p>", unsafe_allow_html=True)
