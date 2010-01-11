#!/usr/bin/env python
"""
Generate a plot, based on the query results (see query_corpora.py)
Add a linear regression, Gnome release dates, and 

"""
import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.mlab as mlab
import query_corpora
from matplotlib import rcParams
matplotlib.use('PDF')
# rcParams['text.usetex']=True
# rcParams['text.latex.unicode']=True

def main(df, product, keyword, normalized=True):
    global project, signifier,fig,ax #is this evil?
    fig = plt.figure()
    significance_threshold = 3 # don't count events that are very small
    ax = fig.add_subplot(111,autoscale_on=False)
    project = product
    signifier = keyword
    years    = mdates.YearLocator()   # every year
    months   = mdates.MonthLocator(interval=3)  # every quarter
    yearsFmt = mdates.DateFormatter('%Y-%m') # want the x-axis to have ticks labelled (2008-Jan)
    plt.gca().set_autoscale_on(False) 
    bug_dates = [datetime.datetime(1997, 8, 1), datetime.datetime(1998, 3, 10), datetime.datetime(1998, 6, 7), datetime.datetime(1998, 12, 30), datetime.datetime(1999, 3, 1), datetime.datetime(1999, 10, 12), datetime.datetime(2000, 5, 25), datetime.datetime(2001, 4, 3), datetime.datetime(2002, 6, 26), datetime.datetime(2003, 2, 5), datetime.datetime(2003, 9, 11), datetime.datetime(2003, 11, 29), datetime.datetime(2004, 3, 31), datetime.datetime(2004, 9, 15), datetime.datetime(2005, 3, 9), datetime.datetime(2005, 9, 7), datetime.datetime(2006, 3, 15), datetime.datetime(2006, 9, 6), datetime.datetime(2007, 3, 14), datetime.datetime(2007, 9, 19), datetime.datetime(2008, 3, 12), datetime.datetime(2008, 9, 24), datetime.datetime(2009, 2, 4)]
    #bug_dates = [datetime.date(1997, 8, 1), datetime.date(1998, 3, 10), datetime.date(1998, 6, 7), datetime.date(1998, 12, 30), datetime.date(1999, 3, 1), datetime.date(1999, 10, 12), datetime.date(2000, 5, 25), datetime.date(2001, 4, 3), datetime.date(2002, 6, 26), datetime.date(2003, 2, 5), datetime.date(2003, 9, 11), datetime.date(2003, 11, 29), datetime.date(2004, 3, 31), datetime.date(2004, 9, 15), datetime.date(2005, 3, 9), datetime.date(2005, 9, 7), datetime.date(2006, 3, 15), datetime.date(2006, 9, 6), datetime.date(2007, 3, 14), datetime.date(2007, 9, 19), datetime.date(2008, 3, 12), datetime.date(2008, 9, 24), datetime.date(2009, 2, 4)]
    bug_descr = ['0.0', '0.13', '0.2', '0.91', '1.0.0', '1.0.53 ', '1.2', '1.4', '2', '2.2', '2.4', '2.5.0', '2.6', '2.8', '2.10', '2.12', '2.14', '2.16', '2.18', '2.20', '2.22', '2.24', '2.26b1']
    total_counts = []
    dates = []
    normal_counts = []
    for dateweek, normal, count in df:
        if count <= significance_threshold and normal > 500:
            continue
        if count == 0: 
            continue
        total_counts.append(count)
        dateweek = str(dateweek) + '-0' #200845 first day of week
        date = datetime.datetime.strptime(dateweek, '%Y%U-%w') 
        dates.append(date) 
        normal_counts.append(normal)
    
    # do we want absolute or normalized values?
    if normalized:
        counts = normal_counts
    else: 
        counts = total_counts
    min_x = 0
    for x in range(len(counts)):
        if counts[x] != 0: # find the first non-zero value and that becomes our start date (may miss some non-zero dates)
             min_x = x
             break
    counts = counts[min_x:]
    dates = dates[min_x:]
    
    #then, set the y height by the greatest value of Y + some padding.    
    #plt.clf() # clear the figure...
    occur = ax.plot(dates, counts, 'r-', label='Occurrences')#, bug_dates, art, 'go') 
        #occur = plt.scatter(dates, date_index, 'b.', label='Occurrences')
    #plot the release dates for Gnome as dashed vertical lines
    rel_lines = ax.vlines(bug_dates, 0, max(counts), color='#616D7E', linestyles='dashed', label='_nolegend_')
    
    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    datemin = min(dates)
    datemax = datetime.date(2009,5,1)

    corr, slope, intercept = add_trend(dates, counts)
    
    ax.set_xlim(datemin, datemax)
    ax.set_ylim(0, max(counts))#+2000)
    r2 = add_metadata(ax,corr)
    add_label(dates, bug_dates, counts, bug_descr)
    #ax.set_ylim(-10, 1600)
    #$plt.show()
    export()
    return r2, slope, intercept, len(counts)
    
