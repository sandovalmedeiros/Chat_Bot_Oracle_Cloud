# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 11:19:19 2024

@author: Sei
"""

import streamlit as st
import oci
from oci.generative_ai_inference.models import ChatDetails, TextContent, Message, GenericChatRequest, OnDemandServingMode

# Configuração OCI
compartment_id = "ocid1.tenancy.oc1..aaaaaaaahzmfodyyhz7vzcktsbkwazcu3ohadbwvwloi33v4gox5yty7kobq"
CONFIG_PROFILE = "DEFAULT"
config = oci.config.from_file('~/.oci/config', CONFIG_PROFILE)

# Endpoint do serviço OCI Generative AI
endpoint = "https://inference.generativeai.sa-saopaulo-1.oci.oraclecloud.com"
generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(
    config=config, 
    service_endpoint=endpoint, 
    retry_strategy=oci.retry.NoneRetryStrategy(), 
    timeout=(10, 240)
)

# Definir o modelo a ser utilizado
model_id = "ocid1.generativeaimodel.oc1.sa-saopaulo-1.amaaaaaask7dceyaz4nxgyqobjvphdho6cup7opj7niharfohm5luw3jbnka"

# Função para enviar mensagem ao modelo
def get_chatbot_response(user_input):
    chat_detail = ChatDetails()
    
    content = TextContent()
    content.text = user_input
    
    message = Message()
    message.role = "USER"
    message.content = [content]
    
    chat_request = GenericChatRequest()
    chat_request.api_format = GenericChatRequest.API_FORMAT_GENERIC
    chat_request.messages = [message]
    chat_request.max_tokens = 600
    chat_request.temperature = 1
    chat_request.frequency_penalty = 0
    chat_request.top_p = 0.75
    chat_request.top_k = -1

    chat_detail.serving_mode = OnDemandServingMode(model_id=model_id)
    chat_detail.chat_request = chat_request
    chat_detail.compartment_id = compartment_id

    response = generative_ai_inference_client.chat(chat_detail)

    # Extrair a resposta do modelo
    if hasattr(response.data, 'chat_response') and response.data.chat_response.choices:
        return response.data.chat_response.choices[0].message.content[0].text
    return "Desculpe, não consegui entender a sua pergunta."

# Configuração do layout do Streamlit
st.title("Chatbot Generative AI - OCI")
st.write("Converse com o assistente e faça suas perguntas!")

# Caixa de entrada do usuário
user_input = st.text_input("Digite sua mensagem:", "")

# Histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Se o usuário enviar uma mensagem
if user_input:
    # Adicionar a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Obter a resposta do chatbot
    response = get_chatbot_response(user_input)
    
    # Adicionar a resposta do chatbot ao histórico
    st.session_state.messages.append({"role": "bot", "content": response})

# Exibir o histórico de conversa
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.write(f"**Você:** {msg['content']}")
    else:
        st.write(f"**Chatbot:** {msg['content']}")
