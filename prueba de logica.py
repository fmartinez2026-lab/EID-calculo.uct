import sympy as sp

def calcular_limites_algoritmicos(expr_funcion, var_x, h_texto):
    """
    Función que resuelve límites algebraicos, trigonométricos e infinitos.
    Aplica aproximaciones numéricas mediante estructuras cíclicas nativas.
    """
    if h_texto == "oo" or h_texto == "-oo":

        x_dinamica=10.0 if h_texto=="oo" else -10.0
        iteraciones= 0
        y_actual= 0.0

        while iteraciones< 5:
            y_actual= float(expr_funcion.subs(var_x, x_dinamica).evalf())
            x_dinamica *= 10.0
            iteraciones+= 1

        if abs(y_actual)> 10000:
            return "oo" if y_actual> 0 else "-oo"
        else:
            return round(y_actual, 4)
    
    else:
        h_val= float(sp.sympify(h_texto).evalf())

        distancias= [0.1, 0.01, 0.001, 0.0001, 0.00001]

        y_izq= 0.0 
        y_der= 0.0

        for d in distancias:
            punto_izq= h_val- d 
            punto_der= h_val+ d 

            y_izq= float(expr_funcion.subs(var_x, punto_izq).evalf())
            y_der= float(expr_funcion.subs(var_x, punto_der).evalf())

        if y_izq> 10000 and y_der> 10000:
            return "oo"
    
        elif y_izq< -10000 and y_der< -10000:
            return "-oo"
        
        elif abs(y_izq - y_der) < 0.01:
            return round((y_izq + y_der) / 2, 4)
        
        else:
            return "No existe (Discontinuidad)"

        
# =====================================================================
# BLOQUE 3: CONECTOR CON LA INTERFAZ Y CONTROL DE ERRORES CRÍTICOS
# =====================================================================
def procesar_calculo_limite(texto_funcion, texto_tendencia):
    """
    Recibe las entradas de texto, inicializa las variables algebraicas,
    y protege la aplicación ante errores de escritura del usuario.
    """
    try:
        # 1. Definimos que la letra 'x' será una variable matemática simbólica
        x = sp.Symbol('x')
        
        # 2. sp.sympify() traduce el string a una ecuación algebraica real
        expr_algebraica = sp.sympify(texto_funcion)
        
        # 3. Invoca tu motor lógico (el que acabas de corregir) y guarda el resultado
        resultado = calcular_limites_algoritmicos(expr_algebraica, x, texto_tendencia)
        
        return resultado
        
    except Exception as e:
        # Si el usuario escribe mal la ecuación, el programa no muere.
        # Atrapa el error y devuelve un aviso amigable.
        return "Error de Sintaxis"


# =====================================================================
# BLOQUE 4: BANCO DE PRUEBAS AUTOMÁTICAS POR CONSOLA
# =====================================================================
if __name__ == "__main__":
    print("\n==============================================")
    print("  EJECUTANDO MOTOR LÓGICO DE FRANCISCO MARTÍNEZ ")
    print("==============================================\n")
    
    # Prueba 1: Límite Algebraico Irreducible (Indeterminación 0/0)
    func_1 = "(x**2 - 4) / (x - 2)"
    tend_1 = "2"
    res_1 = procesar_calculo_limite(func_1, tend_1)
    print(f"[Prueba 1] f(x) = {func_1} cuando x -> {tend_1}")
    print(f"           Resultado obtenido: {res_1}\n")
    
    # Prueba 2: Límite Trigonométrico Notable (Indeterminación sen(0)/0)
    func_2 = "sin(x) / x"
    tend_2 = "0"
    res_2 = procesar_calculo_limite(func_2, tend_2)
    print(f"[Prueba 2] f(x) = {func_2} cuando x -> {tend_2}")
    print(f"           Resultado obtenido: {res_2}\n")
    
    # Prueba 3: Límite Polinomial Racional tendiendo al Infinito Positivo (Asíntota Horizontal)
    func_3 = "(2*x + 5) / (3*x - 1)"
    tend_3 = "oo"
    res_3 = procesar_calculo_limite(func_3, tend_3)
    print(f"[Prueba 3] f(x) = {func_3} cuando x -> {tend_3}")
    print(f"           Resultado obtenido: {res_3}\n")
    
    # Prueba 4: Asíntota Vertical (Infinito en un punto real)
    func_4 = "1 / x**2"
    tend_4 = "0"
    res_4 = procesar_calculo_limite(func_4, tend_4)
    print(f"[Prueba 4] f(x) = {func_4} cuando x -> {tend_4}")
    print(f"           Resultado obtenido: {res_4}\n")
    
    print("==============================================")
    print("        PRUEBAS FINALIZADAS CON ÉXITO         ")
    print("==============================================\n")