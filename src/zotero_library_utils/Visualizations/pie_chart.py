import matplotlib.pyplot as plt

def pie_chart(counts_dict: dict, num_slices: int = 20):
    """Visualize a pie chart given a counts dictionary."""
    total_count = sum([v for v in counts_dict.values()])

    # Get the top num_slices
    counts_dict_top = {}
    for slice_num, slice_name in enumerate(counts_dict.keys()):
        if slice_num >= num_slices:
            break
        slice_name = counts_dict_top[slice_name]
        counts_dict_top[slice_name] = counts_dict[slice_name] / total_count

    labels = [k for k in counts_dict_top.keys()]
    values = [v for v in counts_dict_top.values()]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels)