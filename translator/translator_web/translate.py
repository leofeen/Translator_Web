def translate(input_data: str, language: str):
    """
    Keywords are case insensitive.
    Commands are case sensitive.
    """
    output_data = ''
    language_reference = get_language_reference(language)

    # Every programm should have main block:
    # starts with 'begin' token,
    # ends with 'end' token - checking on it
    if not (input_data.upper().find(language_reference['begin']) != -1 
            and input_data.upper().find(language_reference['end']) != -1):
        raise SyntaxError('Expected main block of programm')
    input_data = input_data.split('\n')

    # Count number og lines for tracebacks
    line_count = 0

    # Parse all enters to one string in output
    input_string = ''
    first_input = True
    while input_data[0].upper().find(language_reference['begin']) == -1:
        line_count += 1
        input_string_line = input_data[0]
        input_string_line = input_string_line.strip().strip('\t')
        if input_string_line != '':
            if not input_string_line.upper().startswith(language_reference['enter']):
                raise SyntaxError(f'Unexpected keyword at line {line_count}: {input_string_line}')
            enter_keyword, string_element, number_of_repetition = input_string_line.split()
            if first_input:
                first_input = False
            else:
                input_string += ' + '
            if int(number_of_repetition) > 1:
                input_string += f'\'{string_element}\'*{number_of_repetition}'
            elif int(number_of_repetition) == 1:
                input_string += f'\'{string_element}\'' # Do not write 'a'*1
            else:
                raise SyntaxError(f'Type Error at line {line_count}: expected positive number of string element repetition, but {number_of_repetition} was given')
        del input_data[0]
    if input_string != '':
        output_data += f'string = {input_string}\n'
        output_data += '\n'

    # Every programm should have main block:
    # starts with 'begin' token,
    # ends with 'end' token - this is at least 2 lines
    if len(input_data) < 2:
        raise SyntaxError(f'Unexpected pseudocode structure after line {line_count}')

    # Parse main block of pseudocode programm
    number_of_spaces = 0
    in_while = 0
    in_if = 0
    # Trying to output good-looking code,
    # so excluding two or more blank line in a row
    previous_line_is_blank = False
    while input_data[0].upper().strip().strip('\t') != language_reference['end']:
        line_count += 1
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
                raise SyntaxError(f'Unexpected end of while block at line {line_count}')
            in_while -= 1
            if not previous_line_is_blank:
                output_data += '\n'
                previous_line_is_blank = True
        elif line.upper() == language_reference['end_if']:
            number_of_spaces -= 4
            if not in_if:
                raise SyntaxError(f'Unexpected end of if block at line {line_count}')
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
                    raise SyntaxError(f'Unexpected keyword at line {line_count}: {condition}')
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
                    raise SyntaxError(f'Unexpected keyword at line {line_count}: {condition}')
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
                    raise SyntaxError(f'Unexpected command at line {line_count}: {command}')
                args = command[len(language_reference['replace'])+1:-1].split(',')
                if len(args) != 2:
                    raise SyntaxError(f'Type Error at line {line_count}: replace command expected 2 arguments, but {len(args)} was given')
                output_data += ' '*number_of_spaces + f'string = string.replace(\'{args[0]}\', \'{args[1].strip()}\', 1)\n'
        elif line.upper().startswith(language_reference['else']):
            previous_line_is_blank = False
            output_data += ' '*(number_of_spaces-4) + 'else:\n'
            command = line[len(language_reference['else'])+1:]
            if command != '':
                if not command.startswith(language_reference['replace']):
                    raise SyntaxError(f'Unexpected command at line {line_count}: {command}')
                args = command[len(language_reference['replace'])+1:-1].split(',')
                if len(args) != 2:
                    raise SyntaxError(f'Type Error at line {line_count}: replace command expected 2 arguments, but {len(args)} was given')
                output_data += ' '*number_of_spaces + f'string = string.replace(\'{args[0]}\', \'{args[1].strip()}\', 1)\n'
        elif line.startswith(language_reference['replace']):
            previous_line_is_blank = False
            args = line[len(language_reference['replace'])+1:-1].split(',')
            if len(args) != 2:
                raise SyntaxError(f'Type Error at line {line_count}: replace command expected 2 arguments, but {len(args)} was given')
            output_data += ' '*number_of_spaces + f'string = string.replace(\'{args[0]}\', \'{args[1].strip()}\', 1)\n'
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
            raise SyntaxError(f'Unexpected keyword at line {line_count}: {line}')

        del input_data[0]
    
    # Every 'if' or 'while' token should have closing 'end_if' and
    # 'end_while' tokens respectfully
    if in_if:
        raise SyntaxError('Expected end of if block, but got EOF') # End-Of-File
    if in_while:
        raise SyntaxError('Expected end of while block, but got EOF') # End-Of-File

    return output_data

