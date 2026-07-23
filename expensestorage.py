import json
database="expensedatabase.json"
def load_database():
    try:
        with open(database,'r') as f:
            if f!={} or type(f)==type({}):
                data=json.load(f)
                return data
            else:
                return {}
    except FileNotFoundError:
        print("FileNotFoundError: Database is not found, creating a new one")
        return {}
    except json.JSONDecodeError:
        print("JSON file is corrupted")
        return {}
    except OSError as e:
        print(e)
        return {}
    except Exception as e:
        print(f"unexpected Error: {e}")
        return {}
    
def write_database(data):
    try:
        with open(database,'w') as f:
            json.dump(data,f,indent=4)
        return True
    except Exception as e:
        print("Error: Could not save the changes mad",e)
        return False