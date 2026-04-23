import sys
import os

# Colores predefinidos variados para asignar a cada parte suelta
COLORES_AUTO = [
    (0.55, 0.27, 0.07),  # cafe (tronco)
    (0.18, 0.55, 0.20),  # verde oscuro
    (0.24, 0.70, 0.25),  # verde claro
    (0.80, 0.20, 0.20),  # rojo
    (0.20, 0.40, 0.80),  # azul
    (0.85, 0.70, 0.10),  # amarillo
    (0.60, 0.20, 0.70),  # morado
    (0.90, 0.50, 0.10),  # naranja
    (0.10, 0.70, 0.70),  # cyan
    (0.90, 0.30, 0.60),  # rosa
]

def encontrar_grupos(caras):
    """Flood fill para encontrar partes sueltas (grupos de caras conectadas)"""
    vertice_a_caras = {}
    for i, cara in enumerate(caras):
        for v in cara:
            if v not in vertice_a_caras:
                vertice_a_caras[v] = []
            vertice_a_caras[v].append(i)

    visitado = [False] * len(caras)
    grupos = []

    for i in range(len(caras)):
        if visitado[i]:
            continue
        grupo = []
        cola = [i]
        visitado[i] = True
        while cola:
            cara_actual = cola.pop()
            grupo.append(cara_actual)
            for v in caras[cara_actual]:
                for cara_vecina in vertice_a_caras.get(v, []):
                    if not visitado[cara_vecina]:
                        visitado[cara_vecina] = True
                        cola.append(cara_vecina)
        grupos.append(grupo)

    return grupos

def obj_to_cpp(archivo_obj, nombre_funcion=None, escala=1.0):
    vertices = []
    caras = []

    if nombre_funcion is None:
        nombre_funcion = os.path.splitext(os.path.basename(archivo_obj))[0]

    with open(archivo_obj, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if linea.startswith('v '):
                partes = linea.split()
                x = float(partes[1]) * escala
                y = float(partes[2]) * escala
                z = float(partes[3]) * escala
                vertices.append((x, y, z))
            elif linea.startswith('f '):
                partes = linea.split()[1:]
                indices = [int(p.split('/')[0]) - 1 for p in partes]
                caras.append(indices)

    # Detectar partes sueltas
    grupos = encontrar_grupos(caras)

    codigo = []
    codigo.append(f"void {nombre_funcion}() {{")
    codigo.append(f"    // {len(vertices)} vertices, {len(caras)} caras, {len(grupos)} partes sueltas")
    codigo.append("")

    for g_idx, grupo in enumerate(grupos):
        color = COLORES_AUTO[g_idx % len(COLORES_AUTO)]
        codigo.append(f"    // --- parte {g_idx + 1} ({len(grupo)} caras) ---")
        codigo.append(f"    glColor3f({color[0]:.4f}f, {color[1]:.4f}f, {color[2]:.4f}f);")
        codigo.append("")

        for cara_idx in grupo:
            cara = caras[cara_idx]
            num_verts = len(cara)

            if num_verts == 3:
                codigo.append("    glBegin(GL_TRIANGLES);")
            elif num_verts == 4:
                codigo.append("    glBegin(GL_QUADS);")
            else:
                codigo.append("    glBegin(GL_POLYGON);")

            for idx in cara:
                v = vertices[idx]
                codigo.append(f"        glVertex3f({v[0]:.4f}f, {v[1]:.4f}f, {v[2]:.4f}f);")

            codigo.append("    glEnd();")

        codigo.append("")

    codigo.append("}")
    return "\n".join(codigo)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python obj_to_cpp.py modelo.obj [nombre_funcion] [escala]")
        print("Ejemplo: python obj_to_cpp.py arbol.obj arbol 100")
        sys.exit(1)

    archivo = sys.argv[1]
    nombre = sys.argv[2] if len(sys.argv) > 2 else None
    escala = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0

    resultado = obj_to_cpp(archivo, nombre, escala)

    carpeta = os.path.dirname(os.path.abspath(__file__))
    nombre_salida = (nombre or os.path.splitext(os.path.basename(archivo))[0]) + "_opengl.txt"
    salida = os.path.join(carpeta, nombre_salida)

    with open(salida, 'w') as f:
        f.write(resultado)

    print(resultado)
    print(f"\n// Guardado en: {salida}")
