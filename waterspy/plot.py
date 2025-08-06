from pandas import DataFrame
import re


def assign_marker(name, pattern_dict):
    for pattern, marker in pattern_dict.items():
        if re.search(pattern, name):
            return marker
    return '.'  # default marker if no patterns match


def assign_color(name, color_dict):
    for pattern, color in color_dict.items():
        if re.search(pattern, name):
            return color
    return '.'  # default marker if no patterns match


def fmt_triangle_piper(df: DataFrame, 
                       label: str = 'station',
                       color: str = 'black',
                       marker: str = 'o',
                       size: int = 30,
                       alpha: float = 0.7,
                       convert_alkalinity: bool = False,
                       **kwargs) -> DataFrame:
    
    """Format a dataframe for plotting in a Piper triangle plot with WQChartPy.

    Args:
        df (DataFrame): A dataframe with columns for cations and anions.
        label (str, optional): A column in the dataframe used as label for the data. Defaults to 'station'.
        color (str, optional): A column in the dataframe used as color for the data. Defaults to 'black'.
        marker (str, optional): A column in the dataframe used as marker for the data. Defaults to 'o'.
        size (int, optional): A column in the dataframe used as size for the data. Defaults to 30.
        alpha (float, optional): A column in the dataframe used as alpha for the data. Defaults to 0.7.
        convert_alkalinity (bool, optional): If True, convert alkalinity to HCO3. Defaults to False.

    Keyword Args:
        color_dict (dict, optional): Dictionaty containing regular expressions to match the station name and colors for the markers.
        marker_dict (dict, optional): Dictionaty containing regular expressions to match the station name and markers for the markers.

    Returns:
        DataFrame: A dataframe with columns for cations and anions formatted for plotting in a Piper triangle plot with WQChartPy.


    Example:
        >>> df = fmt_triangle_piper(df, label='station', color='black', marker='o', size=30, alpha=0.7, convert_alkalinity=False)
    """
    
    # check if dataframe has required columns. If not, add them.
    if "Label" not in df.columns:
        df["Label"] = df[label]
    if "Color" not in df.columns:
        if "color_dict" in kwargs:
            color_dict = kwargs['color_dict']
            df['Color'] = df['Label'].apply(lambda x: assign_color(x, color_dict))
        else:
            df["Color"] = color
    if "Marker" not in df.columns:
        if "marker_dict" in kwargs:
            marker_dict = kwargs['marker_dict']
            df['Marker'] = df['Label'].apply(lambda x: assign_marker(x, marker_dict))
        else:
            df["Marker"] = marker
    if "Size" not in df.columns:
        df["Size"] = size
    if "Alpha" not in df.columns:
        df["Alpha"] = alpha
    if "CO3" not in df.columns:
        df["CO3"] = 0
    # if Alkalinity is given assume that it is the same as HCO3
    if "Alkalinity" in df.columns:
        if convert_alkalinity:
            df['Alkalinity'] = df['Alkalinity'] * 61.0168
        df.rename(columns={'Alkalinity': 'HCO3'}, inplace=True)

    return df
