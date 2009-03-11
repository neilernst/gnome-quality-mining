import csv

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
        
        
gnome_dates = '/Users/nernst/Documents/projects/msr/yearweek.csv'
ev_eff = '/Users/nernst/Documents/projects/msr/evolution-efficiency-week.csv'
ev_usable = '/Users/nernst/Documents/projects/msr/evolution-usability-week.csv'
naut_eff = '/Users/nernst/Documents/projects/msr/nautilus-efficiency-week.csv'
naut_usable = '/Users/nernst/Documents/projects/msr/nautilus-usability-week.csv'

reader = csv.reader(open(gnome_dates, 'rb'))
gnome_dates_list = [int(x[0]) for x in reader]
gnome_dates_dict = dict.fromkeys(gnome_dates_list,[])

dr = csv.reader(open('/Users/nernst/Documents/projects/msr/dates-releases.csv', 'rb'))
release_map = gnome_dates_dict.copy() #shallow copy
releases = [x for x in dr]
for release in releases:
    release_map[int(release[1])] = DateReleaseObj(release)
# print release_map.pop(199941).get_release_name()
    
#this is a bin for dates of events AFTER that particular date but prior to the next event   
reader = csv.reader(open(ev_eff, 'rb'))
ev_eff_list = [x for x in reader] # a list of lists of format [yearweeknum, occur_count

tmp = gnome_dates_dict.keys()
tmp.sort() #in place sort
for lst in ev_eff_list:
    for key in tmp:
        #find the key with the correct index
        if int(lst[0]) > key:
            index = key
    #stick the list in the bucket
    gnome_dates_dict[index] = gnome_dates_dict[index] + [lst]

#repeat for each iteration

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
                dates.append(lst[0])
                values.append(lst[1])
            if len(values) > 3: #don't bother with those smaller than 4, not significant
                pass
            #TODO tomorrow, add the numpy code for generating the stats.

            
