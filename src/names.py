class Taxonomy():
    """ class to store lists of various terms of interest. Each element/term in the list will be queried once."""
    #TODO account for misspelinges 

    usability_spell = ['usbility', 'useability',]
    usability_syn = ['usability', 'serviceability', 'serviceableness', 'usableness', 'useableness'] #synonyms
    usability_hyper = ['utility', 'usefulness'] #hypernyms
    usability_deriv = ['serviceable', 'usable', 'useable'] # derived forms
    usability_mccall = ['flexibility', 'interface'] #mccall defns
    usability_meronym = ['Learnability', 'Understandability', 'Operability'] #as defined in iso9126
    usability_user = ['screen', 'user', 'friendly', 'convention', 'human', 'default', \
                        'click', 'guidelines', 'dialog', 'ugly', 'icons', 'ui', 'focus', \
                        'feature', 'standard', 'convention', 'configure', 'menu', 'accessibility', 'gui'] #from mailing list
    usability =  usability_mccall + usability_user + usability_syn + usability_hyper + usability_deriv + usability_meronym #+ usability_spell
    
    functionality_spell = []
    functionality_mccall = ['accuracy', 'correctness']
    functionality_user = ['vulnerability', 'secure', 'accurate', 'vulnerability', 'vulnerable', 'trustworthy', 'malicious', \
                            'policy', '"buffer overflow"', 'secured', 'certificate', 'exploit', 'compliant' ]
    functionality_syn = ['functionality']
    functionality_hyper = ['practicality']
    functionality_deriv = ['functional']
    functionality_meronym = ['Suitability', 'Interoperability', 'Accuracy', 'Compliance', 'Security'] #as defined in iso9126
    functionality = functionality_mccall + functionality_user + functionality_syn + functionality_hyper + functionality_deriv + functionality_meronym #+ _spell
       
    reliability_spell = []
    reliability_syn = ['dependability', 'dependableness', 'reliability', 'reliableness']
    reliability_hyper = ['responsibility', 'responsibleness']
    reliability_mccall = ['integrity', 'resilience']
    reliability_deriv = ['dependable', 'reliable']
    reliability_user = ['failure', 'error', 'redundancy', 'fails', 'bug', 'crash', 'stable', 'stability']
    reliability_meronym = ['Maturity', 'Recoverability', '"Fault Tolerance"'] #as defined in iso9126
    reliability = reliability_user + reliability_mccall + reliability_syn + reliability_hyper + reliability_deriv + reliability_meronym #+ _spell
    
    maintainability_spell = []
    maintainability_syn = ['maintainable']
    maintainability_hyper = []
    maintainability_user = ['modular', 'decentralized', 'encapsulation', 'dependency', 'interdependent' ]
    maintainability_mccall = ['understandability', 'modifiability', 'modularity']
    maintainability_deriv = ['maintain']
    maintainability_meronym = ['Stability', 'Analyzability', 'Changeability', 'Testability'] #as defined in iso9126
    maintainability = maintainability_user + maintainability_mccall + maintainability_syn + maintainability_hyper + maintainability_deriv + maintainability_meronym #+ _spell
    
    portability_spell = []
    portability_mccall = ['transferability', 'interoperability', 'documentation']
    portability_user = ['internationalization', 'i18n', 'localization', 'l10n', 'standardized', 'migration', 'specification']
    portability_syn = ['portability']
    portability_hyper = ['movability', 'movableness']
    portability_deriv = ['portable']
    portability_meronym = ['Installability', 'Replaceability', 'Adaptability', 'Conformance'] #as defined in iso9126
    portability = portability_mccall + portability_user + portability_syn + portability_hyper + portability_deriv + portability_meronym #+ _spell
    
    efficiency_spell = []
    efficiency_user = ['optimization', 'fast', 'slow', 'faster', 'slower', 'penalty', 'factor', 'sluggish', 'optimize', 'profiled'] #'"moore\'s law"'
    efficiency_syn = ['performance', 'efficiency'] # added from personal experience...
    efficiency_hyper = [] #['ratio']
    efficiency_deriv = ['efficient']
    efficiency_meronym = ['"time behaviour"', '"resource behaviour"'] #as defined in iso9126
    efficiency =  efficiency_user + efficiency_syn + efficiency_hyper + efficiency_deriv + efficiency_meronym #+ _spell
    #efficiency = time/resource behaviour == performance
    
    global signifier_dict
    signifier_dict = {'Efficiency': efficiency, 'Portability': portability, 'Maintainability': maintainability, 'Reliability': reliability, 'Functionality': functionality, 'Usability': usability}
    
    def get_signifiers(self, key):
        return signifier_dict.get(key)
    
    def get_signified(self):
        return signifier_dict.keys()
        
    def get_products(self):
        return ['Evolution', 'Nautilus', 'Deskbar', 'Metacity', 'Ekiga', 'Totem', 'Evince', 'Empathy']