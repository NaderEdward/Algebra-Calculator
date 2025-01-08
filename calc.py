import re

def main():
    print("Welcome to the Algebra Solver! | For help enter 'Help' in mode")
    mode = input("Mode: ")
    if mode == "Help":
        print("Mode 1: one variable in the form:")
        print("5 ^ 2 - (4 + 3) / 6 * 4 + 3x^2 = 3000 / 7 || variable must be the last term")
        print("Mode 2: quadratic equation in the form:")
        print("2x^2 - x + 3 = 10")
        print("Arethmatic actions avalible: \n| addition/subtraction: +|- \n| multiplication/division: *|/\n| exponentiation: ^\n| parentheses: ()")
        print("Imaginary numbers are not supported")
        exit()
    response = input("Equation: ")
    components = parse_response(response, mode)
    first_half, second_half, variable = components
    sumable_terms_1, sumable_terms_2 = simplify_halves(*components)
    left_expression = form_expression(sumable_terms_1)
    right_expression = form_expression(sumable_terms_2)
    simplified_equation_components = get_var_alone(first_half, variable, left_expression, right_expression)
    variable, x = get_var_value(*simplified_equation_components)
    if x is not None: print(str(variable) + " = " +  str(x))
    else: print("No solution found.")
def parse_response(response, mode):
    if mode not in ["1", "2"]:
        print("Invalid mode. Please choose between Mode 1 or Mode 2.")
        exit()
    if mode == "1":
        # Check if response contains parentheses
        parentheses_expressions = []
        temp_response = response
        for c in temp_response:
            expression = []
            if c == '(':
                for l in temp_response[temp_response.index(c)+1:]:
                    if l == ')':
                        temp_response = temp_response.replace(l, " ", 1)
                        parentheses_expressions.append(expression)
                        break
                    else:
                        if l != " ":
                            expression.append(str(l))
                temp_response = temp_response.replace(c, " ", 1)
        for expression in parentheses_expressions:
            final_e = ""
            for c in expression:
                if expression.index(c) != len(expression)-1:
                    final_e += str(c) + " "
                else:
                    final_e += str(c)
            value = form_expression(expression)
            response = response.replace(f"({final_e})", str(value))
        try: # Split equation into its terms and find variable term 
            components = response.split("=")
            first_half = components[0].split(" ")
            second_half = components[1].split(" ")
            variable_term = ""
            for term in first_half:
                if any(c.isalpha() for c in term):
                    variable_term = term
            for term in second_half:
                if any(c.isalpha() for c in term):
                    variable_term = term 
        except:
            print("Invalid equation. Please try again.")
            return False
        return first_half, second_half, variable_term
    else:
        # Find the x^2 term, x term, and rearange the equation to make it quadratic
        x_2_term = re.search("\d?[a-zA-Z]+\^2", response)
        x_term = re.search("\d?[a-zA-Z]+", response)
        if x_2_term is None or x_term is None:
            print("Invalid equation. Please try again.")
            exit()
        x_2_term = x_2_term.group()
        x_term = x_term.group()
        components = response.split("=")
        if x_2_term in components[0]:
            if components[1].strip() != "0" or len(components[1]) != 1:
                if x_term in components[1]:
                    components[1] = components[1].replace(f" {x_term} ", "")
                    components[0] += f"- {x_term}"
                else:
                    print("Invalid equation. Please try again.")
            second_half_terms = components[1].split(" ")
            if len(second_half_terms) % 2 == 0:
                second_half_terms.pop(0)
            value = form_expression(second_half_terms, 2)
            if value < 0:
                value = -value
                components[0] += " + " + str(value)
            else:
                components[0] += " - " + str(value)
            x_1, x_2 = quadratic_equation(x_2_term, x_term, components[0])
            var = x_2_term[1]
            print(f"{var} = {x_1}")
            print("Or")
            print(f"{var} = {x_2}")
            exit()
        else: 
            if components[1].strip() != "0" or len(components[1]) != 1:
                if x_term in components[0]:
                    components[1] = components[1].replace(f" {x_term} ", "")
                    components[0] += f"- {x_term}"
                else:
                    print("Invalid equation. Please try again.")
            first_half_terms = components[0].split(" ")
            if len(first_half_terms) % 2 == 0:
                first_half_terms.pop(0)
            value = form_expression(first_half_terms, 2)
            if value < 0:
                value = -value
                components[0] += " + " + str(value)
            else:
                components[0] += " - " + str(value)
            x_1, x_2 = quadratic_equation(x_2_term, x_term, components[0])
            var = x_2_term[1]
            print(f"{var} = {x_1}")
            print("Or")
            print(f"{var} = {x_2}")
            exit()
    
def simplify_halves(first_half, second_half, variable_term):
    # Remove variable and its operations
    if variable_term in first_half:
        i = first_half.index(variable_term)
        first_half.pop(i-1) # Pop to remove specific index not first occurrence
        first_half.remove(variable_term)
    else:
        i = second_half.index(variable_term)
        second_half.pop(i-1) # Pop to remove specific index not first occurrence
        second_half.remove(variable_term)
        
    # Simplify remaining terms
    sumable_terms_1 = [] # list of terms that can be simplified
    sumable_terms_2 = []
    for term in first_half:
        if term != '':
            sumable_terms_1.append(term)
    for term in second_half:
        if term != '':
            sumable_terms_2.append(term)
    return sumable_terms_1, sumable_terms_2

