"""
🤖 DÉMO INTÉGRATION LLM GRATUITE - PhytoAI
===========================================

Ce fichier démontre comment intégrer facilement des LLMs gratuits
dans votre assistant PhytoAI.

Options gratuites recommandées :
1. Google Gemini : 1500 requêtes/jour
2. Groq : 6K tokens/minute
3. Hugging Face : 30K caractères/mois
"""

import streamlit as st

# ===============================
# 1. GOOGLE GEMINI (GRATUIT)
# ===============================

def demo_gemini_integration():
    """Démo intégration Google Gemini gratuite"""
    
    st.subheader("🧠 Google Gemini - 1500 requêtes/jour GRATUITES")
    
    # Configuration
    gemini_key = st.text_input("Clé API Gemini:", type="password", 
                               help="Gratuite sur https://makersuite.google.com/app/apikey")
    
    if gemini_key:
        st.success("✅ Clé configurée ! Test possible ci-dessous")
        
        # Code d'intégration simple
        st.code("""
# Installation : pip install google-generativeai
import google.generativeai as genai

def ask_phytoai_gemini(question, api_key):
    genai.configure(api_key=api_key)
    
    # Prompt spécialisé phytothérapie
    prompt = f'''
    Tu es un expert PhytoAI avec accès à 1.4M molécules.
    
    QUESTION : {question}
    
    CONTEXTE PHYTOAI :
    - 95.7% précision IA
    - 141 découvertes validées
    - Spécialité : synergies, biodisponibilité
    
    Réponds avec expertise scientifique.
    '''
    
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

# UTILISATION
response = ask_phytoai_gemini("Curcumine biodisponibilité", "your_key")
        """, language="python")
        
        # Test en direct
        test_question = st.text_input("🧪 Testez avec votre question:", 
                                      placeholder="Ex: Curcumine dosage optimal")
        
        if st.button("🚀 Tester Gemini") and test_question:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(f"""
Tu es expert PhytoAI. Question: {test_question}
Réponds comme un spécialiste en phytothérapie avec données précises.
                """)
                
                st.markdown("**🎯 Réponse Gemini :**")
                st.write(response.text)
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")

# ===============================
# 2. GROQ (ULTRA RAPIDE)
# ===============================

def demo_groq_integration():
    """Démo intégration Groq ultra-rapide"""
    
    st.subheader("⚡ Groq - 6K tokens/minute GRATUITS")
    
    groq_key = st.text_input("Clé API Groq:", type="password",
                             help="Gratuite sur https://console.groq.com/keys")
    
    if groq_key:
        st.success("⚡ Prêt pour vitesse fulgurante !")
        
        st.code("""
# Installation : pip install groq
from groq import Groq

def ask_phytoai_groq(question, api_key):
    client = Groq(api_key=api_key)
    
    response = client.chat.completions.create(
        messages=[{
            "role": "system",
            "content": "Expert PhytoAI - 1.4M molécules - Réponds avec précision"
        }, {
            "role": "user",
            "content": question
        }],
        model="llama3-8b-8192",  # Gratuit !
        temperature=0.3
    )
    
    return response.choices[0].message.content

# UTILISATION  
response = ask_phytoai_groq("Resveratrol mécanismes", "your_key")
        """, language="python")

# ===============================
# 3. HUGGING FACE (SIMPLE)
# ===============================

def demo_hf_integration():
    """Démo Hugging Face simple"""
    
    st.subheader("🤗 Hugging Face - 30K caractères/mois")
    
    st.code("""
# Installation : pip install requests
import requests

def ask_phytoai_hf(question):
    API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
    
    response = requests.post(API_URL, 
        headers={"Authorization": f"Bearer {your_token}"},
        json={"inputs": f"PhytoAI expert: {question}"})
    
    return response.json()

# UTILISATION (sans clé pour certains modèles)
response = ask_phytoai_hf("Quercétine antioxydant")
    """, language="python")

# ===============================
# 4. INTÉGRATION DANS STREAMLIT
# ===============================

def demo_streamlit_integration():
    """Comment intégrer dans votre app Streamlit"""
    
    st.subheader("🔧 Intégration dans votre Assistant PhytoAI")
    
    st.markdown("""
    **Étapes simples :**
    
    1. **Ajoutez dans `requirements.txt` :**
    ```
    google-generativeai==0.8.3
    groq==0.11.0
    ```
    
    2. **Modifiez votre fonction `page_assistant()` :**
    """)
    
    st.code("""
def page_assistant():
    # Configuration API
    with st.expander("⚙️ Config LLM"):
        provider = st.selectbox("API:", ["Simulation", "Gemini", "Groq"])
        if provider != "Simulation":
            api_key = st.text_input("Clé:", type="password")
    
    # Fonction réponse
    def get_response(question):
        if provider == "Gemini" and api_key:
            return ask_gemini(question, api_key)
        elif provider == "Groq" and api_key:  
            return ask_groq(question, api_key)
        else:
            return simulation_response(question)
    
    # Interface chat normal
    if prompt := st.chat_input("Question..."):
        response = get_response(prompt)
        st.write(response)
    """, language="python")

# ===============================
# MAIN DEMO
# ===============================

def main():
    st.title("🤖 Intégration LLM Gratuite - PhytoAI")
    
    st.markdown("""
    ## 🎯 Votre Question : APIs Gratuites
    
    **RÉPONSE : OUI, très facilement !**
    
    Pour une app peu utilisée, vous avez d'**excellentes options gratuites** :
    
    ### ✅ **Recommandations par ordre :**
    
    1. **🥇 Google Gemini** - 1500 requêtes/jour gratuites
       - Qualité excellente pour phytothérapie
       - Intégration 5 lignes de code
       - Limite généreuse pour usage faible
    
    2. **🥈 Groq** - 6K tokens/minute gratuits  
       - Vitesse fulgurante (500+ tokens/sec)
       - Modèles Llama3, Mixtral
       - Parfait pour réponses rapides
    
    3. **🥉 Hugging Face** - 30K caractères/mois
       - Simple, pas toujours de clé requise
       - Modèles variés disponibles
    
    ### 💡 **Pas de complication nécessaire !**
    
    Aucun besoin de solutions complexes. Les APIs gratuites sont **parfaites** 
    pour une app avec usage faible.
    """)
    
    # Démos interactives
    tab1, tab2, tab3, tab4 = st.tabs(["🧠 Gemini", "⚡ Groq", "🤗 HuggingFace", "🔧 Intégration"])
    
    with tab1:
        demo_gemini_integration()
    
    with tab2:
        demo_groq_integration()
    
    with tab3:
        demo_hf_integration()
    
    with tab4:
        demo_streamlit_integration()

if __name__ == "__main__":
    main() 