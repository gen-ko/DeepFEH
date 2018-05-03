import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse
import numpy as np


def load_data(data_path, data_mode):
    with open(data_path, 'r') as f:
        contents = f.readlines()
    mean = []
    std = []
    K = 0
        
    if data_mode == 'q2':
        line = contents[0].strip('\n').split(sep=' ')
        assert line[0] == 'K'
        assert line[1] == '='
        K = int(line[2])
    
        for line in contents[1:-1]:
            line = line.strip('\n').split(sep=' ')
            if line[0] == 'r':
                assert line[1] == '='
                mean.append(float(line[2]))
                assert line[3] == '+-'
                std.append(float(line[4]))
    elif data_mode == 'q3':
        line = contents[0].strip('\n').split(sep=' ')
        assert line[0] == 'K'
        assert line[1] == '='
        K = int(line[2])

        for line in contents[1:-1]:
            line = line.strip('\n').split(sep=' ')
            if line[0] == 'r':
                assert line[1] == '='
                mean.append(float(line[2]))
                assert line[3] == '+-'
                std.append(float(line[4]))
            elif line[0] == 'episode':
                assert line[2] == 'r'
                assert line[3] == '='
                mean.append(float(line[4]))
                assert line[5] == '+-'
                std.append(float(line[6]))
                
    return K, mean, std


def plot_data(save_path, K, mean, std):
    matplotlib.use('Agg')
    plt.figure(0)
    plt.xlabel('Episode')
    plt.ylabel('Cumulative Reward')
    x = np.arange(0, len(mean) * K, K)
    plt.errorbar(x=x, y=mean, yerr=std)
    plt.savefig(save_path)
    return 
                

def parse_args():
    # Command-line flags are defined here.
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', dest='data_path', type=str, default='./saved_data/q2_train.txt')
    parser.add_argument('--data_mode', dest='data_mode', type=str, default='q2')
    parser.add_argument('--save_path', dest='save_path', type=str, default='./saved_figures/q2.png')
    return parser.parse_args()


def main():
    args = parse_args()
    data_path = args.data_path
    data_mode = args.data_mode
    save_path = args.save_path
    data = load_data(data_path, data_mode)
    plot_data(save_path, *data)
    return
    


if __name__ == "__main__":
    main()