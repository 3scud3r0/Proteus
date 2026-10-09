"""Safe arithmetic expression evaluator; not arbitrary Python execution."""
import ast
import operator

BINOPS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,
        ast.FloorDiv:operator.floordiv,ast.Mod:operator.mod}
UNARY={ast.UAdd:operator.pos,ast.USub:operator.neg}

def arithmetic(expression: str) -> float:
    if len(expression)>200:raise ValueError("Expression too long")
    tree=ast.parse(expression,mode="eval")
    def visit(node,depth=0):
        if depth>20:raise ValueError("Expression too deep")
        if isinstance(node,ast.Constant) and type(node.value) in (int,float):
            if abs(node.value)>1e12:raise ValueError("Number too large")
            return node.value
        if isinstance(node,ast.UnaryOp) and type(node.op) in UNARY:
            return UNARY[type(node.op)](visit(node.operand,depth+1))
        if isinstance(node,ast.BinOp) and type(node.op) in BINOPS:
            a,b=visit(node.left,depth+1),visit(node.right,depth+1)
            if abs(a)>1e12 or abs(b)>1e12:raise ValueError("Operands too large")
            value=BINOPS[type(node.op)](a,b)
            if abs(value)>1e12:raise ValueError("Result too large")
            return value
        raise PermissionError("Only bounded arithmetic is allowed")
    return float(visit(tree.body))
