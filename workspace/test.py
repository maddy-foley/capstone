item = {
    'example1': {
        'TOAL':1
    },
    'example2': {
        'TOAL':10
    },
       'example3': {
        'TOAL':100
    },
}



sorted_keys_by_value = [key for key, value in sorted(item.items(), key=lambda item: item[1]['TOAL'],reverse=True)]
print(sorted_keys_by_value)