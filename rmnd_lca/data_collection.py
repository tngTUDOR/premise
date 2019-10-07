"""
.. module: data_collection.py

"""
from pathlib import Path
from inspect import currentframe, getframeinfo
import pandas as pd
import xarray as xr
import numpy as np
import csv

DEFAULT_REMIND_DATA_DIR = Path(getframeinfo(currentframe()).filename).resolve().parent.joinpath('data/'+ 'Remind output files')
REMIND_ELEC_MARKETS = Path(getframeinfo(currentframe()).filename).resolve().parent.joinpath('data/'+ 'remind_electricity_markets.csv')
REMIND_ELEC_EFFICIENCIES = Path(getframeinfo(currentframe()).filename).resolve().parent.joinpath('data/'+ 'remind_electricity_efficiencies.csv')
REMIND_ELEC_EMISSIONS = Path(getframeinfo(currentframe()).filename).resolve().parent.joinpath('data/'+ 'remind_electricity_emissions.csv')
GAINS_EMISSIONS_FILEPATH = Path(getframeinfo(currentframe()).filename).resolve().parent.joinpath('data/'+ 'GAINS emission factors.csv')
GAINS_TO_REMIND_FILEPATH = Path(getframeinfo(currentframe()).filename).resolve().parent.joinpath('data/'+ 'GAINStoREMINDtechmap.csv')

