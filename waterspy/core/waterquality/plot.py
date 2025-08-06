"""Plotting module for water quality data."""
from waterspy.core.waterquality.models import SampleTimeseries
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Optional
from pandas import Timestamp, DataFrame, Categorical


def boxplots(sample_ts: SampleTimeseries,
             stats: bool = True,
             split_params: Optional[tuple[Timestamp, str, str]] = None,
             **kwargs) -> None:
    """Plot boxplots of the samples.

    For this function to work, there has to be just one parameter. Multiple stations
    are allowed.

    Args:
        sample_ts (SampleTimeseries): The sample timeseries.
        stats (bool, optional): Whether to plot the statistics of the samples. Defaults to True.
        split_params (Optional[tuple[Timestamp, str, str]], optional): The split parameters. Defaults to None.
        **kwargs: Additional keyword arguments for the plot.

    Functions:
        color_palette (list): The color palette for the plot.

    >>> split_params = (Timestamp('2022-04-01'), 'preinjection', 'postinjection')
    """

    parameter = sample_ts.unique_parameters
    unit = sample_ts[0].measurements[0].unit
    assert len(parameter) == 1, "Only one parameter is allowed for this function."

    color_palette = kwargs.get('color_palette', ['b', 'g'])
    df_long = sample_ts.long_ts().reset_index(
        name=parameter[0])  # type: ignore

    if split_params:
        df_long['split'] = df_long['timestamp'].apply(
            lambda x: split_params[1] if x <= split_params[0] else split_params[2])
        df_long['split'] = Categorical(df_long['split'], categories=[
                                       split_params[1], split_params[2]], ordered=True)
        ax = sns.boxplot(x="station", y=parameter[0],
                         hue="split", palette=color_palette,
                         data=df_long.sort_values(by=['station', 'split']))

    else:
        ax = sns.boxplot(x="station", y=parameter[0], palette=color_palette,
                         data=df_long)

    ax.set_title(f'Boxplot of {parameter[0]}')
    ax.set_ylabel(f'{parameter[0]} [{unit}]')

    def plot_stats_table(stats: DataFrame,
                         label: str,
                         bbox: tuple[float, float, float, float],
                         text_position: tuple[float, float]):
        """Plot a table with the statistics of the samples.

        Args:
            stats (DataFrame): The statistics of the samples.
            label (str): The label of the table.
            bbox (tuple[float, float, float, float]): The bounding box of the table.
            text_position (tuple[float, float]): The position of the text.
        """

        plt.text(*text_position, label, ha='center', va='center',
                 transform=plt.gca().transAxes, fontsize=12, fontweight='bold')
        table = plt.table(cellText=stats.round(3).values,
                          rowLabels=stats.index.get_level_values(0),
                          colLabels=stats.columns,
                          bbox=bbox
                          )
        return table

    if stats and split_params:
        plot_stats_table(sample_ts.filter_samples(
            end=split_params[0]).statistics, split_params[1], (1.3, .5, 0.8, 0.5), (1.55, 1.1))  # type: ignore
        plot_stats_table(sample_ts.filter_samples(
            start=split_params[0]).statistics, split_params[2], (1.3, -.2, 0.8, 0.5), (1.55, 0.4))  # type: ignore

    elif stats:
        plot_stats_table(sample_ts.statistics, 'All',
                         (1.3, .5, 0.8, 0.5), (1.55, 1.1))

    sns.despine(offset=10, trim=True)


def lineplot(sample_ts: SampleTimeseries,
             title: str,
             vline: Optional[Timestamp] = None,
             hline: Optional[float] = None,
             **kwargs) -> None:
    """Plot a lineplot of the samples.

    In this function, there can be either one station and multiple parameters or
    multiple stations and one parameter.

    Args:
        sample_ts (SampleTimeseries): The sample timeseries.
        title (str): The title of the plot.
        vline (Optional[Timestamp], optional): A vertical line to plot. Defaults to None.
        hline (Optional[float], optional): A horizontal line to plot. Defaults to None.
    """

    df_long = sample_ts.long_ts().reset_index(
    ).sort_values(by=['station', 'timestamp'])

    plt.figure(figsize=(12, 4))  # Create a new figure
    ax = sns.lineplot(data=df_long, x='timestamp',
                      y=0, hue='station', style='station', markers=True, dashes=False)

    if vline:
        vline_label = kwargs.get('vline_label', None)
        ax.axvline(x=vline, color='r', linestyle='--', label=vline_label)  # type: ignore # noqa
    if hline:
        hline_label = kwargs.get('hline_label', None)
        ax.axhline(y=hline, color='b', linestyle='--', label=hline_label)

    ax.set_title(title)
    plt.xlabel('Date')
    plt.ylabel('Value')

    handles, labels = ax.get_legend_handles_labels()
    if vline or hline:
        ax.legend(handles=handles, labels=labels)

    plt.grid()
    plt.show()
