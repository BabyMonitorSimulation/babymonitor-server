def clean_data(data):
    data.pop("_sa_instance_state")

    return data
