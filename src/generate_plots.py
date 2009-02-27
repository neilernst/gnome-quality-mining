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

import query_corpora

fig = plt.figure()
ax = fig.add_subplot(111)
from matplotlib import rcParams
rcParams['text.usetex']=True
rcParams['text.latex.unicode']=True

def main(df,product, keyword, normalized=True):
    
    global project, signifier #is this evil?
    project = product
    signifier = keyword
    years    = mdates.YearLocator()   # every year
    months   = mdates.MonthLocator(interval=3)  # every quarter
    yearsFmt = mdates.DateFormatter('%Y-%m') # want the x-axis to have ticks labelled (2008-Jan)

    bug_dates = [datetime.date(1997, 8, 1), datetime.date(1998, 3, 10), datetime.date(1998, 6, 7), datetime.date(1998, 12, 30), datetime.date(1999, 3, 1), datetime.date(1999, 10, 12), datetime.date(2000, 5, 25), datetime.date(2001, 4, 3), datetime.date(2002, 6, 26), datetime.date(2003, 2, 5), datetime.date(2003, 9, 11), datetime.date(2003, 11, 29), datetime.date(2004, 3, 31), datetime.date(2004, 9, 15), datetime.date(2005, 3, 9), datetime.date(2005, 9, 7), datetime.date(2006, 3, 15), datetime.date(2006, 9, 6), datetime.date(2007, 3, 14), datetime.date(2007, 9, 19), datetime.date(2008, 3, 12), datetime.date(2008, 9, 24), datetime.date(2009, 2, 4)]
    bug_descr = ['0.0', '0.13', '0.2', '0.91', '1.0.0', '1.0.53 ', '1.2', '1.4', '2', '2.2', '2.4', '2.5.0', '2.6', '2.8', '2.10', '2.12', '2.14', '2.16', '2.18', '2.20', '2.22', '2.24', '2.26b1']
    total_counts = []
    dates = []
    normal_counts = []
    for normal, count, date in df:
       total_counts.append(count)
       dates.append(date) 
       normal_counts.append(normal)
    
    # do we want absolute or normalized values?
    if normalized:
        counts = normal_counts
    else: 
        counts = total_counts
        
    occur = plt.plot(dates, counts, 'r.', label='Occurrences')#, bug_dates, art, 'go') 
        #occur = plt.scatter(dates, date_index, 'b.', label='Occurrences')
    #plot the release dates for Gnome as dashed vertical lines
    rel_lines = plt.vlines(bug_dates, 0, max(counts), color='#616D7E', linestyles='dashed', label='_nolegend_')
    
    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    datemin = datetime.date(1997,1,1)
    datemax = datetime.date(2009,5,1)

    corr = add_trend(dates, counts)
    
    ax.set_xlim(datemin, datemax)
    ax.set_ylim(0, max(counts))
    add_metadata(ax,corr)
    add_label(bug_dates, counts, bug_descr)
    #plt.show()
    export()
    
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
    p = np.poly1d(z)
    trend_line = plt.plot(x, p(new_x), 'k-', label='\^{{y}} = {0:.2} + {1:.2%} x '.format(intercept,slope))
    #plt.text()
    return corr
    
def add_label(bug_dates, counts, bug_descr):
    """ label the release lines, and add a legend. corr is the correlation coefficient"""
    plt.legend(loc=10,numpoints=1,shadow=True)
    i = 0
    for date in bug_dates:
    #each date position, at the maximum height, add the text of that date's release, vertically rotated
        plt.text(date,max(counts), bug_descr[i], rotation='vertical')
        i = i + 1
    #plt.text(datetime.date(2005,03,02), max(normal_counts) - 20, r'$r^2$={0:.2%}'.format(r2), zorder=3, bbox=dict(facecolor='red', alpha=0.5))
    
def add_metadata(ax,corr):
    #ax.grid(True)
    r2 = corr * corr #r2 value, between 0-1
    plt.ylabel('Frequency (events/total events * 1000)')#("Frequency")
    plt.xlabel("Date")
    plt.title("Frequency of signifier occurrence over time\n" + 'Product: ' + project + ", signifier: " + signifier 
                + ', $r^2$={0:.2%}%'.format(r2), verticalalignment='bottom')
    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()

def export():
    F = plt.gcf()
    F.savefig('/Users/nernst/Desktop/'+ project + '-'+ signifier + '.png')
        
if __name__ == '__main__':
    #sample data -- will be loaded from the query. Format is 1998-q1 -- 2009-q4
    df = [(0.0, 0, datetime.date(1998, 3, 30)), (103.09278350515464, 2, datetime.date(1998, 6, 30)), (0.0, 0, datetime.date(1998, 9, 30)), (0.0, 0, datetime.date(1998, 12, 30)), (0.0, 0, datetime.date(1999, 3, 30)), (0.0, 0, datetime.date(1999, 6, 30)), (0.0, 0, datetime.date(1999, 9, 30)), (0.0, 0, datetime.date(1999, 12, 30)), (12.594458438287154, 1, datetime.date(2000, 3, 30)), (60.090135202804206, 12, datetime.date(2000, 6, 30)), (24.824162184526273, 6, datetime.date(2000, 9, 30)), (41.462495288352805, 11, datetime.date(2000, 12, 30)), (29.239766081871345, 9, datetime.date(2001, 3, 30)), (27.459954233409611, 6, datetime.date(2001, 6, 30)), (14.021312394840157, 5, datetime.date(2001, 9, 30)), (7.2912869121399924, 2, datetime.date(2001, 12, 30)), (14.154281670205236, 2, datetime.date(2002, 3, 30)), (26.791694574681848, 4, datetime.date(2002, 6, 30)), (7.8616352201257858, 1, datetime.date(2002, 9, 30)), (14.466546112115733, 4, datetime.date(2002, 12, 30)), (49.071153172099542, 14, datetime.date(2003, 3, 30)), (13.149243918474689, 4, datetime.date(2003, 6, 30)), (53.191489361702125, 11, datetime.date(2003, 9, 30)), (24.458420684835779, 7, datetime.date(2003, 12, 30)), (27.047913446676972, 7, datetime.date(2004, 3, 30)), (27.04326923076923, 9, datetime.date(2004, 6, 30)), (21.085925144965735, 4, datetime.date(2004, 9, 30)), (30.567685589519652, 7, datetime.date(2004, 12, 30)), (7.8864353312302837, 2, datetime.date(2005, 3, 30)), (25.773195876288661, 4, datetime.date(2005, 6, 30)), (27.041644131963224, 5, datetime.date(2005, 9, 30)), (32.697547683923709, 6, datetime.date(2005, 12, 30)), (42.712226374799783, 8, datetime.date(2006, 3, 30)), (14.55604075691412, 2, datetime.date(2006, 6, 30)), (0.0, 0, datetime.date(2006, 9, 30)), (73.45225603357818, 7, datetime.date(2006, 12, 30)), (141.76663031624864, 13, datetime.date(2007, 3, 30)), (48.402710551790904, 5, datetime.date(2007, 6, 30)), (32.388663967611336, 4, datetime.date(2007, 9, 30)), (17.683465959328029, 2, datetime.date(2007, 12, 30)), (0.0, 0, datetime.date(2008, 3, 30)), (12.406947890818859, 1, datetime.date(2008, 6, 30)), (0.0, 0, datetime.date(2008, 9, 30)), (0, 0, datetime.date(2008, 12, 30))]
    main(df)
