"""
auteur : ...
nom du programme : générateur de qr code
description : programme permettant de generer un qr code contenat le nom et le matricule renseigné
date : 07/02/2021
"""

#importation
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys,qrcode



#classe principale
class interface(QDialog):
    def __init__(self):
        super(interface, self).__init__()
        loadUi("interface.ui", self) #charge notre interface

        #cacher le label d'erreur et le label de succes
        self.error.hide()
        self.txt.hide()
        
        #afficher une image de qr code dans le label qr
        pixmap=QtGui.QPixmap("img/qr.png")
        self.qr.setStyleSheet("border-image: url(img/qr.png);")
        
        
        #lancer la fonction de generation de qr code lorsque le texte change dans le champ name ou/et le champ matricule
        self.name.textChanged.connect(self.qr_code)
        self.id_card.textChanged.connect(self.qr_code)

        
    def qr_code(self):
        """
           fonction qui genère un qr code en temps réel en fonction du matricule et du nom renseigné
        """
        name = self.name.text() #on recupere la valeur du champ name
        matricule = self.id_card.text() #on recupere la valeur du champ matricule
        
        if(len(matricule)>0 and len(name)>0): #verifie si les 2 champs ne sont pas vide
            
            if(len(matricule)>=4): #verifie si le matricule a la longueur recommandé

                #creation du qr code
                qr = qrcode.QRCode(     
                    version=1,     
                    error_correction=qrcode.constants.ERROR_CORRECT_H,     
                    box_size=10,     
                    border=4, )
                qr.add_data("Nom : "+name+"\nMatricule : "+matricule)
                qr.make(fit=True)
        
                self.error.hide()

                #controle pour generé l'image du qr code avec des couleur differente en fonction du matricule
                if matricule[0] and matricule[1] and matricule[2] == "1":
                    img = qr.make_image(fill_color="blue", back_color="white")
                    
                elif matricule[0] == "1" and matricule[1]=="2" and matricule[2] == "3": 
                    img = qr.make_image(fill_color="red", back_color="white")
                    
                else :
                   img = qr.make_image(fill_color="black", back_color="white")

                save_dir = "img/"+name+".png" # lien ou sera stocké notre image qr generé
                img.save(save_dir) #enregistrement de l'image du qr code
                
                #affichage de l'image generé dans le label qr
                pixmap=QtGui.QPixmap(save_dir) 
                self.qr.setStyleSheet("border-image: url("+save_dir+");")
                
                self.txt.show()
            else :
                self.error.show()
                self.txt.hide()
        
if __name__ == "__main__":
    #lancer du programme
    app = QApplication(sys.argv)
    mainwindow = interface()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedHeight(330)
    widget.setFixedWidth(527)
    widget.show()
app.exec_()
