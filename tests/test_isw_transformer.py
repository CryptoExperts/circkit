from circkit.transformers.isw import IswOnArithmetic
from circkit.boolean import BooleanCircuit
import random

def test_isw_transformer():
    C = BooleanCircuit()
    x = C.add_input("x")
    y = C.add_input("y")

    z = x * y + 1
    t = z + x + 1
    C.add_output(t)

    # ISW transformer
    transformer = IswOnArithmetic(order=2)
    iswC = transformer.transform(C)

    # Evaluate on original circuit
    inp = [random.randint(0, 1) for _ in range(2)]
    out = C.evaluate(inp)

    # Evaluate on ISW circuit
    x_shares = [random.randint(0, 1) for _ in range(2)]
    x_shares.append(x_shares[0] ^ x_shares[1] ^ inp[0])
    y_shares = [random.randint(0, 1) for _ in range(2)]
    y_shares.append(y_shares[0] ^ y_shares[1] ^ inp[1])

    inp_shares = x_shares + y_shares
    out_shares = iswC.evaluate(inp_shares)
    ret = 0
    for s in out_shares:
        ret ^= s
    assert ret == out[0]
