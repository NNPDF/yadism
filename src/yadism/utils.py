def get_mass_label(sf_name):
    """
        get_mass_label.

        Parameters
        ----------
        sf_name :
            sf_name

        .. todo::
            docs
    """
    flavour = sf_name[2:]
    if flavour == "light":
        return None
    else:
        return f"m{flavour[0]}"
