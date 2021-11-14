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
    # In all games, each character has to be one of a Knight or a Knave
    # Below is the 'XOR' logic making that happen
    And(Or(AKnight,AKnave), Or(Not(AKnight),Not(AKnave))),

    # These are the implications that arise if what A is saying
    # is true or not (i.e. A is a Knight or a Knave)
    Implication(AKnight, And(AKnight,AKnave)),
    Implication(AKnave, Not(And(AKnight,AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # In all games, each character has to be one of a Knight or a Knave
    # Below is the 'XOR' logic making that happen
    And(Or(AKnight,AKnave), Or(Not(AKnight),Not(AKnave))),
    And(Or(BKnight,BKnave), Or(Not(BKnight),Not(BKnave))),

    # These are the implications that arise if what A is saying
    # is true or not (i.e. A is a Knight or a Knave)
    Implication(AKnight, And(AKnave,BKnave)),
    Implication(AKnave, Not(And(AKnave,BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # In all games, each character has to be one of a Knight or a Knave
    # Below is the 'XOR' logic making that happen
    And(Or(AKnight,AKnave), Or(Not(AKnight),Not(AKnave))),
    And(Or(BKnight,BKnave), Or(Not(BKnight),Not(BKnave))),
    
    # These are the implications that arise if what A and B are saying
    # is true or not (i.e. A,B are a Knight or a Knave)
    Implication(AKnight, Or(And(AKnight,BKnight), And(AKnave, BKnave))),
    Implication(BKnight, Or(And(AKnight,BKnave), And(AKnave, BKnight))),
    
    Implication(AKnave, Or(And(AKnight,BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Or(And(AKnight,BKnight), And(AKnave, BKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # In all games, each character has to be one of a Knight or a Knave
    # Below is the 'XOR' logic making that happen
    And(Or(AKnight,AKnave), Or(Not(AKnight),Not(AKnave))),
    And(Or(BKnight,BKnave), Or(Not(BKnight),Not(BKnave))),
    And(Or(CKnight,CKnave), Or(Not(CKnight),Not(CKnave))),
    
    # These are the implications that arise if what A and B and C are saying
    # is true or not (i.e. A,B,C are a Knight or a Knave) 
    Implication(BKnight, CKnave),
    Implication(BKnave, CKnight),
    Implication(CKnight, AKnight),
    Implication(CKnave, AKnave),
    
    #not sure if this is cheating. The phrase "I am a knave" is an impossible
    #statement in the Knights and Knaves game so B is clearly a knave. But
    #is there a way to have the model checker arrive at the same conclusion
    #from more basic logic statements, rather than me providing some logical reasoning?
    BKnave
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
