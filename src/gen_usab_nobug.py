import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.mlab as mlab
import datetime

fig = plt.figure()
ax = fig.add_subplot(111)
from matplotlib import rcParams
rcParams['text.usetex']=True
rcParams['text.latex.unicode']=True
def main(): 
    """ plot usability- nautilus using useful defaults, without bug data"""
    years    = mdates.YearLocator()   # every year
    months   = mdates.MonthLocator(interval=3)  # every quarter
    yearsFmt = mdates.DateFormatter('%Y-%m') # want the x-axis to have ticks labelled (2008-Jan)

    reader = csv.reader(open('/Users/nernst/Documents/current-papers/icsm09/data/naut-usab-nobug-WN.csv'))
    naut = dict([x for x in reader])

    reader = csv.reader(open('/Users/nernst/Documents/current-papers/icsm09/data/naut-all-nobug.csv'))
    all_d = dict([x for x in reader])
    x = all_d.fromkeys(all_d.keys(), 0)
    for y in naut.keys():
        x[y] = float(naut[y])/float(all_d[y]) #normalize
    assert x['200133'] == 4.0/179

    bug_dates = [  datetime.datetime(2000, 5, 25), datetime.datetime(2001, 4, 3), datetime.datetime(2002, 6, 26), datetime.datetime(2003, 2, 5), datetime.datetime(2003, 9, 11), datetime.datetime(2003, 11, 29), datetime.datetime(2004, 3, 31), datetime.datetime(2004, 9, 15), datetime.datetime(2005, 3, 9), datetime.datetime(2005, 9, 7), datetime.datetime(2006, 3, 15), datetime.datetime(2006, 9, 6), datetime.datetime(2007, 3, 14), datetime.datetime(2007, 9, 19), datetime.datetime(2008, 3, 12), datetime.datetime(2008, 9, 24), datetime.datetime(2009, 2, 4)]
    bug_descr = [  '1.2', '1.4', '2', '2.2', '2.4', '2.5.0', '2.6', '2.8', '2.10', '2.12', '2.14', '2.16', '2.18', '2.20', '2.22', '2.24', '2.26b1']

    date_sort = x.keys()
    date_sort.sort() #sorted dates, ascending
    
    events = []
    for d in date_sort:
        events.append(x[d])
    
    assert events[123] == x[date_sort[123]]    
    
    # i = 0
    #     for e in events:
    #         i = i + 1
    #         if e > 0.320: 
    #             print e, i # the largest three for audit
    #             print date_sort[i]
    
    
    dates = []
    for dateweek in date_sort:
        datefmt = str(dateweek) + '-0' #200845 first day of week
        dates.append(datetime.datetime.strptime(datefmt, '%Y%U-%w') )


    ax.plot(dates, events,'r-', antialiased=True, label='Occurrences') #  problem is the dates are not monotonically increasing
    rel_lines = ax.vlines(bug_dates, 0, max(events), color='#616D7E', linestyles='dashed', label='_nolegend_')

    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    datemin = min(dates)
    datemax = datetime.date(2009,5,1)

    corr, slope, intercept = add_trend(dates, events)

    ax.set_xlim(datemin, datemax)
    ax.set_ylim(0, max(events)+0.13)
    r2 = add_metadata(ax,corr)
    add_label(dates, bug_dates, events, bug_descr)
    plt.show()

def sortedDictValues1(adict):
    items = adict.items()
    items.sort()
    return [value for key, value in items]

def add_label(dates, bug_dates, counts, bug_descr):
    """ label the release lines, and add a legend. corr is the correlation coefficient"""
    
    # min_date = 0
    # for x in range(len(bug_dates)):
    #     if bug_dates[x] >= dates[0]:
    #         min_date = x
    #         break
    # bug_dates = bug_dates[min_date:]
    # bug_descr = bug_descr[min_date:] # align these dates with the start date of the project
    plt.legend(loc=0,numpoints=1,shadow=True) #10 is middle
    i = 0
    for bug_date in bug_dates:
    #each date position, at the maximum height, add the text of that date's release, vertically rotated
        plt.text(bug_date, max(counts), bug_descr[i], rotation='vertical')
        i = i + 1
            
def add_metadata(ax,corr):
    r2 = corr * corr #r2 value, between 0-1 "
    plt.ylabel('Frequency (events/total events)')#("Frequency")
    plt.xlabel("Date")
    plt.title("Frequency of signifier occurrence over time\n" + 'Product: Nautilus, signifier: Usability', verticalalignment='bottom') # $r^2$={0:.2%}%'.format(r2)
    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()
    #return r2
    
def add_trend(x, y):
    """Add the least-squares linear regression, and corr. coeff"""
    #generate a list of integers for the dates
    new_x = []
    for i in range(len(x)):
       new_x.append(i)
    int_corr = np.corrcoef(new_x, y) # of form array([[ 1.,  0.09553632], [ 0.09553632,  1.]])
    corr = int_corr[0][1]
    z = np.polyfit(new_x, y, 1) # a 1-degree regression
    slope, intercept = z
    print slope
    p = np.poly1d(z)
    trend_line = ax.plot(x, p(new_x), 'k-', label='\^{{y}} = {0:.2f} + {1:.2f} x '.format(intercept,slope))
    #ax.text("Aargh")
    return corr, slope, intercept
    
if __name__ == '__main__':
    main()