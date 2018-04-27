'''Guide p89 A5.8'''

# Load pandas and statsmodels
import pandas as pd
import numpy as np
import scipy.stats
import statsmodels.formula.api as smf

def calc(string):
    ''' calculator function; for convenience '''
    ''' use raw string, i.e. r"aoeui" '''
    result = eval(string)
    print(string, '=', result)
    return result

def fCrits(n,d):
    def fCrit(pValue):
        return scipy.stats.f.ppf(q=1-pValue, dfn=n, dfd=d)
    ps = [0.05, 0.025, 0.01, 0.001]
    print("\n__", "p-value", "F-crit(%d,%d)"%(n,d), "____")
    for p in ps:
        print(p, round(fCrit(p),2))

# Load a csv dataset of World Development Indicators
raw_data = pd.read_csv(r"..\Datasets\ces2013.csv")
#print( raw_data.head(3) )
#results = smf.ols("FDHO ~ EXP",raw_data).fit()

# Create custom subset of data
df = pd.DataFrame(raw_data, columns=['HEAL','EXP','SIZE','REFEDUC'])
df = df[df['HEAL'] > 0]
#print( "<0>\n", df.head(3) )
df = df.assign(COLLEGE = lambda x: np.where(x.REFEDUC <= 12, 0, 1))
df = df.assign(LGHEALPC = lambda x: np.log(x.HEAL/x.SIZE))
df = df.assign(LGEXPPC = lambda x: np.log(x.EXP/x.SIZE))
df = df.assign(LGSIZE = lambda x: np.log(x.SIZE))
#print( "<1>\n", df.head(9) )


results = smf.ols("LGHEALPC ~ LGEXPPC + LGSIZE",df[df["COLLEGE"]==1]).fit()
print( "<COLLEGE=1>\n", results.summary() )
rss1 = results.ssr
print("RSS:",rss1)

results = smf.ols("LGHEALPC ~ LGEXPPC + LGSIZE",df[df["COLLEGE"]==0]).fit()
print( "<COLLEGE=0>\n", results.summary() )
rss0 = results.ssr
print("RSS:",rss0)


results = smf.ols("LGHEALPC ~ LGEXPPC + LGSIZE",df).fit()
print( "<whole sample>\n", results.summary() )
rss = results.ssr
print("RSS:",rss)


# print stuff
print("\nRSS:")
rssArray = [rss, rss0, rss1]
for x in rssArray:
    print(round(x,1))

# calculations section
print("\n<Calculations>")
calc(r"3170+1632")
calc(r"((rss-(rss1+rss0))/3) / ((rss1+rss0)/(4802-6))")

# critical values
fCrits(3,1000)