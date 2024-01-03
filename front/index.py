class ExpressionInterpreter:
    def interpret(self, context):
        pass

class NumberExpression(ExpressionInterpreter):
    def interpret(self, context):
        return int(context)

class AdditionExpression(ExpressionInterpreter):
    def interpret(self, context):
        left, right = context.split('+')
        return NumberExpression().interpret(left) + NumberExpression().interpret(right)

# Kullanım
expression = "5+3"
result = AdditionExpression().interpret(expression)
print(f"{expression} = {result}")