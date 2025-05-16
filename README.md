# Secdevops challenge

Este proyecto es una API basada en **FastAPI** que permite subir archivos y obtener análisis de seguridad usando la API de **VirusTotal**. Devuelve resultados tanto en **HTML** como en **JSON**.
La api esta limitada a archivos de 32 MB. Para más información https://docs.virustotal.com/reference/files-scan

# Índice
1.  [Descripción](#secdevops-challenge)
2.  [Características](#caracteristicas)
3.  [Anotación](#anotacion)
4.  [Requisitos](#requisitos)
5.  [Tecnologías](#tecnologias)
6.  [Pasos para construir la imagen](#pasos-para-construir-la-imagen)
7.  [Prueba del contenedor](#prueba-del-contenedor)
8.  [Interpretación de la salida](#interpretacion-de-la-salida)
9.  [Detener el contenedor](#detener-el-contenedor)
10. [Eliminar el contenedor](#eliminar-el-contenedor)
11. [Eliminar imagen del contenedor](#eliminar-imagen-del-contenedor)
12. [Créditos](#creditos) 

## Caracteristicas
- Subida de archivos para análisis.
- Integración con la API de VirusTotal.
- Respuesta en formato HTML o JSON.
- Gestión de rutas y plantillas con Jinja2.
- Servido con Uvicorn.

### Anotacion
Por motivos de seguridad y buenas practicas no es recomendable subir la API Key a repositorios remotos, por lo que la llave se pasara como una variable de entorno al crear el contenedor en Docker.

### Requisitos
- Tener instalado Python3
- Docker
- API Key de VirusTotal
- CURL

### Tecnologias
* FastAPI
* Jinja2
* HTTPX
* Uvicorn
* Pytest

## Pasos para construir la imagen
1. Clona el repositorio:

```bash
git clone https://github.com/jlorenzano/secdevops-challenge.git
cd secdevops-challenge
```

2. Crea un entorno virtual en Python

```bash
python -m venv venv
```
Activacion de entorno virtual
* En Linux/macOS
```bash
source venv/bin/activate
```
* En Windows
```bash
venv\Scripts\activate
```

3.- Instala las dependencias

```bash
pip install -r requirements.txt
```

4.- Construye la imagen del contenedor
```bash
docker build -t secdevops-challenge .
```

5.- Crea el contenedor 
* Mostrara la ejecución del contenedor activa
```bash
docker run --name secdevops-container -e VT_API_KEY=<API_KEY> -p 8000:8000 secdevops-challenge:latest
```
* Mostrara la ejecucion del contenedor desmontable
```bash
docker run --name secdevops-container -d -e VT_API_KEY=<API_KEY> -p 8000:8000 secdevops-challenge:latest
```
Donde `<API_KEY>` es el API Key de VirusTotal necesaria para realizar el analisis

## Prueba del contenedor
* La aplicación tiene una interfaz muy sencilla que se puede acceder por http://localhost:8000

![image](https://github.com/user-attachments/assets/741e48ee-d7ef-411c-9f60-91b04477ed9c)

* pero la llamada a la API es por el siguiente endpoint http://localhost:8000/scan-file/

Para subir un archivo a la api se puede hacer por medio de un CURL
```bash
curl -F "file=@<RUTA DEL ARCHIVO>" http://localhost:8000/scan-file/      
```
Donde `<RUTA_DEL_ARCHIVO>` es la ruta del archivo a escanear, puede ser:  
- Una ruta absoluta: `/home/usuario/archivo.txt`  
- O una ruta relativa: `./archivo.txt`

### Interpretacion de la salida
La salida cuando se hacer por curl regresara un json con todos los datos del analisis hecho por virus total relacionado a todos los motores de AV, pero en la parte final viene un campo llamado summary que contiene un resumen de todos los motores de AV, ejemplo:
```bash
"summary":{
  "Malicious":0,
  "Suspicious":0,
  "Undetected":61,
  "Harmless":0,
  "Timeout":0,
  "Confirmed Timeout":0,
  "Failure":0,
  "Unsupported":14
}
```

## Detener el contenedor
Este comando detendra el contenedor, pero no lo eliminara
```bash
docker stop secdevops-container
```

## Eliminar el contenedor
Este comando eliminara el contenedor
```bash
docker rm secdevops-container
```

## Eliminar imagen del contenedor
Ya que se elimino el contenedor que se creo, se puede eliminar la imagen del conenedor (Se recomienda eliminar primero el contenedor)
```bash
docker rmi secdevops-challenge
```
Si se quiere forzar la eliminacion de la imagen se usara
```bash
docker rmi -f secdevops-challenge
```

## Creditos
Proyecto desarrollado por: **Jose Carlos Lorenzano Vargas**.  
*Todos los derechos reservados.*
