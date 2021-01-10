def clean_data(data):
    try: 
        data.pop("_sa_instance_state")
    except: 
        pass
    return data
