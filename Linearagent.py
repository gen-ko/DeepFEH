import DQN_implementation as dqn

identifier = "FEH linear agent"

# start training
dqn.main(identifier=identifier, model_name="linear", max_iteration=2000, epsilon=1,
         epsilon_decay=4.5e-4, epsilon_min=0.05, interval_iteration=100, gamma=1, test_size=50,
         learning_rate=0.00005, use_replay_memory=True, memory_size=50000, burn_in=10000)
