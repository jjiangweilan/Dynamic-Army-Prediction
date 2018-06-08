import pandas as pd

import statsmodels.api as sm

import pylab as pl

import numpy as np


def cartesian(arrays, out=None):
    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype

    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)

    m = n / arrays[0].size
    out[:,0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m,1:])
        for j in xrange(1, arrays[0].size):
            out[j*m:(j+1)*m,1:] = out[0:m,1:]
    return out

    
df = pd.read_csv("/Users/kavyadindu/Desktop/example.csv")
df.columns = ["win", "UnitA_Health", "UnitB_Health", "Attribution"]

#print df.std()
#print pd.crosstab(df['win'], df['Attribution'], rownames=['win'])
#print pd.crosstab(df['win'], df['Attribution'], rownames=['win'])

dummy_ranks = pd.get_dummies(df['Attribution'], prefix='Attribution')
#print dummy_ranks.head()

cols_to_keep = ['win', 'UnitA_Health', 'UnitB_Health']
data = df[cols_to_keep].join(dummy_ranks.ix[:, 'Attribution_2':])
#print data.head()


data['intercept'] = 1.0
train_cols = data.columns[1:]
logit = sm.Logit(data['win'], data[train_cols])
result = logit.fit()
print result.summary()


#print result.conf_int()
#print np.exp(result.params)
params = result.params
conf = result.conf_int()

#print conf
conf['OR'] = params
print np.exp(conf)
UnitA_Healths = np.linspace(data['UnitA_Health'].min(), data['UnitA_Health'].max(), 10)
#print UnitA_Healths
UnitB_Healths = np.linspace(data['UnitB_Health'].min(), data['UnitB_Health'].max(), 10)



combos = pd.DataFrame(cartesian([UnitA_Healths, UnitB_Healths, [1, 2, 3, 4], [1.]]))
combos.columns = ['UnitA_Health', 'UnitB_Health', 'Attribution', 'intercept']


dummy_ranks = pd.get_dummies(combos['Attribution'], prefix='Attribution')
dummy_ranks.columns = ['Attribution_1', 'Attribution_2', 'Attribution_3', 'Attribution_4']
cols_to_keep = ['UnitA_Health', 'UnitB_Health', 'Attribution', 'intercept']
combos = combos[cols_to_keep].join(dummy_ranks.ix[:, 'Attribution_2':])
combos['win_pred'] = result.predict(combos[train_cols])
print combos.head()

def isolate_and_plot(variable):
  
    grouped = pd.pivot_table(combos, values=['win_pred'], index=[variable, 'Attribution'],
                            aggfunc=np.mean)
  
  

    colors = 'rbgyrbgy'
    for col in combos.Attribution.unique():
        plt_data = grouped.ix[grouped.index.get_level_values(1)==col]
        pl.plot(plt_data.index.get_level_values(0), plt_data['win_pred'],
                color=colors[int(col)])

    pl.xlabel(variable)
    pl.ylabel("P(win=1)")
    pl.legend(['1', '2', '3', '4'], loc='upper left', title='Attribution')
    pl.title("Prob(win=1) isolating " + variable + " and Attribution")
    pl.show()

isolate_and_plot('UnitA_Health')