def add_trend(x, y):
    """Add the least-squares linear regression, and corr. coeff"""
    #generate a list of integers for the dates
    new_x = []
    for i in range(len(x)):
       new_x.append(i)
    print y
    int_corr = np.corrcoef(new_x, y) # of form array([[ 1.,  0.09553632], [ 0.09553632,  1.]])
    corr = int_corr[0][1]
    z = np.polyfit(new_x, y, 1) # a 1-degree regression
    slope, intercept = z
    xr = np.polyval([slope,intercept],new_x)
    #print slope
    #p = np.poly1d(z)
                            #p(new_x)
    trend_line = ax.plot(x, xr, 'k-', label='y = {0:.2f} + {1:.2f} x '.format(intercept,slope))
    #plt.text()
    return corr, slope, intercept
    
def add_label(dates, bug_dates, counts, bug_descr):
    """ label the release lines, and add a legend. corr is the correlation coefficient"""
    
    min_date = 0
    for x in range(len(bug_dates)):
        if bug_dates[x] >= dates[0]:
            min_date = x
            break
    bug_dates = bug_dates[min_date:]
    bug_descr = bug_descr[min_date:] # align these dates with the start date of the project
   # print ax.get_position() # used to figure out how to draw the legend ... 
    loc = (0.34,0.54)
    ax.legend(loc=loc,numpoints=1,shadow=True) #10 is middle
    i = 0
    for bug_date in bug_dates:
    #each date position, at the maximum height, add the text of that date's release, vertically rotated
        ax.text(bug_date,max(counts)-max(counts)/9, bug_descr[i], rotation='vertical')
        i = i + 1
    
def add_metadata(ax,corr):
    r2 = corr * corr #r2 value, between 0-1
    plt.ylabel('Frequency')# (events/total events * 1000)')#("Frequency")
    plt.xlabel("Date")
    plt.title(#"Frequency of signifier occurrence over time\n" + 'Product: ' + project + ", signifier: " + signifier 
                # + 
                'r^2={0:.2%}'.format(r2), verticalalignment='bottom')
    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()
    return r2
    
def export():
    F = plt.gcf()
    F.savefig('/Users/nernst/Documents/papers/current-papers/refsq/figures/abs/' + project + '-'+ signifier + '-line.pdf')
        
if __name__ == '__main__':
    import pickle
    from names import Taxonomy
    t  = Taxonomy()
    products =  ['Evolution', 'Nautilus', 'Deskbar', 'Metacity', 'Ekiga', 'Totem', 'Evince', 'Empathy']
    #products = ['Totem']
    keywords = ['Efficiency', 'Portability', 'Maintainability', 'Reliability', 'Functionality', 'Usability']
    data_dict = {}
    save_file = open('/Users/nernst/Documents/papers/current-papers/refsq/abs-latex-refsq.csv', 'w')
    save_file.write('File-Keyword, r2, slope, intercept, n\n')
    # for product in products:
        # for key in keywords:
    product = 'Nautilus'     
    key = 'Portability'
    filename = product + '-' + key + '.pcl'
    print filename
    f = open('/Users/nernst/Documents/papers/current-papers/refsq/data/pickles/ext/'+ filename)
    df = pickle.load(f)
    f.close()
    df2 = []
    print len(df)
    for x in df:
        # print x[0]
        if x[0] != 200745 and x[0] != 200136 and x[0] != 200744: #if x[2] > 1000:# 
            df2.append(x)
    print len(df2)
    normalized = False
    #save the r2 and slope/intercept numbers externally
    r2, slope, intercept, n = main(df2, product, key, normalized)
    #data_store = [r2,slope,intercept]
    #data_dict[filename] = data_store
    #save_file.write(product + ' & ' + key + ' & ' + str(r2) + ' & ' + str(slope) + ' & ' + str(intercept) + ' & ' + str(n) + ' \\\\\n')
    save_file.write(product + ', ' + key + ' , ' + str(r2) + ' , ' + str(slope) + ' , ' + str(intercept) + ' , ' + str(n) + ' \\\\\n')

    #print((product + ' & ' + key + ' & ' + str(round(r2,2)) + ' & ' + str(round(slope,2)) + ' & ' + str(round(intercept, 2)) + ' & ' + str(n) + ' \\\\\n'))