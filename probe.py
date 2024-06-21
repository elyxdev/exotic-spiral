import os, subprocess
def obtener_salida_comando(comando):
    proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    salida, error = proceso.communicate()  # Obtener la salida y los errores del proceso
    salida_decodificada = salida.decode('utf-8')
    error_decodificado = error.decode('utf-8')
    return salida_decodificada, error_decodificado

res,err = obtener_salida_comando("git lfs ls-files")
print(res, res=="")
os.system('git lfs track "*.zip"')
res,err = obtener_salida_comando("git lfs ls-files")
print(res, res=="")