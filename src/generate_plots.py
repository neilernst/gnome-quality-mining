#!/usr/bin/env python
"""
Show how to make date plots in matplotlib using date tick locators and
formatters.  See major_minor_demo1.py for more information on
controlling major and minor ticks

All matplotlib date plotting is done by converting date instances into
days since the 0001-01-01 UTC.  The conversion, tick locating and
formatting is done behind the scenes so this is most transparent to
you.  The dates module provides several converter functions date2num
and num2date

"""
import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.mlab as mlab

years    = mdates.YearLocator()   # every year
months   = mdates.MonthLocator(interval=3)  # every month
yearsFmt = mdates.DateFormatter('%Y-%m') # want the x-axis to have ticks labelled (2008-Jan)

#sample data -- will be loaded from the query. Format is 1998-q1 -- 2009-q4
df = [(0, datetime.date(1998, 3, 30)), (2, datetime.date(1998, 6, 30)), (0, datetime.date(1998, 9, 30)), (0, datetime.date(1998, 12, 30)), (0, datetime.date(1999, 3, 30)), (0, datetime.date(1999, 6, 30)), (0, datetime.date(1999, 9, 30)), (0, datetime.date(1999, 12, 30)), (1, datetime.date(2000, 3, 30)), (12, datetime.date(2000, 6, 30)), (6, datetime.date(2000, 9, 30)), (11, datetime.date(2000, 12, 30)), (9, datetime.date(2001, 3, 30)), (6, datetime.date(2001, 6, 30)), (5, datetime.date(2001, 9, 30)), (2, datetime.date(2001, 12, 30)), (2, datetime.date(2002, 3, 30)), (4, datetime.date(2002, 6, 30)), (1, datetime.date(2002, 9, 30)), (4, datetime.date(2002, 12, 30)), (14, datetime.date(2003, 3, 30)), (4, datetime.date(2003, 6, 30)), (11, datetime.date(2003, 9, 30)), (7, datetime.date(2003, 12, 30)), (7, datetime.date(2004, 3, 30)), (9, datetime.date(2004, 6, 30)), (4, datetime.date(2004, 9, 30)), (7, datetime.date(2004, 12, 30)), (2, datetime.date(2005, 3, 30)), (4, datetime.date(2005, 6, 30)), (5, datetime.date(2005, 9, 30)), (6, datetime.date(2005, 12, 30)), (8, datetime.date(2006, 3, 30)), (2, datetime.date(2006, 6, 30)), (0, datetime.date(2006, 9, 30)), (7, datetime.date(2006, 12, 30)), (13, datetime.date(2007, 3, 30)), (5, datetime.date(2007, 6, 30)), (4, datetime.date(2007, 9, 30)), (2, datetime.date(2007, 12, 30)), (0, datetime.date(2008, 3, 30)), (1, datetime.date(2008, 6, 30)), (0, datetime.date(2008, 9, 30)), (0, datetime.date(2008, 12, 30))]
bug_dates = [datetime.date(1997, 8, 1), datetime.date(1998, 3, 10), datetime.date(1998, 6, 7), datetime.date(1998, 12, 30), datetime.date(1999, 1, 4), datetime.date(1999, 1, 12), datetime.date(1999, 1, 18), datetime.date(1999, 1, 31), datetime.date(1999, 2, 8), datetime.date(1999, 2, 15), datetime.date(1999, 3, 1), datetime.date(1999, 3, 14), datetime.date(1999, 3, 26), datetime.date(1999, 4, 12), datetime.date(1999, 6, 4), datetime.date(1999, 6, 24), datetime.date(1999, 7, 19), datetime.date(1999, 10, 12), datetime.date(1999, 12, 24), datetime.date(2000, 1, 24), datetime.date(2000, 1, 30), datetime.date(2000, 2, 21), datetime.date(2000, 2, 29), datetime.date(2000, 3, 27), datetime.date(2000, 4, 4), datetime.date(2000, 5, 11), datetime.date(2000, 5, 25), datetime.date(2001, 2, 17), datetime.date(2001, 2, 28), datetime.date(2001, 3, 20), datetime.date(2001, 4, 3), datetime.date(2001, 4, 10), datetime.date(2001, 8, 6), datetime.date(2002, 2, 2), datetime.date(2002, 2, 20), datetime.date(2002, 4, 22), datetime.date(2002, 4, 28), datetime.date(2002, 6, 7), datetime.date(2002, 6, 14), datetime.date(2002, 6, 22), datetime.date(2002, 6, 26), datetime.date(2002, 8, 9), datetime.date(2002, 8, 15), datetime.date(2002, 11, 27), datetime.date(2003, 1, 12), datetime.date(2003, 1, 28), datetime.date(2003, 2, 5), datetime.date(2003, 9, 11), datetime.date(2003, 11, 29), datetime.date(2003, 12, 14), datetime.date(2004, 1, 6), datetime.date(2004, 2, 3), datetime.date(2004, 2, 13), datetime.date(2004, 3, 18), datetime.date(2004, 3, 31), datetime.date(2004, 6, 4), datetime.date(2004, 6, 14), datetime.date(2004, 7, 24), datetime.date(2004, 9, 15), datetime.date(2004, 10, 26), datetime.date(2004, 11, 4), datetime.date(2004, 12, 8), datetime.date(2004, 12, 23), datetime.date(2005, 1, 13), datetime.date(2005, 2, 3), datetime.date(2005, 2, 11), datetime.date(2005, 2, 22), datetime.date(2005, 3, 9), datetime.date(2005, 7, 7), datetime.date(2005, 7, 18), datetime.date(2005, 7, 28), datetime.date(2005, 9, 7), datetime.date(2005, 10, 26), datetime.date(2005, 11, 30), datetime.date(2005, 12, 14), datetime.date(2006, 1, 4), datetime.date(2006, 1, 19), datetime.date(2006, 2, 1), datetime.date(2006, 2, 8), datetime.date(2006, 2, 15), datetime.date(2006, 3, 1), datetime.date(2006, 3, 15), datetime.date(2006, 4, 12), datetime.date(2006, 4, 26), datetime.date(2006, 5, 18), datetime.date(2006, 5, 31), datetime.date(2006, 6, 15), datetime.date(2006, 7, 14), datetime.date(2006, 8, 9), datetime.date(2006, 8, 24), datetime.date(2006, 9, 6), datetime.date(2006, 10, 4), datetime.date(2006, 10, 18), datetime.date(2006, 11, 8), datetime.date(2006, 11, 22), datetime.date(2006, 12, 6), datetime.date(2007, 1, 10), datetime.date(2007, 1, 24), datetime.date(2007, 1, 31), datetime.date(2007, 2, 14), datetime.date(2007, 2, 28), datetime.date(2007, 3, 14), datetime.date(2007, 4, 11), datetime.date(2007, 4, 26), datetime.date(2007, 5, 16), datetime.date(2007, 7, 1), datetime.date(2007, 8, 1), datetime.date(2007, 8, 16), datetime.date(2007, 8, 29), datetime.date(2007, 9, 19), datetime.date(2007, 10, 18), datetime.date(2007, 10, 31), datetime.date(2007, 11, 28), datetime.date(2007, 12, 22), datetime.date(2008, 1, 17), datetime.date(2008, 2, 13), datetime.date(2008, 2, 28), datetime.date(2008, 3, 12), datetime.date(2008, 4, 9), datetime.date(2008, 4, 23), datetime.date(2008, 5, 28), datetime.date(2008, 6, 4), datetime.date(2008, 6, 18), datetime.date(2008, 7, 23), datetime.date(2008, 8, 6), datetime.date(2008, 8, 21), datetime.date(2008, 9, 24), datetime.date(2008, 10, 22), datetime.date(2008, 11, 6), datetime.date(2008, 11, 26), datetime.date(2008, 12, 3), datetime.date(2009, 1, 15), datetime.date(2009, 2, 4)]
bug_descr = ['GNOME development announced', '0.13', '0.2', '0.91', '0.99.2', '0.99.3', '0.99.4', '0.99.5', '0.99.7', '0.99.8', '1.0.0', '1.0.3', '1.0.4', '1.0.5', '1.0.6', '1.0.7', '1.0.9', '1.0.53 ', '1.0.55', '1.1.1', '1.1.2', '1.1.4', '1.1.5', '1.1.6', '1.1.8.1', '1.1.90', '1.2', '1.4.beta1', '1.4.beta2', '1.4 rc1', '1.4', '1.4.0.2', '1.4.1.beta1', '1.4.1 RC1', '2.0.0 beta', '1.4.0.7', '1.4.0.8', '2.0.0 snapshot', '2.0.0 RC1', '2.0.0 RC2', '2', '2.0.1 RC1', '2.0.1', '2.0.3', '2.1.90 RC1', '2.1.91 RC2', '2.2', '2.4', '2.5.0', '2.5.1', '2.5.2', '2.5.3', '2.5.4', '2.5.92', '2.6', '2.7.1', '2.7.2', '2.7.4', '2.8', '2.8.1', '2.9.1', '2.8.2', '2.9.3', '2.9.4', '2.10 beta 1', '2.10 beta 1', '2.8.3', '2.10,', '2.10.2', '2.11.5', '2.12 beta 1', '2.12', '2.13.1', '2.12.2', '2.13.3', '2.13.4', '2.13.5', '2.13.90 beta 1', '2.12.3', '2.14.beta2', '2.14 RC1', '2.14', '2.14.1', '2.15.1', '2.15.2', '2.14.2', '2.15.3', '2.15.4', '2.15.91 (2.16.beta2)', '2.15.92 (2.16 RC1)', '2.16', '2.16.1', '2.17.1', '2.17.2', '2.16.2', '2.17.3', '2.17.5', '2.17.90', '2.16.3', '2.18.0 beta2', '2.18.0 RC1', '2.18', '2.18.1', '2.19.1', '2.19.2', '2.19.5', '2.19.6', '2.19.90', '2.19.91', '2.20,', '2.20.1', '2.21.1', '2.20.2', '2.21.4', '2.21.5', '2.21.91', '2.21.92', '2.22', '2.22.1', '2.23.1', '2.22.2', '2.23.3', '2.23.4', '2.23.5', '2.23.6', '2.23.90', '2.24', '2.24.1', '2.25.1', '2.24.2', '2.25.2', '2.24.3', '2.25.90']
counts = []
dates = []
art = []
for i in range(133):
    art.append(7)
print len(art), len(bug_dates),len(counts), len(dates)
for count, date in df:
   counts.append(count)
   dates.append(date) 

fig = plt.figure()
#xval = [x for x in range(len(df))]
ax = fig.add_subplot(111)
ax.plot(dates, counts, 'b-', bug_dates, art, 'go') 
#line = matplotlib.lines.Line2D([2009,2009], [100,400], color='red', linestyle='-.')

# format the ticks
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(months)

datemin = datetime.date(1998,1,1)
datemax = datetime.date(2009,1,1)

ax.set_xlim(datemin, datemax)

# format the coords message box
#def price(x): return '$%1.2f'%x
#ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
#ax.format_ydata = price
ax.grid(True)

# rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them
fig.autofmt_xdate()

plt.show()
