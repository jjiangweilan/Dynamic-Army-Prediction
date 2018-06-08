def _plot(variable):
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

isolate_and_plot('UnitB_Health')