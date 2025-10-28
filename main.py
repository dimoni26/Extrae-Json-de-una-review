import streamlit as st
from langchain import PromptTemplate
from langchain_openai import OpenAI


template = """\
For the following text, extract the following \
information:

sentiment: Is the customer happy with the product? 
Answer Positivo if yes, Negativo if \
not, Neutral if either of them, or Desconocido if unknown.

delivery_days: How many days did it take \
for the product to arrive? If this \
information is not found, output No hay información sobre esto.

price_perception: How does it feel the customer about the price? 
Answer Caro if the customer feels the product is expensive, 
Barato if the customer feels the product is cheap,
not, Normal if either of them, or Desconocido if unknown.
respond in Spanish always.
Format the output as bullet-points text with the \
following keys:
- Sentimiento
- ¿Cuánto tiempo tardó en entregarse?
- ¿Cómo se percibió el precio?

Input example:
This dress is pretty amazing. It arrived in two days, just in time for my wife's anniversary present. It is cheaper than the other dresses out there, but I think it is worth it for the extra features.

Output example:
- Sentimiento: Positivo
- ¿Cuánto tiempo tardó en entregarse? 2 días
- ¿Cómo se percibió el precio? Barato

text: {review}
"""

#PromptTemplate variables definition
prompt = PromptTemplate(
    input_variables=["review"],
    template=template,
)


#LLM and key loading function
def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
    return llm


#Page title and header
st.set_page_config(page_title="Extrae la información clave de las reseñas de productos")
st.header("Extrae la información clave de las reseñas de productos")


#Intro: instructions
col1, col2 = st.columns(2)

with col1:
    st.markdown("Extrae la información clave de las reseñasde producto")
    st.markdown("""
        - Sentimiento
        - ¿Cuánto tiempo tardó en entregarse?
        - ¿Cómo se percibió el precio?
        """)

with col2:
    st.write("Contacta con [Dimoni](https://autmatix.es) para construir tus proyectos IA personalizados")


#Input OpenAI API Key
st.markdown("## Inserta tu OpenAI API Key")

def get_openai_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input", type="password")
    return input_text

openai_api_key = get_openai_api_key()


# Input
st.markdown("## Inserta la reseña del producto")

def get_review():
    review_text = st.text_area(label="Product Review", label_visibility='collapsed', placeholder="Your Product Review...", key="review_input")
    return review_text

review_input = get_review()

if len(review_input.split(" ")) > 700:
    st.write("Por favor introduce una reseña de producto. Máximo 700 palabras.")
    st.stop()

    
# Output
st.markdown("### Datos Clave Extraídos")

if review_input:
    if not openai_api_key:
        st.warning('Por favor inserta tu OpenAI API KEY. \
            Instrucciones [aquí](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', 
            icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_review = prompt.format(
        review=review_input
    )

    key_data_extraction = llm(prompt_with_review)

    st.write(key_data_extraction)
