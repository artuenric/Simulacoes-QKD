def float_to_string(n):
    # Convertendo o número float para string e dividindo em parte inteira e decimal
    str_number = str(n)
    integer_part, decimal_part = str_number.split('.')
    # Concatenando a parte inteira com a vírgula e a parte decimal
    result_string = f"{integer_part},{decimal_part}" 
    return result_string