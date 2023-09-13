import requests
import time
import readdata as rd
def send_data(folder, title):

    date_text = f"{time.localtime().tm_mon}.{time.localtime().tm_mday}.{time.localtime().tm_year} "
    
    url = f'https://script.google.com/a/macros/mhrd.org/s/AKfycbzO2-sg-cXobFh8xnLJsxnsT5bIn_Y7Y66bDSkPLwFYB7id3WJUVtMa2n03ZllKmVU/exec'#?action=create&folder={folder}&title={title}&date={date_text}'

    data_dictionary = {
        'action':'create',
        'folder':folder,
        'title': title,
        'key':rd.get_api_key(),
        'date': date_text
    }
    x = requests.post(url, data=data_dictionary)
    return (eval(x.text)['link'])

send_data('BIO', 'x')