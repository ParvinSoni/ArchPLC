#                                             
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
import time

cwd = os.getcwd()
sys.path.append(cwd)
# sys.path.append('C:\\Users\\aalsahee\\python_physical_model\\Saudi\\trace\\Traces\\qtm\\src\\')

from apriori_solver.onefile import *
from database import *
from graphicalInterface import *
from geneticAlgorithm.GeneticAlgo import *

def current_milli_time():
    return round(time.time() * 1000)

class OptimizerGeneticAlgo(RuleOptimizer):

    #GeneticAlgo extends EvaluationBaseAlgorithm

    # Tableaux r�pertoriant l'�volution de la qualit� d'une r�gle au fur et � mesure de son optimisation :

    # METTRE CETTE VARIABLE A VRAI POUR AFFICHER UN GRAPHE D'EVOLUTION DE LA QUALITE APRES L'OPTIMISATION D'UNE REGLE :
    m_bAfficherGrapheQualite = False

    m_bSortirQualite = True

    m_iRules =0

    def __init__(self):
        self.m_algoGenetique = None
        self.m_parametresReglesQuantitatives = None
        self.m_parametresAlgo = None
        self.m_tQualiteMoyenne = None
        self.m_tQualiteMin = None
        self.m_tQualiteMax = None
        self.__m_iNombreEtapesCalculRegle = 0

        self.m_algoGenetique = None



    # Outrepassement de la fonction de sp�cification du contexte :
    def DefinirContexteResolution(self, contexteResolution):
        super().DefinirContexteResolution(contexteResolution)

        if self.m_contexteResolution is None:
            self.m_algoGenetique = None
            return

        self.m_parametresReglesQuantitatives = self.m_contexteResolution.m_parametresReglesQuantitatives
        self.m_parametresAlgo = self.m_contexteResolution.m_parametresTechAlgoGenetique
        self.m_algoGenetique = GeneticAlgo(self.m_parametresAlgo.m_iTaillePopulation, self.m_contexteResolution.m_gestionnaireBD)
        self.m_algoGenetique.SpecifierParametresStatistiques(self.m_parametresReglesQuantitatives.m_fMinSupp, self.m_parametresReglesQuantitatives.m_fMinConf, self.m_parametresReglesQuantitatives.m_fMinSuppDisjonctions)
        self.m_algoGenetique.SpecifierParametresGenetiques(self.m_parametresAlgo.m_fPourcentageCroisement, self.m_parametresAlgo.m_fPourcentageMutation)


        m_iRules=0

        if OptimizerGeneticAlgo.m_bAfficherGrapheQualite or OptimizerGeneticAlgo.m_bSortirQualite:
            self.__m_iNombreEtapesCalculRegle = self.m_parametresAlgo.m_iNombreGenerations
            self.m_tQualiteMoyenne = [0 for _ in range(self.__m_iNombreEtapesCalculRegle)]
            self.m_tQualiteMin = [0 for _ in range(self.__m_iNombreEtapesCalculRegle)]
            self.m_tQualiteMax = [0 for _ in range(self.__m_iNombreEtapesCalculRegle)]





    #    *Optimize Rule Association
    #     * @param regle the Association rule
    #     * @param index the index of the n association rules
    #     
    def OptimiseRegle(self, regle, i):
        currentTime = current_milli_time()
        iNombreItemsQuantitatifs = 0
        iIndiceEvolution = 0
        bRegleEstSolide = False
        meilleureRegle = [None for _ in range(self.m_parametresAlgo.m_iNombreGenerations)]

        if (self.m_algoGenetique is None) or (regle is None):
            return False

        iNombreItemsQuantitatifs = regle.CompterItemsGaucheSelonType(Item.ITEM_TYPE_QUANTITATIF) + regle.CompterItemsDroiteSelonType(Item.ITEM_TYPE_QUANTITATIF)

        # If the rule has uniquely qualitative, no need to optimize:
        if iNombreItemsQuantitatifs <= 0:

            regle.EvaluerSiQualitative(self.m_contexteResolution)

            return ((regle.m_fSupport >= self.m_parametresReglesQuantitatives.m_fMinSupp) and (regle.m_fConfiance >= self.m_parametresReglesQuantitatives.m_fMinConf))



        # Calcul de la r�gle optimis�e, sur le sch�ma courant :

        # Indicate algorithm genetic the template of the rule to optimize :
        self.m_algoGenetique.SpecifierSchemaRegle(regle)
        self.m_algoGenetique.GenererReglesPotentiellesInitiales()

        condition = True
        while condition:
            iIndiceEvolution = 0
            while iIndiceEvolution < self.m_parametresAlgo.m_iNombreGenerations:
                self.m_algoGenetique.Evoluer()

                if OptimizerGeneticAlgo.m_bAfficherGrapheQualite or OptimizerGeneticAlgo.m_bSortirQualite:
                    self.m_tQualiteMoyenne[iIndiceEvolution] = self.m_algoGenetique.CalculerQualiteMoyenne()
                    self.m_tQualiteMin[iIndiceEvolution] = self.m_algoGenetique.ObtenirPireQualiteCourante()
                    self.m_tQualiteMax[iIndiceEvolution] = self.m_algoGenetique.ObtenirMeilleureQualiteCourante()
                iIndiceEvolution += 1
            condition = self.m_algoGenetique.InitierNouvellePasse()

        #obtain the best rule

        meilleureRegle[i] = self.m_algoGenetique.ObtenirMeilleureRegle(i)

        #if the rule is not null and have enough support and confidence, copy it to rule
        if meilleureRegle[i] is not None:
            bRegleEstSolide = ((meilleureRegle[i].m_fSupport >= self.m_parametresReglesQuantitatives.m_fMinSupp) and (meilleureRegle[i].m_fConfiance >= self.m_parametresReglesQuantitatives.m_fMinConf))
            if bRegleEstSolide:
                regle.CopierRegleAssociation(meilleureRegle[i])
        else:
            bRegleEstSolide = False


        if OptimizerGeneticAlgo.m_bAfficherGrapheQualite:
            fenetreDetailsRegle = None
            fenetreDetailsRegle = DialogGraphQuality(self.m_contexteResolution.m_fenetreProprietaire, True, self.m_contexteResolution)
            fenetreDetailsRegle.SpecifierQualitesMoyennes(self.m_tQualiteMoyenne)
            fenetreDetailsRegle.SpecifierQualitesMax(self.m_tQualiteMax)
            fenetreDetailsRegle.SpecifierQualitesMin(self.m_tQualiteMin)
            fenetreDetailsRegle.ConstruireGraphe()
            fenetreDetailsRegle.show()

        # Generates error; comment out for now
        #        if ( m_bSortirQualite){
        #            File outputFile = new File("E:\\temp\\rules\\rule"+Integer.toString(m_iRules++)+".txt")
        #            outputFile.delete()
        #            System.out.println(outputFile)
        #            try{
        #                FileWriter out = new FileWriter(outputFile)
        #                System.out.println(out)
        #                out.write("Algo genetiques\n")
        #                out.write("\n - Nb quantitatifs :"+ Integer.toString(iNombreItemsQuantitatifs)+"\n")
        #                out.write("\n - Generations :"+ Integer.toString( (int)(m_parametresAlgo.m_iNombreGenerations))+"\n")
        #                out.write("\n - Population :"+ Integer.toString( (int)(m_parametresAlgo.m_iTaillePopulation))+"\n")
        #                out.write("\n - Taux Croisement :"+ Float.toString((float)(m_parametresAlgo.m_fPourcentageCroisement))+"\n")
        #                out.write("\n - Taux Mutation :"+ Float.toString((m_parametresAlgo.m_fPourcentageMutation))+"\n")
        #                out.write("\n - MinSupp :"+ Float.toString((m_parametresReglesQuantitatives.m_fMinSupp))+"\n")
        #                out.write("\n - MinConf :"+ Float.toString((m_parametresReglesQuantitatives.m_fMinConf))+"\n")
        #                out.write("\n - Temps (s) :"+ Integer.toString( (int)(System.currentTimeMillis()-currentTime))+"\n")
        #                out.write("\n - Temps (ms):"+ Integer.toString( (int)(System.currentTimeMillis()-currentTime)/1000)+"\n")
        #                out.write("\n")
        #                out.write("\n - Regle :\n\n")
        #                out.write("---------------------------------------------------------------\n")
        #                out.write(regle.toString())
        #                out.write("\n---------------------------------------------------------------\n")
        #                out.write("\n")
        #                out.write("generation,moy,max,min\n")
        #                for (int j=0; j<m_tQualiteMoyenne.length; j++){
        #                    out.write(Integer.toString(j))
        #                    out.write(',')
        #                    out.write(Float.toString(m_tQualiteMoyenne[j]))
        #                    out.write(',')
        #                    out.write(Float.toString(m_tQualiteMax[j]))
        #                    out.write(',')
        #                    out.write(Float.toString(m_tQualiteMin[j]))
        #                    out.write("\n")
        #                }
        #                out.close()
        #            } catch(java.io.IOException e){
        #                e.printStackTrace()
        #            }
        #        } 



        return bRegleEstSolide

