# 1.5 非定常問題 p.30


import numpy as np
import matplotlib.pyplot as plt
from bandit import Agent


class NonStatBandit:
    def __init__(self, arms=10):
        self.arms = arms
        self.rates = np.random.rand(arms)
    
    def play(self, arm):
        rate = self.rates[arm]
        
        # 非定常化のためのノイズ
        self.rates += 0.1 * np.random.randn(self.arms)

        if rate > np.random.rand():
            return 1
        else:
            return 0


class AlphaAgent:
    def __init__(self, epsilon, alpha, actions=10):
        self.epsilon = epsilon
        self.Qs = np.zeros(actions)
        self.alpha = alpha
        
    def update(self, action, reward):
        self.Qs[action] += self.alpha * (reward - self.Qs[action])
    
    # epsilonの割合でランダムな行動を取る
    # それ以外は常に最適な行動を取る
    def get_action(self):
        if np.random.rand() < self.epsilon:
            return np.random.randint(0, len(self.Qs))
        return np.argmax(self.Qs)


if __name__ == '__main__':
    runs = 200
    steps = 1000
    epsilon = 0.1
    alpha = 0.8
    agent_types = ['sample average', 'alpha const update']
    results = {}

    for agent_type in agent_types:
        
        # (200, 1000)の配列
        # Agentごとに作成
        all_rates = np.zeros((runs, steps))

        for run in range(runs):
            if agent_type == 'sample average':
                agent = Agent(epsilon)
            else:
                agent = AlphaAgent(epsilon, alpha)
        
            bandit = NonStatBandit()
            total_reward = 0
            rates = []

            for step in range(steps):
                action = agent.get_action()
                reward = bandit.play(action)
                agent.update(action, reward)
                total_reward += reward
                rates.append(total_reward / (step+1))
        
            all_rates[run] = rates
    
        avg_rates = np.average(all_rates, axis=0)
        results[agent_type] = avg_rates
    
    # plot
    plt.figure()
    plt.ylabel('Average Rates')
    plt.xlabel('Steps')
    for key, avg_rates in results.items():
        plt.plot(avg_rates, label=key)
    plt.legend()
    plt.savefig('NonStatBandit.png')

    plt.clf()
    plt.close()