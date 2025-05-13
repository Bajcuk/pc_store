from PySide6.QtCore import QFile, QTextStream

def load_styles(widget):
    style_file = QFile("styles.css")
    if style_file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(style_file)
        widget.setStyleSheet(stream.readAll())
        style_file.close()