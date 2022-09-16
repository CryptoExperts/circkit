from circkit import Circuit, Operation
import random

# Define a new circuit type
class NewCircuitType(Circuit):
    class Operations(Circuit.Operations):
        class MADDC(Operation.Variadic):
            def eval(self, c, *operands):
                return [c + x for x in operands]
            
        class MMULC(Operation.Variadic):
            def eval(self, c, *operands):
                return [c * x for x in operands]

def test_new_circuit_type():
    # Create a new circuit instance
    circuit = NewCircuitType(name="test circuit")
    c = 10
    x = circuit.add_inputs(5, "x%d")
    y = circuit.MADDC()(c, *x)
    z = circuit.MMULC()(c, *x)
    circuit.add_output(y)
    circuit.add_output(z)

    # Evaluate the circuit
    inp = [random.randint(0, 2**32) for _ in range(5)]
    out = circuit.evaluate(inp)

    # Check values
    chk = [[x + c for x in inp], [x * c for x in inp]]
    assert out == chk
