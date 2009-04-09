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
        
gnome_dates = '/Users/nernst/Documents/projects/msr/data/yearweek.csv'
release_dates = '/Users/nernst/Documents/projects/msr/data/dates-releases.csv'
pickle_dir = '/Users/nernst/Documents/current-papers/icsm/data/pickles/'        

# ev_eff = '/Users/nernst/Documents/projects/msr/data/evolution-efficiency-week.csv'
# ev_usable = '/Users/nernst/Documents/projects/msr/data/evolution-usability-week.csv'
# naut_eff = '/Users/nernst/Documents/projects/msr/data/nautilus-efficiency-week.csv'
# naut_usable = '/Users/nernst/Documents/projects/msr/data/nautilus-usability-week.csv'

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
    for product in t.get_products():
        pickle_file = pickle_dir + product+'-'+ signified + '.pcl'
        data = pickle.load(open(pickle_file, 'rb'))
        # parse into ...
#this is a bin for dates of events AFTER that particular date but prior to the next event   

#ev_eff_list = [x for x in reader] # a list of lists of format [yearweeknum, occur_count]

        tmp = gnome_dates_dict.keys()
        tmp.sort() #in place sort
        for lst in data:#ev_eff_list:
            for key in tmp:
                #find the key with the correct index
                if int(lst[0]) > key:
                    index = key
            #stick the list in the bucket
            gnome_dates_dict[index] = gnome_dates_dict[index] + [lst]

#repeat for each iteration

#load the overall event data, per yearweek
# n_all = csv.reader(open('/Users/nernst/Documents/projects/msr/data/nautilus-totals.csv', 'rb'))
# e_all = csv.reader(open('/Users/nernst/Documents/projects/msr/data/evolution-all.csv', 'rb'))
# e_all_dict = dict([x for x in e_all])
# n_all_dict = dict([x for x in n_all])

#figure out average occurrences per quality
#parse the project numbers to find out the average total weekly events
#parse the quality-project numbers, adding in null weeks.

#generate arrays of data for each and plot the trends.
# a release window is the weeks following a release but before the next release. We want to see what effects there are.
# for each window, measure the slope and r2 values and store them
tmp2 = gnome_dates_dict.keys()
tmp2.sort()
for window in tmp2:
        dates = []
        values = []
        if gnome_dates_dict[window] != []:
            # print 'Key is ' + str(window) + ' values are: ' + str(gnome_dates_dict[window])
            for lst in gnome_dates_dict[window]:
                # normalize
                normal = float(lst[1]) / float(e_all_dict[lst[0]]) * 1000
                #print normal
                dates.append(lst[0])
                #values.append(lst[1])
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
                #print len(values)
                print release_map[window].get_release_name() + ', '+ str(r2) + ', ' + str(slope) + ', ' + str(len(values))

            
