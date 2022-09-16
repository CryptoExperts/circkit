from circkit import Circuit, Operation
import random

# Define a new circuit type
class NewCircuitType(Circuit):
    class Operations(Circuit.Operations):
        class MADD(Operation.Variadic):
            def eval(self, *operands):
                return sum(operands)
            
        class MMUL(Operation.Variadic):
            def eval(self, *operands):
                r = 1
                for x in operands:
                    r *= x
                return r

def test_new_circuit_type():
    # Create a new circuit instance
    circuit = NewCircuitType(name="test circuit")
    x = circuit.add_inputs(5, "x%d")
    y = circuit.MADD()(*x)
    z = circuit.MMUL()(*x)
    circuit.add_output(y)
    circuit.add_output(z)

    # Evaluate the circuit
    inp = [random.randint(0, 2**16) for _ in range(5)]
    out = circuit.evaluate(inp)

    chk_madd = sum(inp)
    chk_mmul = 1
    for v in inp:
        chk_mmul *= v
    chk = [chk_madd, chk_mmul]
    assert out == chk