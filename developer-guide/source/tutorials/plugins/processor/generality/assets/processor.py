# Note: this processor hides specific words appearing in text in a case-insensitive manner.
# You can fill the text_to_hide lists with the words you want to hide. 

def process(row):
    
    # List of colors to hide (ensure case-insensitive)
    text_to_hide = ["example_1", "example_2", "to_fill"] 
    text_to_hide = [w.casefold() for w in colors_to_hide]
    
    # Retrieve the user-defined input column
    text_column = params["input_column"]

    # Hide colors from list
    text_list = row[text_column].split(" ")
    text_list_hide = [w if w.casefold() not in text_to_hide else "****" for w in text_list]
    
    return " ".join(text_list_hide)