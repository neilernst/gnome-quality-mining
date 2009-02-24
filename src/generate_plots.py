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
counts = []
dates = []
for count, date in df:
   counts.append(count)
   dates.append(date) 

fig = plt.figure()
#xval = [x for x in range(len(df))]
ax = fig.add_subplot(111)
ax.plot(dates, counts) #will assign arbitrary X values starting from 1

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
