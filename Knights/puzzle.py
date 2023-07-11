from logic import And, Not, Or, Symbol
from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Not(And(AKnight, AKnave)), # A cannot be both a knight and a knave
    Implication(AKnight, And(AKnight,AKnave)), #if A is a Knight then A is both a knight and a knave
    Implication(AKnave, Not(And(AKnight, AKnave))) # if A is a knave then A is not a knight and a knave
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Or(BKnight, BKnave),  # B is either a knight or a knave
    Not(And(BKnight, BKnave)),  # B cannot be a knight and a knave
    Not(And(AKnight, AKnight)),  # A cannot be a knight and a knight
    Implication(AKnight, And(AKnave, BKnave)), #if A is a knight then A is a knave and B is a knave
    Implication(AKnave, Not(And(AKnave, BKnave))) #if A is a knave then A is not a knave and b is not a knave
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Or(BKnight, BKnave),  # B is either a knight or a knave
    Not(And(AKnight, AKnave)),  # A cannot be a knight and a knave
    Not(And(BKnave, BKnight)),  # B cannot be a knave and a knight
    Implication(AKnight, Or(And(AKnight,BKnight), And(AKnave, BKnave))), # If A is a knight, then A and B have the same kind
    Implication(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))), # If B is a knight, then A and B have different kinds
    Implication(AKnave, Not( Or(And(AKnight,BKnight), And(AKnave, BKnave)))), #if A is knave then A and B don't have the same type
    Implication(BKnave, Not(Or(And(AKnave, BKnight), And(AKnight, BKnave)))), #if B is a kanve then A and B are not different
)


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Or(BKnight, BKnave),  # B is either a knight or a knave
    Or(CKnight, CKnave),  # C is either a knight or a knave
    Implication(AKnight, Or(AKnight, AKnave)),  # If A is a knight, then A's statement is true
    Implication(AKnave, Not(Or(AKnight, AKnave))),  # If A is a knave, then A's statement is false
    Implication(BKnight, Biconditional(AKnight, AKnave)),  # If B is a knight, then A's statement is "I am a knave"
    Implication(BKnave, Not(Biconditional(AKnight, AKnave))),  # If B is a knave, then A's statement is not "I am a knave"
    Implication(BKnight, CKnave),  # If B is a knight, then C is a knave
    Implication(BKnave, Not(CKnave)),  # If B is a knave, then C is not a knave
    Implication(CKnight, AKnight)  # If C is a knight, then A is a knight
)




def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
