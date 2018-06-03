import cx_Freeze

executables = [cx_Freeze.Executable("visgraph_simulator/visgraph_simulator.py")]

cx_Freeze.setup(
    name="Visibility Graph Simulator",
    version="0.1.1",
    options={"build_exe": {"packages":["pygame", "pyvisgraph", "tqdm"]}},
    executables = executables
    )
