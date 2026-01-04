import os
import sys

# Optional: Import client libraries (fallback to mock if not installed/configured)
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Simple env loader since python-dotenv might not be installed
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), "../../.env")
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith("#") and "=" in line:
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

load_env()

class SalesBot:
    def __init__(self, strategy_file="sales_strategy.md"):
        self.strategy_file = strategy_file
        self.context = self._load_strategy()
        
        # Configure Gemini if key is present
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_key and GEMINI_AVAILABLE:
            genai.configure(api_key=self.gemini_key)
        
    def _load_strategy(self):
        """Loads the sales strategy from the markdown file to use as system context."""
        # Priority: Root sales_strategy.md, then previous session brain, then default
        root_path = os.path.join(os.path.dirname(__file__), "../../sales_strategy.md")
        brain_path = "/home/llorens/.gemini/antigravity/brain/c07f2033-7f61-40b4-b9f5-1fa11288eac9/sales_strategy.md"
        
        if os.path.exists(root_path):
            with open(root_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif os.path.exists(brain_path):
            with open(brain_path, 'r', encoding='utf-8') as f:
                return f.read()
        return "Estrategia no encontrada. Por favor, asegúrate de que 'sales_strategy.md' existe."

    def generate_response(self, user_message, provider="auto"):
        """
        Generates a response based on the user message and the sales strategy.
        provider: 'gemini', 'mock', or 'auto' (prefers gemini)
        """
        
        system_prompt = f"""
        ESTRATEGIA DE VENTAS Y CONTEXTO (SÍGUELA ESTRICTAMENTE):
        {self.context}
        
        INSTRUCCIONES DE COMPORTAMIENTO:
        1. ACTÚA COMO: "Asesor de LocalPro". Siempre identifícate como parte de **LocalPro**.
        2. MÉTODO AIDA: 
           - Fase 1 (Atención/Interés): Responde dudas, destaca beneficios, muestra demo.
           - Fase 2 (Deseo): Enfoca el PLAN PROFESIONAL (59€) como la mejor opción.
           - Fase 3 (Acción): Solo da el Bizum si el cliente lo pide o confirma compra.
        3. REGLA CRÍTICA BIZUM: NO des el número de Bizum ni el concepto hasta que el cliente lo pida explícitamente.
        4. TONO: Corto, informal, persuasivo y cercano.
        
        MENSAJE DEL CLIENTE: "{user_message}"
        RESPUESTA:
        """

        if provider == "auto":
            if self.gemini_key and GEMINI_AVAILABLE:
                provider = "gemini"
            else:
                provider = "mock"

        if provider == "mock":
            return self._mock_response(user_message)
        
        if provider == "gemini" and GEMINI_AVAILABLE:
            return self._call_gemini(system_prompt, user_message=user_message)
            
        return "⚠️ Error: Proveedor de IA no disponible. (Mock Mode)"

    def _mock_response(self, message):
        """Respuestas predefinidas profesionales para cuando no hay IA."""
        msg = message.lower()
        if "precio" in msg or "cuanto" in msg or "costa" in msg:
            return "En LocalPro tenemos 3 planes de PAGO ÚNICO. El más recomendado es el **Profesional por 59€**, que incluye dominio propio y Blog con IA. No hay cuotas mensuales. ¿Te gustaría activarlo?"
        if "pago" in msg or "pagar" in msg or "bizum" in msg:
            return "El pago se realiza por **Bizum al +34 622 795 058**. Recuerda poner como concepto: **web [nombre de tu negocio]**. En cuanto lo recibamos, te avisamos y empezamos hoy mismo."
        return f"¡Hola! Soy el Asesor de LocalPro. He preparado una demo profesional para tu negocio aquí: https://localpro.top/lampista-serra/. ¿Qué te parece el diseño?"

    def _call_gemini(self, prompt, user_message=""):
        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"⚠️ Error con Gemini API (Falling back to Mock): {str(e)}")
            return self._mock_response(user_message)

if __name__ == "__main__":
    bot = SalesBot()
    print("🤖 SalesBot Iniciado (Escribe 'salir' para terminar)")
    if bot.gemini_key and GEMINI_AVAILABLE:
        print(f"✅ Modo: IA Real (Gemini) activado.")
    else:
        print(f"🔶 Modo: Mock (Simulación). Falta API Key o librería 'google-generativeai'.")
    print("---")
    while True:
        user_input = input("Cliente: ")
        if user_input.lower() in ['salir', 'exit']:
            break
        response = bot.generate_response(user_input, provider="auto")
        print(f"Bot: {response}")
        print("---")
