import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget, QComboBox, QMessageBox, QLineEdit, QHBoxLayout
from openpyxl import Workbook
import csv
import configparser

class TXTtoExcelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = self.load_config()

        # Configuración de la ventana principal
        self.setWindowTitle("Convertir TXT a Excel")
        self.setGeometry(100, 100, int(self.config['width']), int(self.config['height']))

        # Diseño y elementos de la interfaz
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Botón para seleccionar archivo
        self.select_button = QPushButton("Seleccionar archivo TXT")
        self.select_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.select_button)

        # Etiqueta para mostrar el archivo seleccionado
        self.file_label = QLabel("Ningún archivo seleccionado")
        self.layout.addWidget(self.file_label)

        # Menú desplegable para seleccionar el delimitador
        self.delimiter_label = QLabel("Selecciona el delimitador:")
        self.layout.addWidget(self.delimiter_label)
        self.delimiter_combo = QComboBox()
        self.delimiter_combo.addItems([";", ",", ".", "\t"])  # Se puede agregar '\t' para el tabulador
        self.layout.addWidget(self.delimiter_combo)

        # Botón de configuración
        self.settings_button = QPushButton("Configuración")
        self.settings_button.clicked.connect(self.open_settings_window)
        self.layout.addWidget(self.settings_button)

        # Botón de ayuda
        self.help_button = QPushButton("Ayuda")
        self.help_button.clicked.connect(self.show_help)
        self.layout.addWidget(self.help_button)

    def load_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        delimiter = config.get('Settings', 'delimiter', fallback='\t')
        if len(delimiter) != 1:
            delimiter = '\t'
        return {
            'delimiter': delimiter,
            'encoding': config.get('Settings', 'encoding', fallback='utf-8'),
            'width': config.get('Settings', 'width', fallback='400'),
            'height': config.get('Settings', 'height', fallback='300')
        }

    def save_config(self):
        config = configparser.ConfigParser()
        config['Settings'] = {
            'delimiter': self.config['delimiter'],
            'encoding': self.config['encoding'],
            'width': self.config['width'],
            'height': self.config['height']
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo TXT", "", "Archivos TXT (*.txt)")
        if file_path:
            self.file_label.setText(f"Archivo seleccionado: {file_path}")
            self.convert_to_excel(file_path)

    def convert_to_excel(self, txt_file_path):
        try:
            wb = Workbook()
            ws = wb.active

            # Obtener el delimitador seleccionado por el usuario
            delimiter = self.delimiter_combo.currentText()
            if len(delimiter) != 1:
                QMessageBox.critical(self, "Error", "El delimitador debe ser un solo carácter.")
                return

            with open(txt_file_path, newline='', encoding=self.config['encoding']) as txt_file:
                reader = csv.reader(txt_file, delimiter=delimiter)
                for row in reader:
                    ws.append(row)

            excel_file_path = txt_file_path.rsplit('.', 1)[0] + '.xlsx'
            wb.save(excel_file_path)
            QMessageBox.information(self, "Éxito", f"Archivo convertido y guardado en: {excel_file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo convertir el archivo: {e}")

    def open_settings_window(self):
        self.settings_window = QWidget()
        self.settings_window.setWindowTitle("Configuración")
        self.settings_window.setGeometry(150, 150, 300, 200)
        layout = QVBoxLayout()

        width_label = QLabel("Ancho de la ventana:")
        layout.addWidget(width_label)
        self.width_entry = QLineEdit(self.config['width'])
        layout.addWidget(self.width_entry)

        height_label = QLabel("Alto de la ventana:")
        layout.addWidget(height_label)
        self.height_entry = QLineEdit(self.config['height'])
        layout.addWidget(self.height_entry)

        delimiter_label = QLabel("Delimitador:")
        layout.addWidget(delimiter_label)
        self.delimiter_entry_settings = QComboBox()
        self.delimiter_entry_settings.addItems([";", ",", ".", "\t"])  # Igual que en la ventana principal
        layout.addWidget(self.delimiter_entry_settings)

        encoding_label = QLabel("Codificación:")
        layout.addWidget(encoding_label)
        self.encoding_entry = QLineEdit(self.config['encoding'])
        layout.addWidget(self.encoding_entry)

        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        self.settings_window.setLayout(layout)
        self.settings_window.show()

    def save_settings(self):
        try:
            int(self.width_entry.text())
            int(self.height_entry.text())
            self.config['width'] = self.width_entry.text()
            self.config['height'] = self.height_entry.text()
            self.config['delimiter'] = self.delimiter_entry_settings.currentText()
            self.config['encoding'] = self.encoding_entry.text()
            self.save_config()
            self.setGeometry(100, 100, int(self.config['width']), int(self.config['height']))
            self.settings_window.close()
        except ValueError:
            QMessageBox.critical(self, "Error", "El ancho y el alto deben ser números enteros.")

    def show_help(self):
        help_message = """
        1. Haz clic en 'Seleccionar archivo TXT' para elegir un archivo .txt que quieras convertir.
        2. Escoge el delimitador que separa las columnas en el archivo (por ejemplo, ';', ',', '.' o tabulador).
        3. El archivo seleccionado se convertirá automáticamente a un archivo Excel (.xlsx) usando el delimitador escogido.
        4. Usa la opción de 'Configuración' para cambiar la resolución de la ventana o el delimitador por defecto.
        """
        QMessageBox.information(self, "Ayuda", help_message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TXTtoExcelApp()
    window.show()
    sys.exit(app.exec_())
