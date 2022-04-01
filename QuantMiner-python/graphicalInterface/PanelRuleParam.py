﻿#                                             
# *Copyright 2007, 2011 CCLS Columbia University (USA), LIFO University of Orl��ans (France), BRGM (France)
# *
# *Authors: Cyril Nortet, Xiangrong Kong, Ansaf Salleb-Aouissi, Christel Vrain, Daniel Cassard
# *
# *This file is part of QuantMiner.
# *
# *QuantMiner is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
# *
# *QuantMiner is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# *
# *You should have received a copy of the GNU General Public License along with QuantMiner.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import os
cwd = os.getcwd()
sys.path.append(cwd)

from apriori_solver.onefile import *
from tools import *
from graphicalInterface.PanelBaseParam import *



class PanelRuleParam(PanelBaseParam):

    #* Creates new form PanneauParamRegles 
    def __init__(self, contexteResolution):
        self.__jButtonDefautConfiance = None
        self.__jButtonDefautSupport = None
        self.__jLabelConfiance = None
        self.__jLabelSupport = None
        self.__jTextFieldConfiance = None
        self.__jTextFieldSupport = None

        super().__init__(contexteResolution)

        iconeRetourDefaut = None

        self.__initComponents()

        # Ic�nes sur les boutons :
        # iconeRetourDefaut = ImageIcon(ENV.REPERTOIRE_RESSOURCES + "retour_defaut.jpg")
        # self.__jButtonDefautSupport.setIcon(iconeRetourDefaut)
        # self.__jButtonDefautConfiance.setIcon(iconeRetourDefaut)

        if self.m_contexteResolution is None:
            return

        # Initialisation du contenu des champs :
        # self.__jTextFieldSupport.setText(ResolutionContext.EcrirePourcentage(self.m_contexteResolution.m_parametresRegles.m_fMinSupp, 3, False))
        # self.__jTextFieldConfiance.setText(ResolutionContext.EcrirePourcentage(self.m_contexteResolution.m_parametresRegles.m_fMinConf, 3, False))

    #    * This method is called from within the constructor to
    #     * initialize the form.
    #     * WARNING: Do NOT modify this code. The content of this method is
    #     * always regenerated by the Form Editor.
    #     
    def __initComponents(self):
        self.__jTextFieldSupport = None
        self.__jLabelSupport = None
        self.__jLabelConfiance = None
        self.__jTextFieldConfiance = None
        self.__jButtonDefautSupport = None
        self.__jButtonDefautConfiance = None

        # setLayout(None)

        # setPreferredSize(java.awt.Dimension(300, 90))
        # self.__jTextFieldSupport.setInputVerifier(ToolsInterface.VerifieurTextFieldIntervalleFloat(0.0, 100.0))
        # add(self.__jTextFieldSupport)
        # self.__jTextFieldSupport.setBounds(160, 20, 100, 20)

        # self.__jLabelSupport.setText("Support threshold (%) :")
        # add(self.__jLabelSupport)
        # self.__jLabelSupport.setBounds(10, 20, 140, 20)

        # self.__jLabelConfiance.setText("Confidence threshold (%) : ")
        # add(self.__jLabelConfiance)
        # self.__jLabelConfiance.setBounds(10, 50, 150, 16)

        # self.__jTextFieldConfiance.setInputVerifier(ToolsInterface.VerifieurTextFieldIntervalleFloat(0.0, 100.0))
        # add(self.__jTextFieldConfiance)
        # self.__jTextFieldConfiance.setBounds(160, 50, 100, 20)

        # self.__jButtonDefautSupport.setBackground(java.awt.Color(255, 255, 255))
        # self.__jButtonDefautSupport.addActionListener(ActionListenerAnonymousInnerClass(self))

        # add(self.__jButtonDefautSupport)
        # self.__jButtonDefautSupport.setBounds(270, 20, 20, 20)

        # self.__jButtonDefautConfiance.setBackground(java.awt.Color(255, 255, 255))
        # self.__jButtonDefautConfiance.addActionListener(ActionListenerAnonymousInnerClass2(self))

        # add(self.__jButtonDefautConfiance)
        # self.__jButtonDefautConfiance.setBounds(270, 50, 20, 20)
 #GEN-END:initComponents

    class ActionListenerAnonymousInnerClass:

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__jButtonDefautSupportActionPerformed(evt)

    class ActionListenerAnonymousInnerClass2:

        def __init__(self, outerInstance):
            self.__outerInstance = outerInstance

        def actionPerformed(self, evt):
            outerInstance.__jButtonDefautConfianceActionPerformed(evt)

    def __jButtonDefautConfianceActionPerformed(self, evt):
        self.__jTextFieldConfiance.setText(ResolutionContext.EcrirePourcentage(StandardParameters.DEFAUT_MINCONF, 3, False)) #GEN-LAST:event_jButtonDefautConfianceActionPerformed

    def __jButtonDefautSupportActionPerformed(self, evt):
        self.__jTextFieldSupport.setText(ResolutionContext.EcrirePourcentage(StandardParameters.DEFAUT_MINSUPP, 3, False)) #GEN-LAST:event_jButtonDefautSupportActionPerformed


    # Variables declaration - do not modify//GEN-BEGIN:variables
    # End of variables declaration//GEN-END:variables




    def EnregistrerParametres(self):

        parametresRegles = None
        fMinSupp = 0.0
        fMinConf = 0.0

        parametresRegles = self.m_contexteResolution.m_parametresRegles
        if parametresRegles is None:
            return True

        # M�morisation des param�tres :

        try:
            fMinSupp = float((float(self.__jTextFieldSupport.getText()) / 100.0))
            parametresRegles.m_fMinSupp = fMinSupp
        except NumberFormatException as e:
            return False

        try:
            fMinConf = float((float(self.__jTextFieldConfiance.getText()) / 100.0))
            parametresRegles.m_fMinConf = fMinConf
        except NumberFormatException as e:
            return False

        return True

