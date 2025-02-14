import streamlit as st
import pandas as pd
import random
from PIL import Image

# Configuración de la página y estética oscura y siniestra
st.set_page_config(
    page_title="Wild Cards RPG",
    page_icon="🃏",
    layout="wide"
)

st.markdown(
    """
    <style>
    body {
        background-color: #1a1a1a;
        color: #e0e0e0;
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

st.title("Wild Cards RPG - Extracción de Carta")
st.write("Presiona el botón para extraer una carta y generar las características del personaje.")

# Ruta al archivo Excel con las cartas
excel_path = r"C:\Users\Miliv\Desktop\Wild_Cards_RPG\cartas_list.xlsx"
df_cartas = pd.read_excel(excel_path)
df_cartas.columns = [col.strip() for col in df_cartas.columns]  # Limpiar espacios en los nombres de columnas

# Textos narrativos completos
narrative_texts = [
    "La Marca del Virus: 'Dicen que el Virus no elige… pero miente quien lo dice. Algunos despiertan con fuego en las venas, otros con sombras en los huesos. Y unos pocos… simplemente no despiertan en absoluto. La suerte no es justa, y en esta ciudad, los afortunados no siempre son los que sobreviven.'",
    "Noctámbulos en las Calles: 'A esta hora, solo los necios y los poderosos caminan sin miedo. Los Jokers se esconden entre las sombras de los callejones, y los Aces patrullan desde las alturas, jueces de un tribunal sin ley. Pero en el silencio de la madrugada, incluso ellos se preguntan quién es el verdadero monstruo.'",
    "Cartas Marcadas: 'Un hombre encapuchado te da una baraja. \"Escoge\", dice con una sonrisa sin labios. No importa qué carta saques; ya estás perdido. En esta ciudad, el destino se reparte como en un juego trucado, y las cartas siempre están marcadas con sangre.'",
    "Ecos del Pasado: 'Dicen que las ruinas de la ciudad vieja todavía murmuran los nombres de los que cayeron. Algunos escuchan susurros en los túneles, otros ven sombras que se mueven en paredes sin luz. Pero todos saben una cosa: hay lugares donde ni siquiera los Aces se atreven a entrar.'",
    "La Dama de los Ojos Rotos: 'Camina por los callejones con una venda roja, y aquellos que la miran a los ojos jamás vuelven a dormir en paz. Dicen que fue una Reina, antes de que la suerte le torciera la sonrisa. Ahora solo reparte condenas… y nadie quiere su bendición.'",
    "El Juego del Cuervo: 'Apuestas una noche en la taberna del Cuervo, y descubres que aquí las fichas son vidas y las cartas dictan destinos. Pierdes, y te conviertes en una sombra en las calles. Ganas… y te conviertes en una leyenda con fecha de caducidad.'",
    "Sombras de Medianoche: 'En la ciudad de los condenados, las sombras tienen voz y el viento sopla con el aliento de los que no descansan. Algunos creen que son ecos del pasado. Otros, que es el futuro intentando advertirnos. Nadie escucha. Nadie aprende.'",
    "Hijos del Caos: 'Nacidos en el fuego, bendecidos por la ruina. Los llaman Aces, pero no hay victoria en sus rostros. La ciudad los teme, los admira, los odia… y ellos simplemente existen. Poderosos, sí. Pero jamás libres.'",
    "El Último Deseo: 'Dicen que si encuentras a la Dama Roja antes de la medianoche y le ofreces una carta de tu baraja, te concederá un deseo. Pero los que lo intentaron nunca volvieron a ser los mismos. A veces, conseguir lo que quieres es la peor condena de todas.'",
    "Bajo la Luna Negra: 'La luna se tiñe de negro una vez al año, y esa noche… los Jokers reinan. Los Aces se esconden, los humanos huyen, y las calles se convierten en el escenario de un carnaval de monstruos. Si ves un rostro sin ojos entre la multitud, reza. O corre.'"
]

# Textos completos para la muerte
death_texts = [
    "La Lotería Perdida: 'El virus te atraviesa como un rayo helado. En cuestión de segundos, tus venas se ennegrecen, y cada célula de tu cuerpo se descompone. No hay gritos, solo un instante de comprensión antes de que el polvo de lo que fuiste se mezcle con el viento.'",
    "Sufrimiento Silencioso: 'Caes de rodillas, incapaz de respirar. Tus órganos fallan en una sinfonía de agonía interna, cada latido de tu corazón un martillazo final. El mundo se oscurece, no por la noche, sino porque tu cuerpo simplemente ha dejado de ser.'",
    "Carne y Ceniza: 'Sientes el fuego crecer dentro de ti. Intentas gritar, pero solo sale aire ardiente de tus labios. En segundos, tu piel se agrieta como tierra seca y te desmoronas en ceniza. El Wild Card no tuvo piedad contigo.'",
    "El Espejo Roto: 'Tu reflejo en el charco de sangre frente a ti es lo último que ves. Tu cuerpo se colapsa como un edificio demolido, piel destrozada, huesos que ceden bajo su propio peso. La lotería de los dioses no te favoreció.'",
    "El Susurro Final: 'Un escalofrío recorre tu espalda. De pronto, el mundo parece distante, borroso. Intentas moverte, pero ya no puedes. En un susurro, el virus toma su premio. El suelo se acerca a tu rostro y ahí termina todo.'",
    "Cuerpos de Cristal: 'Cada célula de tu cuerpo se vuelve frágil como vidrio. Un movimiento más y colapsas en mil pedazos, un artefacto roto de una historia sin final. Solo queda el sonido del viento arrastrando lo que fuiste.'"
]

# Diccionario de modificaciones según el valor de la carta
modifications = {
    'Ace': {'Quantum': 7, 'Dones': 2, 'Mega-Atributos': 1},
    'Joker': {'Quantum': 7, 'Dones': 2, 'Mega-Atributos': 1},
    '2': {'Quantum': 4, 'Dones': 2, 'Mega-Atributos': 1},
    'K': {'Quantum': 4, 'Dones': 2, 'Mega-Atributos': 1},
    '3': {'Quantum': 3, 'Dones': 2, 'Mega-Atributos': 1},
    'Q': {'Quantum': 3, 'Dones': 2, 'Mega-Atributos': 1},
    '4': {'Quantum': 0, 'Dones': 0, 'Mega-Atributos': 0},
    'J': {'Quantum': 0, 'Dones': 0, 'Mega-Atributos': 0},
}

# Diccionario de bonos según la pinta de la carta
suit_bonuses = {
    'Espadas': 'Combate y estrategia',
    'Corazones': 'Persuasión y regeneración',
    'Diamantes': 'Recursos y suerte',
    'Tréboles': 'Sigilo y conocimientos ocultos'
}

if st.button("Extraer Carta"):
    # Seleccionar una carta aleatoria
    carta = df_cartas.sample(n=1).iloc[0]
    ruta = carta['Ruta Completa']
    numero = str(carta['Carta']).strip()
    pinta = str(carta['Pinta']).strip()
    
    try:
        imagen = Image.open(ruta)
        # Especificamos un ancho fijo para reducir el tamaño de la imagen
        st.image(imagen, caption=f"Carta: {numero} de {pinta}", width=300, use_container_width=False)
    except Exception as e:
        st.error(f"No se pudo cargar la imagen: {e}")
    
    # Determinar si la carta indica muerte (si es dígito y entre 5 y 10)
    is_death_card = False
    if numero.isdigit():
        if 5 <= int(numero) <= 10:
            is_death_card = True
    
    if is_death_card:
        st.error("¡El personaje ha muerto por el virus!")
        death_message = random.choice(death_texts)
        st.markdown(f"<p style='font-size: 1.5em;'>{death_message}</p>", unsafe_allow_html=True)
    else:
        narrativa = random.choice(narrative_texts)
        st.markdown(f"<p style='font-size: 1.5em;'>{narrativa}</p>", unsafe_allow_html=True)
        
        # Determinar las modificaciones según el valor de la carta:
        if numero in modifications:
            mod = modifications[numero]
        elif numero.upper() in ['AS', 'A']:
            mod = modifications['Ace']
        elif numero.lower() == 'jota':
            mod = modifications['J']
        elif numero.lower() == 'joker':
            mod = modifications['Joker']
        elif numero.lower() == 'rey':
            mod = modifications['K']
        elif numero.lower() == 'reina':
            mod = modifications['Q']
        else:
            mod = None
        
        st.markdown("#### Modificaciones para la Creación del Personaje:")
        if mod is not None:
            st.write(f"- **Quantum Máx:** {mod['Quantum']}")
            st.write(f"- **Dones:** {mod['Dones']}")
            st.write(f"- **Mega-Atributos:** {mod['Mega-Atributos']}")
        else:
            st.warning("No se han definido modificaciones para este valor de carta.")
        
        st.markdown("#### Características Base del Personaje:")
        st.write("- **Atributos Base:** Mente: 6, Cuerpo: 4, Carácter: 3")
        st.write("- **Habilidades Base:** 9 puntos + 6 en grupo favorito")
        st.write("- **Puntos Extra:** 15")
        
        bono = suit_bonuses.get(pinta, "No definido")
        st.write(f"- **Bono por Pinta ({pinta}):** + en {bono}")
        
        # Preparar datos para exportar
        character_data = {
            'Carta': [numero],
            'Pinta': [pinta],
            'Narrativa': [narrativa],
            'Quantum Máx': [mod['Quantum'] if mod else 0],
            'Dones': [mod['Dones'] if mod else 0],
            'Mega-Atributos': [mod['Mega-Atributos'] if mod else 0],
            'Atributos Base': ["Mente:6, Cuerpo:4, Carácter:3"],
            'Habilidades Base': ["9 puntos + 6 en grupo favorito"],
            'Puntos Extra': [15],
            'Bono por Pinta': [bono]
        }
        df_character = pd.DataFrame(character_data)
        csv = df_character.to_csv(index=False)
        
        st.download_button(
            label="Descargar Datos del Personaje",
            data=csv,
            file_name='datos_personaje.csv',
            mime='text/csv'
        )

