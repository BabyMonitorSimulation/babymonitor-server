def clean_data(data):
    data.pop("_sa_instance_state")
    try: 
        data.pop("id")
    except Exception:
        pass
    return data
