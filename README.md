# Conversor de TXT a Excel

Esta aplicación convierte archivos `.txt` a formato Excel de manera sencilla. Permite seleccionar un archivo `.txt` y definir un delimitador para separar las celdas en el archivo Excel resultante.

## Requisitos

- Python 3.x
- Dependencias: [pandas](https://pandas.pydata.org/), [openpyxl](https://openpyxl.readthedocs.io/)

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/tuusuario/conversor-txt-a-excel.git
    ```
2. Navega al directorio del proyecto:
    ```bash
    cd conversor-txt-a-excel
    ```
3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. **Abre la aplicación**:
    - Al ejecutar el programa, se abrirá una ventana donde podrás seleccionar un archivo `.txt` para convertir.

    ![Pantalla de inicio](images/screen1.png)

2. **Selecciona el archivo TXT**:
    - Se abrirá una ventana para que elijas el archivo `.txt` que deseas convertir.

    ![Seleccionar archivo](images/screen2.png)

3. **Elige el delimitador**:
    - Antes de la conversión, selecciona el delimitador. Este es el carácter que se utilizará para separar las celdas en el archivo Excel (por ejemplo, coma, punto y coma, tabulación, etc.).

    ![Elegir delimitador](images/screen3.png)

4. **Conversión**:
    - Después de seleccionar el delimitador, la aplicación convertirá el archivo `.txt` a un archivo Excel. El archivo resultante se podrá guardar en el formato `.xlsx`.

    ![Conversión realizada](images/screen4.png)