def form_expression(terms, mode=1):
    terms_used = set()
    final = 0
    if mode == 2:
        if len(terms) == 2:
            final = float(terms[0] + terms[1])
            return final
    if len(terms) == 1: # check that there is more than one term
        total = float(terms[0])
        return total
    for term in find_operators(terms):
        i = terms.index(term)
        if i == 1:
            insert_index = 0
        else:
            insert_index = terms[i-2]
        try:
            int_1 = float(terms[i-1]) # use positional argument based on term's position to get 2 surrounding integers
            int_2 = float(terms[i+1])
            terms_used.add(i)
            final = calculate(int_1, term, int_2)
            if final == None: exit()
            terms.pop(i+1) # Remove used terms
            terms.pop(i-1)
            terms.pop(i-1) # Remove operator
            try:
                terms.insert(terms.index(insert_index)+1, str(final)) # insert result back into list at the same position as the used terms
            except ValueError:
                terms.insert(0, str(final)) # if insert_index == 0
        except IndexError:
            break # all terms already used
    if len(terms) > 1:
        final = form_expression(terms) 
    return final # to account for index difference

def calculate(int_1, operation, int_2): # calculate the operations form the expressions
    try:
        if operation == '+':
            return int_1 + int_2
        elif operation == '-':
            return int_1 - int_2
        elif operation == '*':
            return int_1 * int_2
        elif operation == '/':
            return int_1 / int_2
        elif operation == '^':
            return int_1 ** int_2
        elif operation == "^/":
            return float(round(float(int_1) ** (1. / float(int_2)), 3))
        else:
            print("Invalid operation.")
            return None
    except (TypeError, ZeroDivisionError):
        print("Error: Division by zero or negative root computed.")
        return None

def find_operators(terms): # find all operators and arrange them by order of operations
    operators = ["^/","^", "*", "/", "+", "-"]
    terms_opps = [term for term in terms if term in operators]
    sorted_opps = []
    opp_nums = [0, 0, 0, 0, 0, 0]
    for opp in terms_opps:
        if opp == "^/":
            opp_nums[0] = opp_nums[0] + 1
        elif opp == "^":
            opp_nums[1] = opp_nums[1] + 1
        elif opp == "*":
            opp_nums[2] = opp_nums[2] + 1
        elif opp == "/":
            opp_nums[3] = opp_nums[3] + 1
        elif opp == "+":
            opp_nums[4] = opp_nums[4] + 1
        elif opp == "-":
            opp_nums[5] = opp_nums[5] + 1
    total_opps = sum(opp_nums)
    while total_opps != 0: # loop over the opperators until all are sorted based on PEMDAS
        for opp in terms_opps:
            if opp == "^/":
                sorted_opps.append(opp)
                opp_nums[0] = opp_nums[0] - 1
                total_opps -= 1
                terms_opps.remove(opp)
            elif opp == "^":
                if opp_nums[0] == 0:
                    sorted_opps.append(opp)
                    opp_nums[1] = opp_nums[1] - 1
                    total_opps -= 1
                    terms_opps.remove(opp)
            elif opp == "*":
                if opp_nums[0] == 0 and opp_nums[1] == 0:
                    sorted_opps.append(opp)
                    opp_nums[2] = opp_nums[2] - 1
                    total_opps -= 1
                    terms_opps.remove(opp)
            elif opp == "/":
                if opp_nums[0] == 0 and opp_nums[1] == 0:
                    sorted_opps.append(opp)
                    opp_nums[3] = opp_nums[3] - 1
                    total_opps -= 1
                    terms_opps.remove(opp)
            elif opp == "+":
                if opp_nums[0] == 0 and opp_nums[1] == 0 and opp_nums[2] == 0 and opp_nums[3] == 0:
                    sorted_opps.append(opp)
                    opp_nums[4] = opp_nums[4] - 1
                    total_opps -= 1
                    terms_opps.remove(opp)
            elif opp == "-":
                if opp_nums[0] == 0 and opp_nums[1] == 0 and opp_nums[2] == 0 and opp_nums[3] == 0:
                    sorted_opps.append(opp)
                    opp_nums[5] = opp_nums[5] - 1
                    total_opps -= 1
                    terms_opps.remove(opp) 
    return sorted_opps

def get_var_alone(first_half, variable_term, left_expression, right_expression):
    if variable_term in first_half:
        variable_term_value = left_expression - right_expression
    else:
        variable_term_value = right_expression - left_expression
    return variable_term, variable_term_value

def get_var_value(var_term, var_term_value):
    var_opperations = []
    temp_var_term = var_term
    for c in enumerate(var_term):
        if not(c[1].isalpha()):
            if c[1].isdigit() and var_term[c[0]-1] != "^":
                var_opperations.append("/ " + c[1])
                temp_var_term = temp_var_term.removeprefix(c[1])
            if c[1] == "^":
                var_opperations.append("^/ " + var_term[c[0]+1])
                temp_var_term = temp_var_term.removesuffix("^" + var_term[c[0]+1])
        else: var = c[1]
    for opp in var_opperations:
        try:
            if "^/" in opp:
                var_term_value = float(round(var_term_value ** (1 / float(opp.split("/")[-1])), 3))
            else:
                var_term_value = calculate(var_term_value, opp[0], float(opp[2:]))
        except (TypeError, ZeroDivisionError):
            print("Error: Division by zero or negative root computed.")
            return None
    return var, var_term_value

def quadratic_equation(x_2, x, equation):
    # Implements the quadratic equation to solve for 2 values of x
    a = float(x_2[0])
    b = float(x[0])
    c = equation[10:]
    if c[0] == "+":
        c = float(c[1:])
    else:
        c = -float(c[1:])
    try:
        x_1 = round((-b + (((b*b)-(4*a*c)) ** (1. / float(2)))) / (2*a), 5)
        x_2 = round((-b - (((b*b)-(4*a*c)) ** (1. / float(2)))) / (2*a), 5)
    except TypeError:
        print("Error: Division by zero or negative root computed.")
        exit()
    return -x_1, -x_2
    
main() # Start program