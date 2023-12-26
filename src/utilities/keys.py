import base64

def get_project_id(encoded_str):
    # Decode the Base64 encoded string
    decoded_bytes = base64.b64decode(encoded_str)
    
    # Convert bytes to a string
    decoded_str = decoded_bytes.decode('utf-8')

    # Split the string by '$'
    split_values = decoded_str.split('$')

    # Retrieve the second value if it exists
    if len(split_values) > 1:
        return split_values[1]
    else:
        raise Exception("Invalid API Key provided.")