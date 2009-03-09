class Taxonomy():
    """ class to store lists of various terms of interest. Each element/term in the list will be queried once."""
    #TODO account for misspelinges 

    usability_spell = ['usbility', 'useability',]
    usability_syn = ['usability', 'serviceability', 'serviceableness', 'usableness', 'useableness']
    usability_hyper = ['utility', 'usefulness']
    usability_deriv = ['serviceable', 'usable', 'useable']
    usability_meronym = ['Learnability', 'Understandability', 'Operability'] #as defined in iso9126
    usability =  usability_syn + usability_hyper + usability_deriv + usability_meronym #+ usability_spell
    
    functionality_spell = []
    functionality_syn = ['functionality']
    functionality_hyper = ['practicality']
    functionality_deriv = ['functional']
    functionality_meronym = ['Suitability', 'Interoperability', 'Accuracy', 'Compliance', 'Security'] #as defined in iso9126
    functionality =  functionality_syn + functionality_hyper + functionality_deriv + functionality_meronym #+ _spell
       
    reliability_spell = []
    reliability_syn = ['dependability', 'dependableness', 'reliability', 'reliableness']
    reliability_hyper = ['responsibility', 'responsibleness']
    reliability_deriv = ['dependable', 'reliable']
    reliability_meronym = ['Maturity', 'Recoverability', '"Fault Tolerance"'] #as defined in iso9126
    reliability =  reliability_syn + reliability_hyper + reliability_deriv + reliability_meronym #+ _spell
    
    maintainability_spell = []
    maintainability_syn = ['maintainable']
    maintainability_hyper = []
    maintainability_deriv = ['maintain']
    maintainability_meronym = ['Stability', 'Analyzability', 'Changeability', 'Testability'] #as defined in iso9126
    maintainability =  maintainability_syn + maintainability_hyper + maintainability_deriv + maintainability_meronym #+ _spell
    
    portability_spell = []
    portability_syn = ['portability']
    portability_hyper = ['movability', 'movableness']
    portability_deriv = ['portable']
    portability_meronym = ['Installability', 'Replaceability', 'Adaptability', 'Conformance'] #as defined in iso9126
    portability =  portability_syn + portability_hyper + portability_deriv + portability_meronym #+ _spell
    
    efficiency_spell = []
    efficiency_syn = ['performance', 'efficiency'] # added from personal experience...
    efficiency_hyper = ['ratio']
    efficiency_deriv = ['efficient']
    efficiency_meronym = ['"time behaviour"', '"resource behaviour"'] #as defined in iso9126
    efficiency =  efficiency_syn + efficiency_hyper + efficiency_deriv + efficiency_meronym #+ _spell
    #efficiency = time/resource behaviour == performance
    
    global signifier_dict
    signifier_dict = {'Efficiency': efficiency, 'Portability': portability, 'Maintainability': maintainability, 'Reliability': reliability, 'Functionality': functionality, 'Usability': usability}
    
    def get_signifiers(self, key):
        return signifier_dict.get(key)
    
    def get_signified(self):
        return signifier_dict.keys()
        
    def get_products(self):
        return ['Evolution', 'Nautilus', 'Deskbar', 'Metacity', 'Ekiga', 'Totem', 'Evince', 'Empathy']