class RemindDataCollection:
    """
    Class that extracts data from REMIND output files.

    :ivar scenario: name of a Remind scenario
    :vartype scenario: str

    """

    def __init__(self, scenario, year):
        self.scenario = scenario
        self.year = year
        self.data = self.get_remind_data()
        self.gains_data = self.get_gains_data()
        self.electricity_market_labels = self.get_remind_electricity_market_labels()
        self.electricity_efficiency_labels = self.get_remind_electricity_efficiency_labels()
        self.electricity_emission_labels = self.get_remind_electricity_emission_labels()
        self.rev_electricity_market_labels = self.get_rev_electricity_market_labels()
        self.rev_electricity_efficiency_labels = self.get_rev_electricity_efficiency_labels()
        self.electricity_markets = self.get_remind_electricity_markets()
        self.electricity_efficiencies = self.get_remind_electricity_efficiencies()
        self.electricity_emissions = self.get_remind_electricity_emissions()

    def get_remind_electricity_emission_labels(self):
        """
        Loads a csv file into a dictionary. This dictionary contains labels of electricity emissions
        in Remind.

        :return: dictionary that contains emission names equivalence
        :rtype: dict
        """

        if not REMIND_ELEC_EMISSIONS.is_file():
            raise FileNotFoundError('The REMIND electricity emissions dictionary file could not be found.')

        with open(REMIND_ELEC_EMISSIONS) as f:
            return dict(filter(None, csv.reader(f, delimiter=';')))

    def get_remind_electricity_market_labels(self):
        """
        Loads a csv file into a dictionary. This dictionary contains labels of electricity markets
        in Remind.

        :return: dictionary that contains market names equivalence
        :rtype: dict
        """

        if not REMIND_ELEC_MARKETS.is_file():
            raise FileNotFoundError('The REMIND electricity markets dictionary file could not be found.')

        with open(REMIND_ELEC_MARKETS) as f:
            return dict(filter(None, csv.reader(f, delimiter=';')))

    def get_remind_electricity_efficiency_labels(self):
        """
        Loads a csv file into a dictionary. This dictionary contains labels of electricity technologies efficiency
        in Remind.

        :return: dictionary that contains market names equivalence
        :rtype: dict
        """

        if not REMIND_ELEC_EFFICIENCIES.is_file():
            raise FileNotFoundError('The REMIND electricity technologies efficiencies dictionary file could not be found.')

        with open(REMIND_ELEC_EFFICIENCIES) as f:
            return dict(filter(None, csv.reader(f, delimiter=';')))

    def get_rev_electricity_market_labels(self):
        return {v: k for k, v in self.electricity_market_labels.items()}

    def get_rev_electricity_efficiency_labels(self):
        return {v: k for k, v in self.electricity_efficiency_labels.items()}


    def get_remind_data(self, directory = DEFAULT_REMIND_DATA_DIR):
        """
        Read the REMIND csv result file and return an `xarray` with dimensions:
        * region
        * variable
        * year

        :return: an multi-dimensional array with Remind data
        :rtype: xarray.core.dataarray.DataArray

        """

        filename = self.scenario + ".mif"
        filepath = Path(getframeinfo(currentframe()).filename).resolve().parent.joinpath(directory, filename)
        if not filepath.is_file():
            raise FileNotFoundError('The REMIND data outputs file could not be found.')

        df = pd.read_csv(
            filepath, sep=';',
            index_col=['Region', 'Variable', 'Unit']
        ).drop(columns=['Model', 'Scenario', 'Unnamed: 24'])
        df.columns = df.columns.astype(int)

        # Filter the dataframe
        df = df.loc[(df.index.get_level_values('Variable').str.contains('SE')) |
                    (df.index.get_level_values('Variable').str.contains('Tech'))]
        variables = df.index.get_level_values('Variable').unique()

        regions = df.index.get_level_values('Region').unique()
        years = df.columns
        array = xr.DataArray(
            np.zeros(
                (
                    len(variables),
                    len(regions),
                    len(years),
                    1
                )
            ),
            coords=[
                variables,
                regions,
                years,
                np.arange(1)
            ],
            dims=["variable", "region", "year", "value"],
        )
        for r in regions:
            val = df.loc[(df.index.get_level_values('Region') == r), :]
            array.loc[dict(region=r, value=0)] = val

        return array

    def get_gains_data(self, directory = DEFAULT_REMIND_DATA_DIR):
        """
        Read the GAINS emissions csv file and return an `xarray` with dimensions:
        * region
        * pollutant
        * sector
        * year

        :return: an multi-dimensional array with GAINS emissions data
        :rtype: xarray.core.dataarray.DataArray

        """
        if not GAINS_EMISSIONS_FILEPATH.is_file():
            raise FileNotFoundError('The GAINS emissions file could not be found.')

        gains_emi = pd.read_csv(GAINS_EMISSIONS_FILEPATH, skiprows=4,
                            names=["year", "region", "GAINS", "pollutant", "scenario", "factor"])
        gains_emi["unit"] = "Mt/TWa"
        gains_emi = gains_emi[gains_emi.scenario == 'SSP2']

        if not GAINS_TO_REMIND_FILEPATH.is_file():
            raise FileNotFoundError('The GAINS to REMIND mapping file could not be found.')

        sector_mapping = pd.read_csv(GAINS_TO_REMIND_FILEPATH).drop(["noef", "elasticity"], axis=1)

        gains_emi = gains_emi.join(sector_mapping.set_index("GAINS"), on="GAINS").dropna()\
                .drop(['scenario', 'REMIND'], axis=1)\
                .pivot_table(index = ['region','GAINS', 'pollutant', 'unit'] ,values='factor', columns='year')

        regions = gains_emi.index.get_level_values('region').unique()
        years = gains_emi.columns.values
        pollutants = gains_emi.index.get_level_values('pollutant').unique()
        sectors = gains_emi.index.get_level_values('GAINS').unique()

        array = xr.DataArray(
            np.zeros(
                (
                    len(pollutants),
                    len(sectors),
                    len(regions),
                    len(years),
                    1
                )
            ),
            coords=[
                pollutants,
                sectors,
                regions,
                years,
                np.arange(1)
            ],
            dims=["pollutant", "sector", "region", "year", "value"],
        )
        for r in regions:
            for s in sectors:
                val = gains_emi.loc[(gains_emi.index.get_level_values('region') == r) &
                                    (gains_emi.index.get_level_values('GAINS') == s), :]
                array.loc[dict(region=r, sector=s, value=0)] = val

        return array / 8760 # per TWha --> per TWh

    def get_remind_electricity_markets(self, drop_hydrogen = True):
        """
        This method retrieves the market share for each electricity-producing technology, for a specified year,
        for each region provided by REMIND.
        Electricity production from hydrogen can be removed from the mix (unless specified, it is removed).

        :param drop_hydrogen: removes hydrogen from the region-specific electricity mix if `True`.
        :type drop_hydrogen: bool
        :return: an multi-dimensional array with electricity technologies market share for a given year, for all regions.
        :rtype: xarray.core.dataarray.DataArray

        """
        # If hydrogen is not to be considered, it is removed from the technologies labels list
        if drop_hydrogen:
            list_technologies = [l for l in list(self.electricity_market_labels.values()) if 'Hydrogen' not in l]
        else:
            list_technologies = list(self.electricity_market_labels.values())

        # If the year specified is not contained within the range of years given by REMIND
        if self.year < self.data.year.values.min() or self.year > self.data.year.values.max():
            raise KeyError('year not valid, must be between 2005 and 2150')

        # Otherwise, if the year specified corresponds exactly to a year given by REMIND
        elif self.year in self.data.coords['year']:
            # The contribution of each technologies, for a specified year, for a specified region is normalized to 1.
            return self.data.loc[list_technologies,:,self.year]\
                   / self.data.loc[list_technologies,:,self.year].groupby('region').sum(axis=0)

        # Finally, if the specified year falls in between two periods provided by REMIND
        else:
            # Interpolation between two periods
            data_to_interp_from = self.data.loc[list_technologies,:,:]\
                   / self.data.loc[list_technologies,:,:].groupby('region').sum(axis=0)
            return data_to_interp_from.interp(year=self.year)

    def get_remind_electricity_efficiencies(self, drop_hydrogen = True):
        """
        This method retrieves efficiency values for electricity-producing technology, for a specified year,
        for each region provided by REMIND.
        Electricity production from hydrogen can be removed from the mix (unless specified, it is removed).

        :param drop_hydrogen: removes hydrogen from the region-specific electricity mix if `True`.
        :type drop_hydrogen: bool
        :return: an multi-dimensional array with electricity technologies market share for a given year, for all regions.
        :rtype: xarray.core.dataarray.DataArray

        """
        # If hydrogen is not to be considered, it is removed from the technologies labels list
        if drop_hydrogen:
            list_technologies = [l for l in list(self.electricity_efficiency_labels.values()) if 'Hydrogen' not in l]
        else:
            list_technologies = list(self.electricity_efficiency_labels.values())

        # If the year specified is not contained within the range of years given by REMIND
        if self.year < self.data.year.values.min() or self.year > self.data.year.values.max():
            raise KeyError('year not valid, must be between 2005 and 2150')

        # Otherwise, if the year specified corresponds exactly to a year given by REMIND
        elif self.year in self.data.coords['year']:
            # The contribution of each technologies, for a specified year, for a specified region is normalized to 1.
            return self.data.loc[list_technologies,:,self.year] / 100 # Percentage to ratio

        # Finally, if the specified year falls in between two periods provided by REMIND
        else:
            # Interpolation between two periods
            data_to_interp_from = self.data.loc[list_technologies,:,:]
            return data_to_interp_from.interp(year=self.year) / 100 # Percentage to ratio

    def get_remind_electricity_emissions(self):
        """
        This method retrieves emission values for electricity-producing technology, for a specified year,
        for each region provided by REMIND.

        :return: an multi-dimensional array with emissions for different technologies for a given year, for all regions.
        :rtype: xarray.core.dataarray.DataArray

        """
        # If the year specified is not contained within the range of years given by REMIND
        if self.year < self.gains_data.year.values.min() or self.year > self.gains_data.year.values.max():
            raise KeyError('year not valid, must be between 2005 and 2150')

        # Otherwise, if the year specified corresponds exactly to a year given by REMIND
        elif self.year in self.gains_data.coords['year']:
            # The contribution of each technologies, for a specified year, for a specified region is normalized to 1.
            return self.gains_data.loc[dict(year = self.year, value = 0)]

        # Finally, if the specified year falls in between two periods provided by REMIND
        else:
            # Interpolation between two periods
            return self.gains_data.loc[dict(value = 0)].interp(year=self.year)















