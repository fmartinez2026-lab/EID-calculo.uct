import sympy as sp

def calcular_limites_algoritmicos(expr_funcion, var_x, h_texto):# BLOQUE 2: MOTOR ALGORÍTMICO DE CÁLCULO DE LÍMITES
    """
    Función principal que resuelve límites algebraicos, trigonométricos e infinitos.
    Aplica aproximaciones numéricas mediante estructuras cíclicas nativas.
    """
    #EVALUACIÓN CUANDO X TIENDE AL INFINITO (oo o -oo)
    if h_texto == "oo" or h_texto == "-oo":
        x_dinamica = 10.0 if h_texto == "oo" else -10.0# Define si iniciamos con un número positivo grande (10) o negativo (-10)
        iteraciones = 0   # Contador para controlar las vueltas del ciclo
        y_actual = 0.0     # Variable para almacenar el resultado de la función
        
        # CICLO WHILE: Simula el viaje al infinito multiplicando x por 10 en cada vuelta
        while iteraciones < 5:
            # .subs() reemplaza la 'x' por el número gigante actual; .evalf() lo calcula en decimal
            y_actual = float(expr_funcion.subs(var_x, x_dinamica).evalf())
            x_dinamica *= 10.0  # El número crece exponencialmente: 10 -> 100 -> 1000 -> 10000 -> 100000
            iteraciones += 1    # Incrementa el contador para avanzar y evitar un bucle infinito
            
        # CONTROL DE DIVERGENCIA EN EL INFINITO: Si el número explota, el límite es infinito
        if abs(y_actual) > 10000:
            return "oo" if y_actual > 0 else "-oo"
        else:
            return round(y_actual, 4)  # Si se estabiliza, retorna la asíntota horizontal real
         
    # EVALUACIÓN CUANDO X TIENDE A UN PUNTO REAL H
    else:
        # Traduce el string de la tendencia (ej: "2" o "0") a un número decimal real de Python
        h_val = float(sp.sympify(h_texto).evalf())
        
        # Sucesión de distancias decrecientes para aproximarse milimétricamente al punto sin tocarlo
        distancias = [0.1, 0.01, 0.001, 0.0001, 0.00001]
        y_izq = 0.0  # Guardará la altura alcanzada por el camino izquierdo
        y_der = 0.0  # Guardará la altura alcanzada por el camino derecho
        
        # Recorre las distancias para evaluar el comportamiento en entornos reducidos
        for d in distancias:
            punto_izq = h_val - d  # Calcula la coordenada un paso a la izquierda de h (ej: 1.99999)
            punto_der = h_val + d  # Calcula la coordenada un paso a la derecha de h (ej: 2.00001)
            
            # Evaluamos la función en estos puntos laterales eludiendo la indeterminación exacta 0/0
            y_izq = float(expr_funcion.subs(var_x, punto_izq).evalf())
            y_der = float(expr_funcion.subs(var_x, punto_der).evalf())
            
        # REGLAS DE DECISIÓNES LOGICAS MATEMÁTICAS (CRITERIOS DE EXISTENCIA Y ASÍNTOTAS)
        
        # Regla 1: Si ambos lados explotan positivamente, detecta una asíntota vertical hacia +infinito
        if y_izq > 10000 and y_der > 10000:
            return "oo"
            
        # Regla 2: Si ambos lados explotan negativamente, detecta una asíntota vertical hacia -infinito
        elif y_izq < -10000 and y_der < -10000:
            return "-oo"
            
        # Regla 3: Si la diferencia entre ambos lados es despreciable, los caminos confluyen al mismo valor
        elif abs(y_izq - y_der) < 0.01:
            # Promedia ambos extremos para neutralizar el margen de error del redondeo flotante
            return round((y_izq + y_der) / 2, 4)
            
        # Regla 4: Si los valores difieren drásticamente, hay un salto o una discontinuidad esencial
        else:
            return "No existe (Discontinuidad)"

# CONECTOR INTERFAZ-LOGICA Y MANEJO DE ERRORES
def procesar_calculo_limite(texto_funcion, texto_tendencia):
    """
    Recibe las entradas de texto desde el usuario, inicializa las variables algebraicas,
    y protege la aplicación ante errores de escritura (Criterio 4 de la rúbrica).
    """
    try:
        # Definimos de forma pura que la letra 'x' será el símbolo matemático del sistema
        x = sp.Symbol('x')
        
        # sp.sympify() parsea y traduce el string de texto a una expresión algebraica real interpretable
        expr_algebraica = sp.sympify(texto_funcion)
        
        # Invoca tu motor matemático (Bloque 2) y captura el resultado final
        resultado = calcular_limites_algoritmicos(expr_algebraica, x, texto_tendencia)
        
        return resultado
        
    except Exception as e:
        # Bloque de contingencia: si el usuario ingresa una sintaxis inválida, la app no colapsa
        return "Error de Sintaxis"
    

