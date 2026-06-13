import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk  
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")  

def calcular_limites_algoritmicos(expr_funcion, var_x, h_texto):
    if h_texto == "oo" or h_texto == "-oo":
        x_dinamica = 10.0 if h_texto == "oo" else -10.0
        iteraciones = 0   
        y_actual = 0.0     
        
        while iteraciones < 5:
            y_actual = float(expr_funcion.subs(var_x, x_dinamica).evalf())
            x_dinamica *= 10.0  
            iteraciones += 1    
            
        if abs(y_actual) > 10000:
            return "oo" if y_actual > 0 else "-oo"
        else:
            return round(y_actual, 4)  
         
    else:
        h_val = float(sp.sympify(h_texto).evalf())
        distancias = [0.1, 0.01, 0.001, 0.0001, 0.00001]
        y_izq = 0.0  
        y_der = 0.0  
        
        for d in distancias:
            punto_izq = h_val - d  
            punto_der = h_val + d  
            
            y_izq = float(expr_funcion.subs(var_x, punto_izq).evalf())
            y_der = float(expr_funcion.subs(var_x, punto_der).evalf())
            
        if y_izq > 10000 and y_der > 10000:
            return "oo"
        elif y_izq < -10000 and y_der < -10000:
            return "-oo"
        elif abs(y_izq - y_der) < 0.01:
            return round((y_izq + y_der) / 2, 4)
        else:
            return "No existe (Discontinuidad)"

def procesar_calculo_limite(texto_funcion, texto_tendencia):
    try:
        x = sp.Symbol('x')
        expr_algebraica = sp.sympify(texto_funcion)
        resultado = calcular_limites_algoritmicos(expr_algebraica, x, texto_tendencia)
        return resultado
    except Exception as e:
        return "Error de Sintaxis"

