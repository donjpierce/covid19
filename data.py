import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
from operator import eq


# counties = pd.read_csv('us-counties.csv')
# states = pd.read_csv('us-states.csv')
population = pd.read_csv('population.csv')
# poverty = pd.read_csv('poverty.csv')
# unemployment = pd.read_csv('unemployment.csv')

# pre-processing
population.columns = ['CENSUS_POP_2010' if col == 'CENSUS_2010_POP' else col for col in population.columns]
melted = pd.melt(population, id_vars=['State', 'County', 'FIPS'], value_vars=population.columns[3:])
variables = melted.variable.str.split('_', expand=True)


def require(df, column, operator, value):
    return operator(df[column], value)


def subset(df, *requirements):
    return df[np.logical_and(*requirements)]


def get_new_cols():
    cols, groups, new_columns = [], [], {}
    for col in variables.columns[:-1]:
        groups.append(col)
        layer = variables.groupby(groups).first()
        for name, row in layer.iterrows():
            try:
                if not row.iloc[0]:
                    continue
                date = pd.to_datetime(row.iloc[0])
                name = name if type(name) == str else '_'.join(name)
                new_columns[name] = [date.year]
                reqs, group_names = [], name.split('_')
                for g, n in zip(groups, group_names):
                    reqs.append(require(variables, g, eq, n))
                dates = pd.unique(subset(variables, reqs)[col + 1])
                print(dates)
                for d in dates:
                    new_columns[name].append(d)
            except ValueError or AttributeError:
                continue
    return new_columns

