

def test_algo():
    from margot.signals import algos

    class MyAlgo(algos.BaseAlgo):

        pass

    myalgo = MyAlgo(env={})