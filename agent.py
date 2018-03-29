import DQN_implementation as dqn
from dqn import deep_qn
import tensorflow as tf

identifier = "FEH MLP agent"

# start training
dqn.main(identifier=identifier, model_name="MLP", max_iteration=100000, epsilon=0.5,
         epsilon_decay=4.5e-4, epsilon_min=0.05, interval_iteration=1000, gamma=0.99, test_size=20,
         learning_rate=0.0001, use_replay_memory=True, memory_size=50000, burn_in=10000)



def train(args=None):
    gpu_ops = tf.GPUOptions(allow_growth=True)
    config = tf.ConfigProto(gpu_options=gpu_ops, log_device_placement=False)
    sess = tf.Session(config=config)
    args_test = copy.copy(args)
    args_test.use_monitor = False
    env = EnvWrapper(args.env, mod_r=True)
    env_test = EnvWrapper(args.env, mod_r=False)


    if args.use_mr:
        print('Set experience replay ON')
    else:
        print('Set experience replay OFF')


    path = './tmp/burn_in_' + args.env + '-' + str(args.mr_capacity) + '.pickle'
    if os.path.exists(path):
        print('Found existing burn_in memory replayer, load...')
        with open(path, 'rb') as f:
            mr = pickle.load(file=f)
    else:
        mr = MemoryReplayer(env.state_shape, capacity=args.mr_capacity, enabled=args.use_mr)
        # burn_in
        mr = utils.burn_in(env, mr)


    # set type='v1' for linear model, 'v3' for three layer model (two tanh activations)

    # type='v5' use dual

    print('Set Q-network version: ', args.qn_version)
    qn = DeepQN(state_shape=env.state_shape, num_actions=env.num_actions, gamma=args.gamma, type=args.qn_version)

    qn.reset_sess(sess)

    qn.set_train(args.lr)



    if not args.reuse_model:
        print('Set reuse model      OFF')
        init = tf.global_variables_initializer()
        sess.run(init)
    else:
        print('Set reuse model      ON')
        try:
            qn.load('./tmp/qn-' + args.qn_version + '-' + args.env + '-keyinterrupt' + '.ckpt')
            optimizer_scope = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, "optimizer")
            init = tf.variables_initializer(optimizer_scope)
            sess.run(init)
            print('Found previous model')
        except tf.errors.NotFoundError:
            print('No previous model found, init new model')
            init = tf.global_variables_initializer()
            sess.run(init)

    # plotter = Plotter(save_path=args.performance_plot_path, interval=args.performance_plot_interval,
    #                   episodes=args.performance_plot_episodes)


    pretrain_test = Tester(qn, env_test, report_interval=100)
    print('Pretrain test:')
    pretrain_test.run(qn, sess)
    print('Pretrain test done.')

    tester_1 = Tester(qn, env, episodes=args.performance_plot_episodes,
                         report_interval=args.performance_plot_episodes, title='test-r-mod')
    tester_2 = Tester(qn, env_test, episodes=args.performance_plot_episodes,
                         report_interval=args.performance_plot_episodes, title='test-r-real')


    score = deque([], maxlen=args.performance_plot_episodes)
    reward_record = []

    try:
        for epi in range(args.max_episodes):
            s = env.reset()

            done = False

            rc = 0

            while not done:
                a = qn.select_action_eps_greedy(get_eps(epi), s)
                a_ = a[0]
                s_, r, done, _ = env.step(a_)
                mr.remember(s, s_, r, a_, done)
                s = s_
                rc += r
            score.append(rc)
            # replay
            s, s_, r, a, done = mr.replay(batch_size=args.batch_size)
            qn.train(s, s_, r, a, done)

            if (epi + 1) % args.performance_plot_interval == 0:
                print('train-r-mod reward avg: ', np.mean(score))
                tester_2.run(qn, sess)
                #r_avg, _ = tester_2.run(qn, sess)
                # reward_record.append(r_avg)
    except KeyboardInterrupt:
        qn.save('./tmp/qn-' + args.qn_version + '-' + args.env + '-keyinterrupt' + '.ckpt')
        # save mr

        with open(path, 'wb+') as f:
            pickle.dump(mr, f)
        exit(-1)


    qn.save(args.model_path)
    f = open(args.log_name, 'w')
    f.write(str(reward_record))
    f.close()
    return


def main():
    ns = 48
    na = 4
    dqn = deep_qn(state_shape=ns+na, num_actions=1)
    sess =