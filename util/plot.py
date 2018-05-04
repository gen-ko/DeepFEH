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
    K = 500
        
    if data_mode == 'q2':
        line = contents[0].strip('\n').split(sep=' ')
    
        for line in contents[1:-1]:
            line = line.strip('\n').split(sep=' ')
            if line[0] == 'r':
                assert line[1] == '='
                mean.append(float(line[2]))
                assert line[3] == '+-'
                std.append(float(line[4]))
    elif data_mode == 'q3':
        line = contents[0].strip('\n').split(sep=' ')

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
    #plt.errorbar(x=x, y=mean, yerr=std)
    plt.plot(x, mean)
    plt.savefig(save_path)
    return 
                

def parse_args():
    # Command-line flags are defined here.
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', dest='data_path', type=str, default='N/A')
    parser.add_argument('--data_mode', dest='data_mode', type=str, default='q3')
    parser.add_argument('--save_path', dest='save_path', type=str, default='N/A')
    return parser.parse_args()


def main():
    args = parse_args()
    data_path = args.data_path
    data_mode = args.data_mode
    save_path = args.save_path
    if data_path == 'N/A':
        data_path = input(f'''data path: (current path: {__file__})''')
    if save_path == 'N/A':
        save_path = input(f'''save path: (current path: {__file__})''')
    data = load_data(data_path, data_mode)
    plot_data(save_path, *data)
    return
    


if __name__ == "__main__":
    main()