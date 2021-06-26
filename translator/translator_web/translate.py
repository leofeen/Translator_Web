def translate(input_data: str, language: str):
    """
    Keywords are case insensitive.
    Commands are case sensitive.
    """
    output_data = ''
    # Languge reference keywords must be in upper case
    if language == 'ru':
        language_reference = {
            'begin': 'НАЧАЛО',
            'enter': 'ВВОД',
            'end': 'КОНЕЦ',
            'find': 'нашлось',
            'replace': 'заменить',
            'end_while': 'КОНЕЦ ПОКА',
            'end_if': 'КОНЕЦ ЕСЛИ',
            'if': 'ЕСЛИ',
            'while': 'ПОКА',
            'or': 'ИЛИ',
            'and': 'И',
            'not': 'НЕ',
            'then': 'ТО',
            'else': 'ИНАЧЕ',
            'str_out': 'ВЫВОД СТРОКИ',
            'len_out': 'ВЫВОД ДЛИНЫ',
            'sum_out': 'ВЫВОД СУММЫ',
        }
    elif language == 'en':
        language_reference = {
            'begin': 'BEGIN',
            'enter': 'ENTER',
            'end': 'END',
            'find': 'find',
            'replace': 'replace',
            'end_while': 'END WHILE',
            'end_if': 'END IF',
            'if': 'IF',
            'while': 'WHILE',
            'or': 'OR',
            'and': 'AND',
            'not': 'NOT',
            'then': 'THEN',
            'else': 'ELSE',
            'str_out': 'OUTPUT STRING',
            'len_out': 'OUTPUT LENGTH',
            'sum_out': 'OUTPUT SUM',
        }
    else:
        raise ValueError(f'Unsopported language: {language}')

    # Every programm should have main block:
    # starts with 'begin' token,
    # ends with 'end' token - checking on it
    if not (input_data.upper().find(language_reference['begin']) != -1 
            and input_data.upper().find(language_reference['end']) != -1):
        raise SyntaxError('Expected main block of programm')
    input_data = input_data.split('\n')

    # Parse all enters to one string in output
    input_string = ''
    first_input = True
    while input_data[0].upper().find(language_reference['begin']) == -1:
        input_string_line = input_data[0]
        input_string_line = input_string_line.strip().strip('\t')
        if input_string_line != '':    
            enter_keyword, string_element, number_of_repetition = input_string_line.split()
            if enter_keyword.upper() != language_reference['enter']:
                raise SyntaxError(f'Unexpected keyword: {enter_keyword}')
            if first_input:
                first_input = False
            else:
                input_string += ' + '
            if int(number_of_repetition) != 1:
                input_string += f'\'{string_element}\'*{number_of_repetition}'
            elif int(number_of_repetition) == 1:
                input_string += f'\'{string_element}\'' # Do not write 'a'*1
            else:
                raise SyntaxError(f'Expected positive number of string element\
                                    repetition, but {number_of_repetition} was given')
        del input_data[0]
    if input_string != '':
        output_data += f'string = {input_string}\n'
        output_data += '\n'

    # Every programm should have main block:
    # starts with 'begin' token,
    # ends with 'end' token - this is at least 2 lines
    if len(input_data) <= 2:
        raise SyntaxError('Unexpected pseudocode structure')

    # Parse main block of pseudocode programm
    number_of_spaces = 0
    in_while = 0
    in_if = 0
    # Trying to output good-looking code,
    # so excluding two or more blank line in a row
    previous_line_is_blank = False
    while input_data[0].upper().strip().strip('\t') != language_reference['end']:
        # Preformating line to handle parsing more easily
        line = input_data[0]
        line = line.strip().strip('\t')
        while line.find(language_reference['find'] + ' ') != -1 or line.find(language_reference['replace'] + ' ') != -1:
            line = line.replace(language_reference['find'] + ' ', language_reference['find'])
            line = line.replace(language_reference['replace'] + ' ', language_reference['replace'])

        if line.upper() == language_reference['begin']:
            pass
        elif line.startswith('//'):
            output_data += ' '*number_of_spaces + '#' + line[2:] + '\n'
        elif line.upper() == language_reference['end_while']:
            number_of_spaces -= 4
            if not in_while:
                raise SyntaxError('Unexpected end of while block')
            in_while -= 1
            if not previous_line_is_blank:
                output_data += '\n'
                previous_line_is_blank = True
        elif line.upper() == language_reference['end_if']:
            number_of_spaces -= 4
            if not in_if:
                raise SyntaxError('Unexpected end of if block')
            in_if -= 1
            if not previous_line_is_blank :
                output_data += '\n'
                previous_line_is_blank = True
        elif line.upper().startswith(language_reference['while']):
            previous_line_is_blank = False
            in_while += 1
            output_data += ' '*number_of_spaces + 'while'
            number_of_spaces += 4
            conditions = line[len(language_reference['while']):].split()
            for condition in conditions:
                if not (condition.startswith(language_reference['find']) 
                        or condition.upper() == language_reference['or']
                        or condition.upper() == language_reference['and'] 
                        or condition.upper() == language_reference['not']):
                    raise SyntaxError(f'Unexpected keyword: {condition}')
                if condition.upper() == language_reference['or']:
                    output_data += ' or'
                elif condition.upper() == language_reference['and']:
                    output_data += ' and'
                elif condition.upper() == language_reference['not']:
                    output_data += ' not'
                else:
                    arg = condition[len(language_reference['find'])+1:-1]
                    output_data += f' string.find(\'{arg}\') != -1'
            output_data += ':\n'
        elif line.upper().startswith(language_reference['if']):
            previous_line_is_blank = False
            in_if += 1
            output_data += ' '*number_of_spaces + 'if'
            number_of_spaces += 4
            conditions = line[len(language_reference['if']):].split()
            for condition in conditions:
                if not (condition.startswith(language_reference['find']) 
                        or condition.upper() == language_reference['or']
                        or condition.upper() == language_reference['and'] 
                        or condition.upper() == language_reference['not']):
                    raise SyntaxError(f'Unexpected keyword: {condition}')
                if condition.upper() == language_reference['or']:
                    output_data += ' or'
                elif condition.upper() == language_reference['and']:
                    output_data += ' and'
                elif condition.upper() == language_reference['not']:
                    output_data += ' not'
                else:
                    arg = condition[len(language_reference['find'])+1:-1]
                    output_data += f' string.find(\'{arg}\') != -1'
            output_data += ':\n'
        elif line.upper().startswith(language_reference['then']):
            previous_line_is_blank = False
            command = line[len(language_reference['then'])+1:]
            if command != '':
                if not command.startswith(language_reference['replace']):
                    raise SyntaxError(f'Unexpected command: {command}')
                args = command[len(language_reference['replace'])+1:-1].split(', ')
                if len(args) != 2:
                    raise SyntaxError(f'Replace command expected 2 arguments, but {len(args)} was given')
                output_data += ' '*number_of_spaces + f'string = string.replace(\'{args[0]}\', \'{args[1]}\', 1)\n'
        elif line.upper().startswith(language_reference['else']):
            previous_line_is_blank = False
            output_data += ' '*(number_of_spaces-4) + 'else:\n'
            command = line[len(language_reference['else'])+1:]
            if command != '':
                if not command.startswith(language_reference['replace']):
                    raise SyntaxError(f'Unexpected command: {command}')
                args = command[len(language_reference['replace'])+1:-1].split(', ')
                if len(args) != 2:
                    raise SyntaxError(f'Replace command expected 2 arguments, but {len(args)} was given')
                output_data += ' '*number_of_spaces + f'string = string.replace(\'{args[0]}\', \'{args[1]}\', 1)\n'
        elif line.startswith(language_reference['replace']):
            previous_line_is_blank = False
            args = line[len(language_reference['replace'])+1:-1].split(', ')
            if len(args) != 2:
                raise SyntaxError(f'Replace command expected 2 arguments, but {len(args)} was given')
            output_data += ' '*number_of_spaces + f'string = string.replace(\'{args[0]}\', \'{args[1]}\', 1)\n'
        elif line.upper() == language_reference['str_out']:
            previous_line_is_blank = False
            output_data += ' '*number_of_spaces + 'print(string)\n'
        elif line.upper() == language_reference['len_out']:
            previous_line_is_blank = False
            output_data += ' '*number_of_spaces + 'print(len(string))\n'
        elif line.upper() == language_reference['sum_out']:
            previous_line_is_blank = False
            output_data += ' '*number_of_spaces + 'summ = 0\n'
            output_data += ' '*number_of_spaces + 'for element in string:\n'
            output_data += ' '*(number_of_spaces + 4) + 'if element.isnumeric(): summ += int(element)\n'
            output_data += ' '*number_of_spaces + 'print(summ)\n'
        else:
            raise SyntaxError(f'Unexpected keyword: {line}')

        del input_data[0]
    
    # Every 'if' or 'while' token should have closing 'end_if' and
    # 'end_while' tokens respectfully
    if in_if:
        raise SyntaxError('Expected end of if block, but got EOF') # End-Of-File
    if in_while:
        raise SyntaxError('Expected end of while block, but got EOF') # End-Of-File

    return output_data