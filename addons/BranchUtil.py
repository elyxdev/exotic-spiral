import subprocess
import sys
import os
import glob
import requests
import zipfile
import shutil

import time

RGB = [(0, 255, 0), (0, 128, 255), (255, 0, 255)]

def run_command(command):
    """Ejecutar un comando en el sistema y verificar si fue exitoso."""
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return e

def gradient_text(text, colors):
    length = len(text)
    num_colors = len(colors)
    result = ""
    for i, char in enumerate(text):
        color_index = (i * (num_colors - 1)) // length
        t = (i * (num_colors - 1)) / length - color_index
        color1 = colors[color_index]
        color2 = colors[color_index + 1] if color_index + 1 < num_colors else colors[color_index]
        r = int(color1[0] + (color2[0] - color1[0]) * t)
        g = int(color1[1] + (color2[1] - color1[1]) * t)
        b = int(color1[2] + (color2[2] - color1[2]) * t)
        result += f'\033[38;2;{r};{g};{b}m{char}'
    return result + '\033[0m'

def create_commit_tree():
    """Crear un nuevo commit tree desde el estado actual del índice."""
    commit_tree = run_command(["git", "write-tree"])
    commit_message = "Branch para guardar tu server_minecraft"
    commit = run_command(["git", "commit-tree", commit_tree, "-m", commit_message])
    return commit

def force_push(branch_name, commit):
    """Forzar el push al repositorio remoto en la rama especificada."""
    print(gradient_text(f"Realizando push forzado en la rama {branch_name}", [(0, 255, 0), (0, 128, 255)]))
    try:
        run_command(["git", "update-ref", f"refs/heads/{branch_name}", commit])
        run_command(["git", "push", "--force", "origin", branch_name])
        print(gradient_text(f"Push forzado realizado con éxito en la rama {branch_name}.", [(0, 255, 0), (0, 128, 255)]))
    except subprocess.CalledProcessError as e:
        print(gradient_text(f"Error en el push forzado: {e.stderr}", [(255, 0, 0), (255, 128, 0)]))
        sys.exit(1)

def branch():
    # Cambia el directorio actual
    
    os.chdir(f"{glob.glob('/workspaces/*')[0]}/")
    os.system("cd /workspaces/*/")

    new_branch_name = "minecraft_branch"

    # Obtener la URL del repositorio
    print(gradient_text("Obteniendo la URL del repositorio remoto", RGB))
    repo_url = run_command(["git", "remote", "-v"])

    # Eliminar la rama remota si existe
    print(gradient_text(f"Eliminando la rama remota", RGB))
    run_command(["git", "push", "origin", "--delete", new_branch_name])

    # Eliminar la rama local si existe
    print(gradient_text(f"Eliminando la rama local", RGB))
    os.system(f"git branch -D {new_branch_name}")

    # Comprometiendo servidor_mc y config.json
    os.system("git add servidor_minecraft configuracion.json -f")

    # Preparar para el checkout
    os.system("git add . && git commit -a -m 'X' && git push")
    
    # Crear la rama
    os.system(f"git checkout -b {new_branch_name}")

    # Añadir específicamente los archivos requeridos
    print(gradient_text("Añadiendo archivos necesarios", RGB))
    os.system("git add --force servidor_minecraft")
    os.system("git add --force configuracion.json")
    time.sleep(2) #de

    # Crear un commit tree y obtener el commit SHA
    print(gradient_text("Creando el commit tree", RGB))
    commit = create_commit_tree()
    time.sleep(2) #de

    # Push forzado
    print(gradient_text("Realizando push", RGB))
    force_push(new_branch_name, commit)
    time.sleep(2) #de

    # Se regresa a la rama principal para continuar con la ejecución normal
    os.system("git checkout master")

    # Generar la URL de descarga del ZIP
    user_name, repo_name = repo_url.split('/')[-2], repo_url.split('/')[-1].replace('.git', '')
    zip_url = f"https://codeload.github.com/{user_name}/{repo_name}/zip/refs/heads/{new_branch_name}".replace(" (push)", "")
    print(gradient_text(f"\nBranch creado/actualizado localmente: {new_branch_name}\nEnlace al branch para descargar en ZIP: {zip_url}", RGB))
    input(gradient_text("\nPresiona cualquier tecla para continuar...", RGB))
    
def download_and_extract_zip(url, extract_to='.'):
    local_zip_file = "repo.zip"
    
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_zip_file, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        with zipfile.ZipFile(local_zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    finally:
        if os.path.exists(local_zip_file):
            os.remove(local_zip_file)

def link():
    zip_url2 = input(gradient_text("Introduce el enlace directo del archivo ZIP: ", [(0, 255, 0), (0, 128, 255)])).strip()

    # Descargar y extraer el archivo zip
    download_and_extract_zip(zip_url2, os.getcwd())

    # Obtener el nombre del repositorio y el branch del enlace
    repo_name2 = zip_url2.split('/')[-5]
    branch_name2 = zip_url2.split('/')[-1]

    # Formatear el nombre esperado del directorio extraído
    expected_dir_name = f"{repo_name2}-{branch_name2}"

    # Verificar si la carpeta existe
    if not os.path.isdir(expected_dir_name):
        print(gradient_text("Error: No se pudo encontrar la carpeta extraída correctamente.", [(255, 0, 0), (255, 128, 0)]))
        sys.exit(1)

    # Mover archivos del directorio extraído al directorio principal
    extracted_dir = os.path.join(os.getcwd(), expected_dir_name)
    for item in os.listdir(extracted_dir):
        source_path = os.path.join(extracted_dir, item)
        target_path = os.path.join(os.getcwd(), item)
        if os.path.exists(target_path):
            if os.path.isdir(target_path):
                shutil.rmtree(target_path)
            else:
                os.remove(target_path)
        shutil.move(source_path, target_path)
    
    shutil.rmtree(extracted_dir)

    print(gradient_text("\n¡Repositorio descargado y extraído exitosamente!", [(0, 255, 0), (0, 128, 255)]))
    print(gradient_text("\nDirectorio actualizado con el contenido del archivo ZIP.", [(0, 255, 0), (0, 128, 255)]))