def get_language_reference(language: str):
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
    return language_reference

def get_language_description(language: str):
    if language == 'ru':
        language_description = {
            'НАЧАЛО ... КОНЕЦ': 'Операторные скобки для основного блока программы.',
            'ВВОД str number': 'Добавляет <code class="code-snippet">number</code> раз к строке для обработки подстроку <code class="code-snippet">str</code>. Может идти только перед <code class="code-snippet">НАЧАЛО</code>.',
            'нашлось(str)': 'Проверяет наличие подстроки <code class="code-snippet">str</code> в строке для обработки. Возвращает True, если подстрока найдена. Иначе возвращает False.',
            'заменить(old, new)': 'Заменяет первую слева подстроку <code class="code-snippet">old</code> на подстроку new в строке для обработки. Если подстрока old отсутствует, то команда не выполняется.',
            'ПОКА condition ... КОНЕЦ ПОКА': 'Объявление блока цикла Пока. Выполняются строки внутри блока, пока <code class="code-snippet">condition</code> возвращает True.',
            'ЕСЛИ condition ТО ... ИНАЧЕ ... КОНЕЦ ЕСЛИ': 'Объявление блока Если/То/Иначе. Если <code class="code-snippet">condition</code> возвращает True, то выполняются строка с <code class="code-snippet">ТО</code> или строки между <code class="code-snippet">ТО</code> и <code class="code-snippet">ИНАЧЕ</code>/<code class="code-snippet">КОНЕЦ ЕСЛИ</code>, иначе выполняется строка с <code class="code-snippet">ИНАЧЕ</code> или строки между <code class="code-snippet">ИНАЧЕ</code> и <code class="code-snippet">КОНЕЦ ЕСЛИ</code>, если такие присутствуют.',
            'ВЫВОД СТРОКИ': 'Печатает строку для обработки в текущем состоянии.',
            'ВЫВОД ДЛИНЫ': 'Печатает длину строки для обработки в текущем состоянии.',
            'ВЫВОД СУММЫ': 'Печатет сумму всех цифр в строке для обработки в текущем состоянии.',
            '// ...': 'Строка, начинающаяся с <code class="code-snippet">//</code>, является комментарием, не влияющим на исполнение кода.',
            'И, ИЛИ, НЕ': 'Логические операторы, использующиеся в <code class="code-snippet">condition</code> в <code class="code-snippet">ЕСЛИ</code> и <code class="code-snippet">ПОКА</code> между несколькими <code class="code-snippet">нашлось()</code>.',
        }
    elif language == 'en':
        language_description = {
            'BEGIN ... END': 'Declaration of main block of the program.',
            'ENTER str number': 'Appends substring <code class="code-snippet">str</code> to input string <code class="code-snippet">number</code> times. This must go before <code class="code-snippet">BEGIN</code> statement.',
            'find(str)': 'Check if substing <code class="code-snippet">str</code> is a part of input string. Returns True if <code class="code-snippet">str</code> was found. Returns False otherwise.',
            'replace(old, new)': 'Replace first from the left substring <code class="code-snippet">old</code> by substring <code class="code-snippet">new</code> in input string. If there is no inclusion of substring <code class="code-snippet">old</code> in input string, than nothing happens.',
            'WHILE condition ... END WHILE': 'Declaration of While block. Lines inside block will be executed, while <code class="code-snippet">condition</code> returns True.',
            'IF condition THEN ... ELSE ... END IF': 'Declaration of If/Then/Else block. If <code class="code-snippet">condition</code> returns True, then line with <code class="code-snippet">THEN</code> or lines between <code class="code-snippet">THEN</code> and <code class="code-snippet">ELSE</code>/<code class="code-snippet">END IF</code> will be executed, else line with <code class="code-snippet">ELSE</code> or lines between <code class="code-snippet">ELSE</code> and <code class="code-snippet">END IF</code> will be executed, if there is one.',
            'OUTPUT STRING': 'Print input string in current state of processing.',
            'OUTPUT LENGTH': 'Print length input string in current state of processing.',
            'OUTPUT SUM': 'Print sum of all digits in input string in current state of processing.',
            '// ...': 'Line that starts with <code class="code-snippet">//</code>, considered a сomment and does not affect program execution.',
            'AND, OR, NOT': 'Logic operands that used in <code class="code-snippet">condition</code> inside <code class="code-snippet">IF</code> and <code class="code-snippet">WHILE</code> statements between several <code class="code-snippet">find()</code>.',
        }
    else:
        raise ValueError(f'Unsopported language: {language}')
    return language_description