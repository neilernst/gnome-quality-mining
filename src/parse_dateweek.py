import csv
import numpy as np
import pickle
from names import Taxonomy

class DateReleaseObj():
    # self.date = ''
    # self.release_name = ''
    # self.dateweek = 0
     
    def __init__(self, dr):
         """ Init the data structure"""
         self.date, self.dateweek, self.release_name = dr  
         
    def get_release_name(self): 
        return self.release_name
    def get_dateweek(self):
        return self.dateweek
    def get_date(self):
        return self.date 
    def __str__(self):
        return 'hello' #str(self.date, self.dateweek, self.release_name)

def generate_compare(product, signified):
    """Finds the average occurrences over project lifespan"""
    pickle_dir = '/Users/nernst/Documents/papers/current-papers/refsq/data/pickles/ext/'        
    pickle_file = pickle_dir + product+'-'+ signified + '.pcl'
    significance_threshold = 3 # number of events below which we don't consider this important.
    data = pickle.load(open(pickle_file, 'rb'))
    avg_norm = 0.0
    avg_abs = 0.0
    total_weeks = len(data)
    for lst in data:
        if (lst[2] <= significance_threshold and lst[1] > 500) or (lst[2] == 0):
            #print 'excluded week ' + str(lst[0]) + 'insufficient events'
            total_weeks -= 1
        else:
            avg_norm = avg_norm + lst[1] # normalized
            avg_abs = avg_abs + lst[2] # absolute numbers
    # print ' & \\textbf{' + str(round(avg_norm/total_weeks, 2)) + '} & ' + str(round(avg_abs/total_weeks, 2)) + ' & ' + str(total_weeks)
    print ', ' + str(round(avg_norm/total_weeks, 2)) + ', ' + str(round(avg_abs/total_weeks, 2)) + ', ' + str(total_weeks) + ', ' + str(len(data))
    
def find_window(product, signified):
    """generates the r2, slope values for this product over the Gnome release data"""
    pickle_dir = '/Users/nernst/Documents/papers/current-papers/refsq/data/pickles/ext/'        
    pickle_file = pickle_dir + product+'-'+ signified + '.pcl'
    data = pickle.load(open(pickle_file, 'rb'))
    #print product, signified, len(data)
    tmp = []
    index = None
    tmp = gnome_dates_dict.keys()
    tmp.sort() #in place sort
    for lst in data:#ev_eff_list:
        for key in tmp:
        #find the key with the correct index
            if lst[0] > key:
                index = key
            #stick the list in the bucket
        gnome_dates_dict[index] = gnome_dates_dict[index] + [lst]

#generate arrays of data for each and plot the trends.
# a release window is the weeks following a release but before the next release. We want to see what effects there are.
# for each window, measure the slope and r2 values and store them
    tmp2 = []
    tmp2 = gnome_dates_dict.keys()
    tmp2.sort()
    for window in tmp2:
            dates = []
            values = []
            if gnome_dates_dict[window] != []:
                #print 'Key is ' + str(window) + ' values are: ' + str(gnome_dates_dict[window])
                for tup in gnome_dates_dict[window]:
                    # normalize
                    normal =  tup[1] 
                    dates.append(tup[0])
                    #values.append(lst[1]) #non normalized
                    values.append(normal)
                if len(values) > 3: #don't bother with those smaller than 4, not significant
                    new_x = []
                    for i in range(len(dates)):
                       new_x.append(i)
                    int_corr = np.corrcoef(new_x, values)
                    corr = int_corr[0][1] #note, not r^2 value
                    r2 = corr*corr
                    y = [float(x) for x in values]
                    z = np.polyfit(new_x, y, 1) # a 1-degree regression
                    slope, intercept = z
                    slope = round(slope,2)
                    r2 = round(r2, 2)
                    #print product, signified, len(values)
                    if release_map[window].get_release_name() == '2.8' or release_map[window].get_release_name() == '2.20,': # ' & ' + str(len(values)) +
                        # print '& &' + release_map[window].get_release_name() +  '& '+ str(r2) + ' & ' + str(slope) + '\\\\'
                        print release_map[window].get_release_name() +  ', '+ str(r2) + ', ' + str(slope) + ', ' + str(len(values))#+ '\\\\'

def main():
    gnome_dates = '/Users/nernst/Documents/projects/msr/data/yearweek.csv'
    release_dates = '/Users/nernst/Documents/projects/msr/data/dates-releases.csv'
    global gnome_dates_dict
    global release_map
    
    reader = csv.reader(open(gnome_dates, 'rb'))
    gnome_dates_list = [int(x[0]) for x in reader]
    gnome_dates_dict = dict.fromkeys(gnome_dates_list,[])
    #open the list of Gnome releases
    dr = csv.reader(open(release_dates, 'rb'))
    release_map = gnome_dates_dict.copy() #shallow copy
    releases = [x for x in dr]
    for release in releases:
        release_map[int(release[1])] = DateReleaseObj(release)
    t = Taxonomy()     
    for signified in t.get_signified(): # e.g. usability, performance, etc
        # print signified + ' & ',
        print signified #+ ' , ',

        for product in t.get_products():
            # print '& ' + product,
            print product + ',',
            gnome_dates_dict = dict.fromkeys(gnome_dates_list,[])
            find_window(product, signified)
            #generate_compare(product, signified)
            # print '\\hline'
            #pass
    #find_window("Nautilus", "Usability")

if __name__ == '__main__':
    main()