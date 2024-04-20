import pandas as pd

# A function that return True if input is a complex number, otherwise False
# Complex number formatting:
# 1. (a + bi) / (a + bj) if a and b are numerical values
# 2. (ai + b) / (aj + b) if a and b are numerical values
# 3. (a) if a is a numerical value
# 4. (ai) / (aj) if a is a numerical value
def is_complex_number(text):
    number = text.split("+")
    if len(number) == 1:
        if text[-1] in {'i', 'j'}:
            text = text[:-1]
        try:
            float(text)
            return True
        except:
            return False
    elif len(number) == 2:
        if number[0][-1] in {'i', 'j'}:
            try:
                float(number[0][:-1])
                float(number[1])
                return True
            except:
                return False
        elif number[1][-1] in {'i', 'j'}:
            try:
                float(number[1][:-1])
                float(number[0])
                return True
            except:
                return False
        else:
            return False
    else:
        return False

# Count the possibility of data types compare with others and the number of data
def infer_data_type(data):
    integer_ct = 0
    float_ct = 0
    datetime_ct = 0
    complex_ct = 0

    for e in data:

        if is_complex_number(str(e)):
            complex_ct += 1

        try:
            f = float(e)
            if f % 1 == 0:
                integer_ct += 1
            float_ct += 1
        except:
            pass

        try:
            pd.to_datetime(e)
            datetime_ct += 1
        except:
            pass

    unique_data = data.unique()
    categorical_ct = len(data) - len(unique_data)
    bool_ct = len(data) - len(unique_data) if len(unique_data) == 2 else 0.0

    confidence = {}

    # the number of integer dataset
    confidence['integer'] = integer_ct /len(data)  
    # the number of float dataset that can't be converted to integer
    confidence['float'] = (float_ct - integer_ct) / len(data)
    # the number of complex number dataset that can't be converted to float
    confidence['complex'] = (complex_ct - float_ct) / len(data)
    # the number of datetime dataset that can't be converted to float
    confidence['datetime'] = (datetime_ct - float_ct) / len(data)
    # the number of categorical dataset compared to boolean dataset
    confidence['categorical'] = (categorical_ct - bool_ct) / len(data)
    # the number of boolean dataset
    confidence['boolean'] = bool_ct / len(data)
    # everything else is an object dataset
    confidence['object'] = 1 - max(categorical_ct, complex_ct, datetime_ct) / len(data)  

    most_likely_dtype = max(confidence, key=confidence.get)

    return (most_likely_dtype, confidence[most_likely_dtype])


# Convert the dataset in Object datatype with complex number format (a, b),
# where a and b is float datatype with a being the real number and b is the imaginary number
def to_complex_number(dataframe):
    data = []

    for e in dataframe:
        number = e.split("+")
        if len(number) == 1:
            if e[-1] in {'i', 'j'}:
                e = e[:-1]
                try:
                    data.append((0, float(e)))
                except:
                    data.append((0, 0))
            else:
                try:
                    data.append((float(e), 0))
                except:
                    data.append((0, 0))
        elif len(number) == 2:
            if number[0][-1] in {'i', 'j'}:
                try:
                    data.append((float(number[1]), float(number[0][:-1])))
                except:
                    data.append((0, 0))
            elif number[1][-1] in {'i', 'j'}:
                try:
                    data.append((float(number[0]), float(number[1][:-1])))
                except:
                    data.append((0, 0))
            else:
                data.append((0, 0))
        else:
            data.append((0, 0))

    return data

# A function to infer and convert datatype based on the highest probability
def infer_and_convert_data_types(df):

    data_types = {}

    for col in df.columns:

        # Acquire the data type that such column most likely to be
        most_likely, confidence = infer_data_type(df[col])

        # Convert the data type and discard any data that does not follow the highest probability
        # Categorical and Boolean are using Categorical data type.
        # Complex number is an object; a tuple with two data (real and imaginary).
        if most_likely == 'integer':
            df[col] = pd.to_numeric(df[col], downcast='integer', errors='coerce')
        elif most_likely == 'float':
            df[col] = pd.to_numeric(df[col], downcast='float', errors='coerce')
        elif most_likely == 'complex':
            df[col] = to_complex_number(df[col])
        elif most_likely == 'datetime':
            df[col] = pd.to_datetime(df[col], format="mixed", errors='coerce')
        elif most_likely == 'categorical':
            df[col] = pd.Categorical(df[col])
        elif most_likely == 'boolean':
            df[col] = pd.Categorical(df[col])
        else:
            pass

        data_types[col] = (most_likely, confidence)

    return (df, data_types)
