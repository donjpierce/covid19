import pandas as pd
import matplotlib.pyplot as plt


counties = pd.read_csv('us-counties.csv')
states = pd.read_csv('us-states.csv')
population = pd.read_csv('population.csv')
poverty = pd.read_csv('poverty.csv')
unemployment = pd.read_csv('unemployment.csv')

# pre-processing
population.columns = ['CENSUS_POP_2010' if col == 'CENSUS_2010_POP' else col for col in population.columns]
melted = pd.melt(population, id_vars=['State', 'County', 'FIPS'], value_vars=population.columns[3:])
variables = melted.variable.str.split('_', expand=True)


def get_new_cols():
    cols, groups, new_columns = [], [], {}
    for col in variables.columns[:-1]:
        groups.append(col)
        layer = variables.groupby(groups).first()

        levels = [layer.index.get_level_values(i) for i in range(len(groups))]
        for _, val in *levels, layer.loc[:, 1].values:
            try:
                date = pd.to_datetime(val)
                name = '_'.join(_)
                new_columns[name] = [date]
            except ValueError:
                continue
    return new_columns