# EMPIEZA LA TAREA DE LA INTERFAZ
class GeoGebraLimitesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculo limites type shit")
        self.root.geometry("1100x650")

        # El profe pidio paneles separados, este es el de los botones
        panel_izquierdo = ctk.CTkFrame(root, width=380, corner_radius=0)
        panel_izquierdo.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)

        titulo = ctk.CTkLabel(panel_izquierdo, text="Configuración de Límites", font=ctk.CTkFont(size=16, weight="bold"))
        titulo.pack(pady=(20, 20))

        # Texto de arriba de la caja de la funcion
        label_func = ctk.CTkLabel(panel_izquierdo, text="Función f(x):")
        label_func.pack(anchor="w", padx=20)
        self.input_funcion = ctk.CTkEntry(panel_izquierdo, width=250)
        self.input_funcion.pack(pady=(0, 10), padx=20)
        self.input_funcion.insert(0, "1/x")

        # Texto de arriba de la caja del limite
        label_tend = ctk.CTkLabel(panel_izquierdo, text="x tiende a (h):")
        label_tend.pack(anchor="w", padx=20)
        self.input_tendencia = ctk.CTkEntry(panel_izquierdo, width=250)
        self.input_tendencia.pack(pady=(0, 15), padx=20)
        self.input_tendencia.insert(0, "oo")

        # Este boton lee lo que el usuario escriba a mano
        btn_calcular = ctk.CTkButton(panel_izquierdo, text="Graficar Entrada Manual", command=self.actualizar_desde_inputs, fg_color="#27ae60", hover_color="#219653")
        btn_calcular.pack(fill=tk.X, pady=(0, 25), padx=20)

        label_ejemplos = ctk.CTkLabel(panel_izquierdo, text="Ejemplos Preestablecidos:", font=ctk.CTkFont(size=12, weight="bold"))
        label_ejemplos.pack(anchor="w", padx=20, pady=(10, 5))

        # BOTONES DE EJEMPLOS (Hacer a mano uno por uno por si acaso)
        btn1 = ctk.CTkButton(panel_izquierdo, text="Asín. Horizontal: 1/x cuando x ➔ oo", command=self.cargar_ejemplo_1, fg_color="#34495e", hover_color="#2c3e50", anchor="w")
        btn1.pack(fill=tk.X, pady=3, padx=20)

        btn2 = ctk.CTkButton(panel_izquierdo, text="Asín. Vertical: 1/x cuando x ➔ 0", command=self.cargar_ejemplo_2, fg_color="#34495e", hover_color="#2c3e50", anchor="w")
        btn2.pack(fill=tk.X, pady=3, padx=20)

        btn3 = ctk.CTkButton(panel_izquierdo, text="Límite Continuo: x^2 - 2 cuando x ➔ 3", command=self.cargar_ejemplo_3, fg_color="#34495e", hover_color="#2c3e50", anchor="w")
        btn3.pack(fill=tk.X, pady=3, padx=20)

        btn4 = ctk.CTkButton(panel_izquierdo, text="Discontinuidad Evitable: (x^2-4)/(x-2)", command=self.cargar_ejemplo_4, fg_color="#34495e", hover_color="#2c3e50", anchor="w")
        btn4.pack(fill=tk.X, pady=3, padx=20)

        # La etiqueta que cambia abajo con la respuesta de la funcion del Bloque 2
        self.lbl_resultado = ctk.CTkLabel(panel_izquierdo, text="Resultado: ", font=ctk.CTkFont(size=14, weight="bold"), text_color="#f1c40f")
        self.lbl_resultado.pack(side=tk.BOTTOM, pady=30)

        # Panel blanco de la derecha donde va el grafico pegado
        self.panel_derecho = ctk.CTkFrame(root, fg_color="white")
        self.panel_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Conectar matplotlib con tkinter para que no se abra otra ventana aparte
        self.fig, self.ax = plt.subplots(figsize=(6, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.panel_derecho)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.actualizar_desde_inputs()

    # FUNCIONES DE LOS BOTONES (Borran lo que hay y ponen el ejemplo)
    def cargar_ejemplo_1(self):
        self.input_funcion.delete(0, tk.END)
        self.input_funcion.insert(0, "1/x")
        self.input_tendencia.delete(0, tk.END)
        self.input_tendencia.insert(0, "oo")
        self.actualizar_grafico("1/x", "oo")

    def cargar_ejemplo_2(self):
        self.input_funcion.delete(0, tk.END)
        self.input_funcion.insert(0, "1/x")
        self.input_tendencia.delete(0, tk.END)
        self.input_tendencia.insert(0, "0")
        self.actualizar_grafico("1/x", "0")

    def cargar_ejemplo_3(self):
        self.input_funcion.delete(0, tk.END)
        self.input_funcion.insert(0, "x**2 - 2")
        self.input_tendencia.delete(0, tk.END)
        self.input_tendencia.insert(0, "3")
        self.actualizar_grafico("x**2 - 2", "3")

    def cargar_ejemplo_4(self):
        self.input_funcion.delete(0, tk.END)
        self.input_funcion.insert(0, "(x**2 - 4)/(x - 2)")
        self.input_tendencia.delete(0, tk.END)
        self.input_tendencia.insert(0, "2")
        self.actualizar_grafico("(x**2 - 4)/(x - 2)", "2")

    def actualizar_desde_inputs(self):
        f = str(self.input_funcion.get())
        t = str(self.input_tendencia.get())
        self.actualizar_grafico(f, t)

    # RE HACER EL DIBUJO CON LOS DATOS NUEVOS
    def actualizar_grafico(self, texto_funcion, texto_tendencia):
        res = procesar_calculo_limite(texto_funcion, texto_tendencia)
        self.lbl_resultado.configure(text="Resultado Límite:\nL = " + str(res))

        if res == "Error de Sintaxis":
            messagebox.showerror("Error", "Revisa la funcion.")
            return

        # Limpiar la pantalla de matplotlib antes de dibujar encima
        self.ax.clear()
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)

        x_sym = sp.Symbol('x')
        try:
            expr = sp.sympify(texto_funcion)
        except:
            return

        # Ajustar los ejes X a mano dependiendo de si es infinito o un numero
        if texto_tendencia == "oo" or texto_tendencia == "-oo":
            min_x, max_x = -20.0, 20.0
            h_val = 99999
        else:
            valor_h = float(sp.sympify(texto_tendencia).evalf())
            h_val = valor_h
            min_x = valor_h - 5.0
            max_x = valor_h + 5.0

        # CAMBIO: NO USAR NUMPY, HACER EL LINSPACE MANUAL CON UN FOR
        x_vals = []
        pasos = 400
        ancho_paso = (max_x - min_x) / pasos
        
        for i in range(pasos + 1):
            x_vals.append(min_x + (i * ancho_paso))

        # Ir metiendo los resultados de Y uno por uno en la lista vacia
        y_vals = []
        for v in x_vals:
            try:
                # OJO: Si x vale justo h, saltarselo para que no se caiga por division por cero
                if h_val != 99999 and abs(v - h_val) < 0.0001:
                    y_vals.append(float('nan'))
                    continue
                    
                resultado_punto = expr.subs(x_sym, v).evalf()
                resultado_float = float(resultado_punto)
                
                # Si el grafico vuela muy arriba, poner nan para que matplotlib deje el espacio en blanco
                if resultado_float > 50 or resultado_float < -50:
                    y_vals.append(float('nan')) 
                else:
                    y_vals.append(resultado_float)
            except:
                y_vals.append(float('nan'))

        # Tira la linea azul de la funcion a la pantalla
        self.ax.plot(x_vals, y_vals, color="#3498db", linewidth=2)

        # Si no es infinito, poner las marcas rojas del limite
        if h_val != 99999:
            self.ax.axvline(x=h_val, color="red", linestyle=":")
            
            # Si dio un numero real, poner el puntito rojo encima
            if res != "oo" and res != "-oo" and res != "No existe (Discontinuidad)":
                punto_y = float(res)
                self.ax.plot(h_val, punto_y, 'ro')

        self.ax.set_title("Grafico de la funcion", color="#2c3e50")
        self.ax.set_ylim(-10, 10)
        self.canvas.draw()

# EL MAIN PARA COMPILAR
if __name__ == "__main__":
    ventana = ctk.CTk()  
    app = GeoGebraLimitesApp(ventana)
    ventana.mainloop()