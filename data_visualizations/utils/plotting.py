import matplotlib.pyplot as plt
import numpy as np
import math

from io import BytesIO
import base64


# Count how many data can be converted to its highest probability of data type.
# It will be grouped by Categorical data type, and displayed it with a bar graph.
def count_per_category(df, category):
    grouped_data = df.groupby(category) # group data by categorical data type

    keys = [key for key, _ in grouped_data]
    values = grouped_data.count()

    x = np.arange(len(keys))  # the label locations
    width = 1 / (len(values.keys())+1)  # the width of the bars
    multiplier = (len(values.keys())-3) * -0.5 # adjust the first position for the label

    _, ax = plt.subplots(layout='constrained')

    max_data = 0
    for column, data in values.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, data, width, label=column)
        ax.bar_label(rects, padding=3)
        multiplier += 1
        max_data = max(max_data, max(data))

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Frequency')
    ax.set_xlabel(category)
    ax.set_xticks(x + width, keys)
    ax.legend(loc='upper right', ncols=3)
    # add 40% space from maximum height for legend
    ax.set_ylim(0, int(max_data * 1.4))

# Generate a time-based plot that display all numerical data.
def time_based_plot(df, timeframe, comparisons):
    df = df.sort_values(by=[timeframe]) # Sort the data based on datetime datatype

    min_data, max_data = math.inf, -math.inf

    # Display all numerical datatypes
    for col in comparisons:
        plt.plot(df[timeframe], df[col], linestyle='-', label=col)
        min_data = min(min_data, min(df[col]))
        max_data = max(max_data, max(df[col]))

    plt.legend(loc='upper right')
    # Set the limit of y-axis by increasing 20% of the min and max data
    plt.ylim(min_data-abs(min_data)*0.2, max_data+abs(max_data)*0.2) 

    plt.xlabel(timeframe)


# A plot to display complex number data types.
# The real value will be on the x-axis,
# and the imaginary value will be on the y-axis.
def scatter_plot_complex(df, complexes):

    for complex in complexes:
        unzip = list(zip(*df[complex])) # split the tuple into two arrays
        plt.scatter(unzip[0], unzip[1], label=complex)

    plt.legend(loc='upper right')

    plt.xlabel("Real")
    plt.ylabel("Imaginary")

# Render the plot based on plot_id
# Time-based plot for every numerical data if plot_id = 1
# Counting the data and split it for every category if plot_id = 2
# Scatter plot of real and imaginary value if plot_id = 3
def get_plot(df, plot_id):
    plt.clf()

    # Time-based plot that display all numerical value.
    if plot_id == 1:
        timeframe = ""
        comparisons = []
        for col in df:
            if df[col].dtype == "datetime64[ns]":
                timeframe = col

            if df[col].dtype == "int8" or df[col].dtype == "float32":
                comparisons.append(col)

        if timeframe != "" and len(comparisons) > 0:
            time_based_plot(df, timeframe, comparisons)

    # Categorical grouped data
    elif plot_id == 2:
        category = ""
        for col in df:
            if df[col].dtype == "category":
                category = col

        if category != "":
            count_per_category(df, category)

    # Scatter plot for complex number data type
    elif plot_id == 3:
        complex = []
        for col in df:
            if type(df[col][0]) is tuple:
                complex.append(col)

        if len(complex) > 0:
            scatter_plot_complex(df, complex)
    else:
        return

    # Render the plot as an image that will be passed to the html.
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image = buffer.getvalue()
    graph = base64.b64encode(image)
    graph = graph.decode('utf-8')
    buffer.close()

    return graph
