"""
前向传播 + 反向传播
bs/N： 一般用来表示批次的大小，也就是一个批次中有多少的样本
"""
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding='utf-8')

class BPNeuralNetwork:
    def __init__(self, input_size=2, hidden_size=3, output_size=2, learning_rate=0.5):
        """
        初始化神经网络
        :param input_size: 输入层大小
        :param hidden_size: 隐藏层大小
        :param output_size: 输出层大小
        :param learning_rate: 学习率
        """
        # 网络结构参数
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.lr = learning_rate
        
        # 初始化权重和偏置
        self.w1 = np.random.randn(input_size, hidden_size) * 0.1
        self.b1 = np.zeros(hidden_size)
        self.w2 = np.random.randn(hidden_size, output_size) * 0.1
        self.b2 = np.zeros(output_size)
        
        # 记录训练历史
        self.losses = []
        self.train_history = {
            'losses': [],
            'accuracies': []
        }

    def sigmoid(self, x):
        """sigmoid激活函数"""
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        """sigmoid导数"""
        return x * (1 - x)

    def forward(self, x, y=None):
        """
        前向传播
        :param x: 输入数据
        :param y: 目标值（训练时需要）
        :return: 根据是否提供y返回不同的值
        """
        # 保存中间值用于反向传播
        self.layer0 = x
        self.layer1 = np.dot(x, self.w1) + self.b1
        self.layer1_act = self.sigmoid(self.layer1)
        self.layer2 = np.dot(self.layer1_act, self.w2) + self.b2
        self.layer2_act = self.sigmoid(self.layer2)

        if y is not None:
            # 计算损失
            loss = 0.5 * np.sum((self.layer2_act - y) ** 2)
            
            # 计算梯度
            delta2 = (self.layer2_act - y) * self.sigmoid_derivative(self.layer2_act)
            w2_grad = np.dot(self.layer1_act.T, delta2)
            b2_grad = np.sum(delta2, axis=0)
           
            delta1 = np.dot(delta2, self.w2.T) * self.sigmoid_derivative(self.layer1_act)
            w1_grad = np.dot(self.layer0.T, delta1)
            b1_grad = np.sum(delta1, axis=0)
            
            return self.layer2_act, loss, (w1_grad, b1_grad, w2_grad, b2_grad)
        return self.layer2_act

    def train_step(self, x, y):
        """单步训练"""
        _, loss, gradients = self.forward(x, y)
        w1_grad, b1_grad, w2_grad, b2_grad = gradients
        
        # 更新权重和偏置
        self.w1 -= self.lr * w1_grad
        self.b1 -= self.lr * b1_grad
        self.w2 -= self.lr * w2_grad
        self.b2 -= self.lr * b2_grad
        
        return loss

    def train(self, x, y, epochs=1000, batch_size=None, verbose=True):
        """
        训练模型
        :param x: 训练数据
        :param y: 目标值
        :param epochs: 训练轮数
        :param batch_size: 批量大小
        :param verbose: 是否打印训练信息
        """
        for epoch in range(epochs):
            if batch_size:
                # 实现小批量训练
                indices = np.random.permutation(len(x))
                for i in range(0, len(x), batch_size):
                    batch_idx = indices[i:i+batch_size]
                    loss = self.train_step(x[batch_idx], y[batch_idx])
            else:
                loss = self.train_step(x, y)
            
            self.losses.append(loss)
            
            if verbose and epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {loss:.6f}")
        
        return self.losses

    def predict(self, x):
        """预测"""
        return self.forward(x)
    
    def evaluate(self, x, y):
        """评估模型"""
        predictions = self.predict(x)
        loss = 0.5 * np.sum((predictions - y) ** 2)
        mse = np.mean((predictions - y) ** 2)
        mae = np.mean(np.abs(predictions - y))
        return {
            'loss': loss,
            'predictions': predictions,
            'mse': mse,
            'mae': mae
        }

    def plot_training_history(self):
        """绘制训练历史"""
        plt.figure(figsize=(12, 4))
        
        # 绘制损失曲线
        plt.subplot(1, 1, 1)
        plt.plot(self.losses, label='Training Loss')
        plt.title('Training History')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()

def main():
    # 生成示例数据
    x = np.asarray([[5.0, 10.0]])
    y = np.asarray([[0.01, 0.99]])
    
    # 创建并训练模型
    model = BPNeuralNetwork(
        input_size=2,
        hidden_size=3,
        output_size=2,
        learning_rate=0.5
    )
    
    # 训练模型
    model.train(x, y, epochs=1000, verbose=True)
    
    # 评估模型
    results = model.evaluate(x, y)
    print("\n评估结果:")
    print(f"预测值: {results['predictions']}")
    print(f"目标值: {y}")
    print(f"最终损失: {results['loss']:.6f}")
    
    # 绘制训练历史
    model.plot_training_history()

if __name__ == '__main__':
    main()
