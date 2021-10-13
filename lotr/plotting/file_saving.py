from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def save_multiplot_to_pdf(plot_func, args_list, filename, **kwargs):
    """Function to save a list of pdfs from a plotting function and a list of arguments.

    Parameters
    ----------
    plot_func : fun
        The function to be used for plotting. Should return the Figure obj.
    args_list : list
        List of arguments with which the plotting function will be called, once per page
    filename : str or Path
        Location where the plot will be saved.

    Returns
    -------

    """
    with PdfPages(filename) as pdf:
        for args in args_list:
            fig = plot_func(*args)
            pdf.savefig(fig, **kwargs)
            plt.close(fig)
