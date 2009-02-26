#!/usr/bin/env python
"""
Generate a plot, based on the query results (see query_corpora.py)
Add a linear regression, Gnome release dats, and 

"""
import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.mlab as mlab

project = 'Evolution'
signifier = 'Usability'
fig = plt.figure()
ax = fig.add_subplot(111)

def main():
    years    = mdates.YearLocator()   # every year
    months   = mdates.MonthLocator(interval=3)  # every quarter
    yearsFmt = mdates.DateFormatter('%Y-%m') # want the x-axis to have ticks labelled (2008-Jan)

    #sample data -- will be loaded from the query. Format is 1998-q1 -- 2009-q4
    df = [(0, datetime.date(1998, 3, 30)), (2, datetime.date(1998, 6, 30)), (0, datetime.date(1998, 9, 30)), (0, datetime.date(1998, 12, 30)), (0, datetime.date(1999, 3, 30)), (0, datetime.date(1999, 6, 30)), (0, datetime.date(1999, 9, 30)), (0, datetime.date(1999, 12, 30)), (1, datetime.date(2000, 3, 30)), (12, datetime.date(2000, 6, 30)), (6, datetime.date(2000, 9, 30)), (11, datetime.date(2000, 12, 30)), (9, datetime.date(2001, 3, 30)), (6, datetime.date(2001, 6, 30)), (5, datetime.date(2001, 9, 30)), (2, datetime.date(2001, 12, 30)), (2, datetime.date(2002, 3, 30)), (4, datetime.date(2002, 6, 30)), (1, datetime.date(2002, 9, 30)), (4, datetime.date(2002, 12, 30)), (14, datetime.date(2003, 3, 30)), (4, datetime.date(2003, 6, 30)), (11, datetime.date(2003, 9, 30)), (7, datetime.date(2003, 12, 30)), (7, datetime.date(2004, 3, 30)), (9, datetime.date(2004, 6, 30)), (4, datetime.date(2004, 9, 30)), (7, datetime.date(2004, 12, 30)), (2, datetime.date(2005, 3, 30)), (4, datetime.date(2005, 6, 30)), (5, datetime.date(2005, 9, 30)), (6, datetime.date(2005, 12, 30)), (8, datetime.date(2006, 3, 30)), (2, datetime.date(2006, 6, 30)), (0, datetime.date(2006, 9, 30)), (7, datetime.date(2006, 12, 30)), (13, datetime.date(2007, 3, 30)), (5, datetime.date(2007, 6, 30)), (4, datetime.date(2007, 9, 30)), (2, datetime.date(2007, 12, 30)), (0, datetime.date(2008, 3, 30)), (1, datetime.date(2008, 6, 30)), (0, datetime.date(2008, 9, 30)), (0, datetime.date(2008, 12, 30))]
    bug_dates = [datetime.date(1997, 8, 1), datetime.date(1998, 3, 10), datetime.date(1998, 6, 7), datetime.date(1998, 12, 30), datetime.date(1999, 3, 1), datetime.date(1999, 10, 12), datetime.date(2000, 5, 25), datetime.date(2001, 4, 3), datetime.date(2002, 6, 26), datetime.date(2003, 2, 5), datetime.date(2003, 9, 11), datetime.date(2003, 11, 29), datetime.date(2004, 3, 31), datetime.date(2004, 9, 15), datetime.date(2005, 3, 9), datetime.date(2005, 9, 7), datetime.date(2006, 3, 15), datetime.date(2006, 9, 6), datetime.date(2007, 3, 14), datetime.date(2007, 9, 19), datetime.date(2008, 3, 12), datetime.date(2008, 9, 24), datetime.date(2009, 2, 4)]
    bug_descr = ['GNOME development announced', '0.13', '0.2', '0.91', '1.0.0', '1.0.53 ', '1.2', '1.4', '2', '2.2', '2.4', '2.5.0', '2.6', '2.8', '2.10,', '2.12', '2.14', '2.16', '2.18', '2.20,', '2.22', '2.24', '2.25.90']
    counts = []
    dates = []
    
    for count, date in df:
       counts.append(count)
       dates.append(date) 


    occur = plt.plot(dates, counts, 'b.')#, bug_dates, art, 'go') 
    #plot the release dates for Gnome as dashed vertical lines
    rel_lines = plt.vlines(bug_dates, 0, max(counts), color='k', linestyles='dashed')
    
    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    datemin = datetime.date(1998,1,1)
    datemax = datetime.date(2009,1,1)

    corr = add_trend(dates, counts)
    
    ax.set_xlim(datemin, datemax)
    add_metadata(ax)
    add_label(corr)
    #plt.show()
    export()
    
def add_trend(x, y):
    """Add the least-squares linear regression, and corr. coeff"""
    #generate a list of integers for the dates
    new_x = []
    for i in range(len(x)):
       new_x.append(i)
    int_corr = np.corrcoef(new_x, y) # of form     array([[ 1.        ,  0.09553632], [ 0.09553632,  1.        ]])
    corr = int_corr[0][1]
    z = np.polyfit(new_x, y, 1) # a 1-degree regression
    p = np.poly1d(z)
    plt.plot(x, y, '.', x, p(new_x), '-')
    return corr
    
def add_label(corr):
    """ label the release lines, and add a legend. corr is the correlation coefficient"""
    r2 = corr * corr #r2 value, between 0-1

def add_metadata(ax):
    #ax.grid(True)
    plt.ylabel("Frequency")
    plt.xlabel("Date")
    plt.title("Frequency of signifier occurrence over time\n" + 'Product: ' + project + ", signifier: " + signifier, verticalalignment='bottom')
    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()

def export():
    F = plt.gcf()
    F.savefig('/Users/nernst/Desktop/'+ project + '-'+ signifier + '.png')
        
if __name__ == '__main__':
      main()
