#
# Scenario: there is data that contains two datetime stamps: Opened <some date> and Closed <some date>
# Goal: Establish environment count for incidents by quarter
#

# explicit date setting: start and end date of the quarter
start_date = datetime.datetime(2018, 1, 1, 0, 0, 0) # <- beginning of Q1
end_date = datetime.datetime(2018, 9, 30, 23, 59, 59) # <- end of Q3

# create masks which can be applied against a dataframe
date_mask_opened = (book['Opened'] >= start_date) & (book['Opened'] <= end_date)
date_mask_closed = (book['Closed'] >= start_date) & (book['Closed'] <= end_date)

# force all dates to fall within the 3 quarter limit
book = book.loc[(date_mask_opened & date_mask_closed)]


#
# setting up dataset for graphing
#

# set up overall distribution
# <>.groupby(pd.Grouper(freq='Q')) means group by quarter. 'W' means week, etc. Datetime operations.
opens = book.set_index('Opened').groupby(pd.Grouper(freq='Q'))['Number'].count() 
resolves = book.set_index('Resolved').groupby(pd.Grouper(freq='Q'))['Number'].count()

# Means and other cool things
test_plt = pd.DataFrame({'opens':opens, 'resolves': resolves})
opens_mean = np.floor(test_plt['opens'].mean())
resolves_mean = np.floor(test_plt['resolves'].mean())
ax2.plot([test_plt.index.min(), test_plt.index.max()], [resolves_mean,resolves_mean], label='Mean', color='red', linestyle='--', linewidth=0.5)
# the above: plot [ range of X (dates) ], [ range of Y - in this case the mean which is always the same, a constant ], <some pretty fluff>

#
# awesome titles and things
#

# comepute a mean of means
mean_of_means = np.round(book.groupby('Priority')['Resolve time'].describe()['mean'].mean() / 3600, decimals=0)
# plot it in your figure
ax1.plot([book.loc[:,('Priority')].sort_values().unique().min(), book.loc[:,('Priority')].sort_values().unique().max()], [mean_of_means,mean_of_means], label='Mean', color='red', linestyle='--', linewidth=0.5)
# write the number in your plot's title
ax1.set_title('Mean incident resolve by Priority\n Resolve mean of means: %g hours' % mean_of_means)
