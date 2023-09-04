import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QGuiApplication

app = QApplication(sys.argv)

# Get the primary screen
screen = QGuiApplication.primaryScreen()

# Get the screen's pixel density in pixels per centimeter
pixels_per_cm = screen.physicalDotsPerInch() / 2.54

print("Pixels per centimeter:", pixels_per_cm)

# Don't forget to clean up when done
app.quit()

