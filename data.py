def save_data(code):
    with open('codes.txt', 'a') as file:
        file.write(code+ '\n')

def load_data():
    try:
        with open('codes.txt', 'r') as file:
            codes = file.readlines()
            codes = [code.strip() for code in codes]
            return codes
    except FileNotFoundError:
        return []
    
    


