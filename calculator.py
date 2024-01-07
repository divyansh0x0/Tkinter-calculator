import math
import log


CALC_CMDS = {"+":"addition","−":"subtract","÷":"divide","×":"product","√":"square root","²":"square","!":"factorial","%":"modulo","=":"result"}
operators = list(CALC_CMDS.keys())
left_operand_operator = ["²","!"]
right_operand_operator = ["√"]
single_operand_operator = left_operand_operator + right_operand_operator
print("operators that require single operands: ", single_operand_operator)
def evaluateExpression(exp:str):
    stack = createStack(exp=exp)
    if stack == None:
        return None
    return calculateResult(stack)
    

def createStack(exp:str):
    if(exp.endswith("e")):
        return False
    log.info("Creating stack from", exp)
    stack = []
    i = 0
    exp = exp.replace("π",str(math.pi))
    # if exp[0] in "−":
    #     num = ""
    #     while exp[i] < len(exp) and (exp[i] not in operators or exp[i] in "e.−+"):
    #         if exp[i] == "−":
    #             num += "-" 
    #             i += 1
    #         elif exp[i] == "e" and exp[i+1] in "+−":
    #             num += "e" + exp[i+1]
    #             i += 2 
    #         else: 
    #             num += exp[i]
    #             i+=1    
    #     stack.append(float(num))
    #     log.info(f"negative number {num} appended to stack. Now starting from index {i}")
    #Main loop for creating a stack
    while i < len(exp):
        if exp[i] not in "(.)" and exp[i] not in operators and exp[i].isdigit() == False:
            log.error("Returning because expression contains : " + exp[i])
            return None
        if (exp[i] not in operators and exp[i] not in "()") or exp[i] == "−":
            if exp[i].isdigit() or exp[i] in ".e−":
                num=""
                k = i
                #this will extract the whole number with sign
                while i < len(exp) and (exp[i] not in operators or (exp[i] in "+−" and (num == "" or num.endswith("e")))) and (exp[i].isdigit() or exp[i] in "e.+−"):
                    if exp[i] == "−":
                        num += "-"
                    elif exp[i] == "e" and exp[i + 1] not in "+−":
                        i+=1 #skip if case like 3232e is there
                    else: 
                        num += exp[i]
                    i+=1
                f1 = float(num)
                #a + sign will be added automatically. Example if 3-2 then stack = [3,"+",-2]
                if f1 < 0 and len(stack) > 0 and exp[k-1] not in operators and exp[k-1] not in "()":
                    stack.append("+")
                stack.append(f1)
        elif exp[i] in operators or exp[i] in "()":
            #this condition will convert expressions like 3√3 into 3*√3 and 3(3) to 3 * (3)
            if (exp[i] == "√" or exp[i] == "(") and i-1 >= 0 and exp[i-1] not in operators: 
                stack.append("×")
            stack.append(exp[i])
            if exp[i] == ")" and i + 1 < len(exp) and exp[i+1] not in operators and exp[i+1] not in ")":
                stack.append("×")
            i+=1    
        else:
            i+=1
    log.success("stack created: ",stack)
    return stack


def calculateResult(stack:list):   
    try:
        i = 0
        while i < len(stack):
            curr = stack[i]
            if curr == "(":
                k = i + 1
                new_stack = []
                open_p = 0
                close_p = 0

                    
                while str(stack[k]) != ")" or close_p != open_p:
                    if str(stack[k]) == "(":
                        open_p += 1
                    if str(stack[k]) == ")":
                        close_p += 1
                    new_stack.append(stack.pop(k))
                else:
                    stack.pop(k) #remove close bracket if all values inside parenthesis have been stored in a new stack
                result =   calculateResult(new_stack)
                if result != None:
                    stack.insert(k,result)
                else:
                    return None
                
                #remove parenthesis, if there is no operator before parenthesis then replace it with *
                prev_index = i-1
                isNoOperatorBeforeParenthesis= prev_index >= 0 and str(stack[prev_index]) not in operators
                log.warn("removing open bracket", stack," at index:",prev_index, "and is operator before parenthesis=", isNoOperatorBeforeParenthesis)

                if isNoOperatorBeforeParenthesis:
                    stack.pop(i)
                    stack.insert(i,"×")
                    log.warn("replacing bracket with *",stack)
                else: 
                    stack.pop(i)
                log.success("brackets replaced: ",stack)
            else:
                i += 1
        return doPemdas(stack)
    except Exception as e:
        log.error("An error occurred: " + str(e))
        return None
#only evaluates expression without parenthesis
def doPemdas(stack: list):
    log.info("Applying pemdas order on", stack)
    square = lambda a:a**2 #0
    fact = lambda a:math.factorial(a) #1
    sqrt = lambda a:math.sqrt(a) #2
    mult = lambda a,b:a*b #3
    divide = lambda a,b:a/b #3
    modulo = lambda a,b:a%b #3
    add = lambda a,b:a+b #4
    sub = lambda a,b:a-b #4

    i = 0
    #iteration by priority which are 5 in total
    while i < 5:
        log.info("iteration number: ",i)

        k = 0
        while k < len(stack): 
            if stack[k] in operators:
                op = stack[k]
                prev_el = None
                next_el = None
                if k + 1< len(stack):
                    next_el = stack[k+1]
                if k - 1 >= 0:
                    prev_el = stack[k-1]
                if i == 0 and op == "²": #square
                    log.warn("[Square] Calculating: ",prev_el,op)
                    stack[k-1]=square(prev_el)
                    stack.pop(k)
                    k = 0
                elif i == 1 and op == "!": #factorial
                    log.warn("[Factorial] Calculating: ",prev_el,op)
                    stack[k-1] = fact(prev_el)
                    stack.pop(k)
                    k = 0
                elif i == 2 and op == "√": #square root
                    log.warn("[Sqrt] Calculating: ",op,next_el)
                    stack[k+1] = sqrt(next_el)
                    stack.pop(k)
                    k = 0
                elif i == 3: #multiply and divide have same priority
                    log.warn("[Multiply/Divide] Calculating: ",prev_el,op,next_el)
                    if op == "×":
                        stack[k] = mult(prev_el,next_el)
                        stack.pop(k+1)
                        stack.pop(k-1)
                        k = 0
                    elif op == "÷":
                        stack[k] = divide(prev_el,next_el)
                        stack.pop(k+1)
                        stack.pop(k-1)
                        k = 0
                    elif op == "%":
                        stack[k] = modulo(prev_el,next_el)
                        stack.pop(k+1)
                        stack.pop(k-1)
                        k = 0
                elif i == 4:#addition and subtraction have same priority
                    log.warn("[ADD/SUB] Calculating: ",prev_el,op,next_el)
                    if op == "+":
                        stack[k] = add(prev_el,next_el)
                        stack.pop(k+1)
                        stack.pop(k-1)
                        k = 0
                    elif op == "−":
                        stack[k] = sub(prev_el,next_el)
                        stack.pop(k+1)
                        stack.pop(k-1)
                        k = 0
            k += 1
        i+=1
    log.info("Pemdas calculation result: ", stack)
    return stack[0]
    

