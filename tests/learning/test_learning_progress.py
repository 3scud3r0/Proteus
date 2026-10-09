from proteus.core.agent import ProteusAgent

def test_fixed_grid_learning_is_measurable(tmp_path):
    with ProteusAgent(tmp_path,seed=7) as agent:
        before=agent.evaluate(30,seed=8100,size=5,max_steps=50)
        agent.train(220,size=5,max_steps=50,max_seconds=45)
        after=agent.evaluate(30,seed=8100,size=5,max_steps=50)
        assert after["success_rate"]>=before["success_rate"]
        assert after["success_rate"]>=0.7
