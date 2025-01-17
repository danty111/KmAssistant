'''
Author: danty haiboy@globalcrown.com.cn
Date: 2025-01-16 13:42:52
LastEditors: danty haiboy@globalcrown.com.cn
LastEditTime: 2025-01-16 17:05:09
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# _*_ coding: utf-8 _*_

import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
from typing import Tuple, List

class BPNetwork(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        """初始化BP网络"""
        super(BPNetwork, self).__init__()
        
        # 使用nn.Sequential构建网络层
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.Sigmoid(),
            nn.Linear(hidden_size, output_size),
            nn.Sigmoid()
        )
        
        # 使用xavier初始化权重
        self.apply(self._init_weights)
        
    @staticmethod
    def _init_weights(m):
        """初始化网络权重"""
        if isinstance(m, nn.Linear):
            torch.nn.init.xavier_uniform_(m.weight)
            torch.nn.init.zeros_(m.bias)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """前向传播"""
        return self.network(x)
    
    def train_model(
        self, 
        x: torch.Tensor, 
        y: torch.Tensor, 
        epochs: int = 1000,
        lr: float = 0.1
    ) -> List[float]:
        """训练模型"""
        # 使用MSE损失函数
        criterion = nn.MSELoss()
        # 使用Adam优化器
        optimizer = optim.Adam(self.parameters(), lr=lr)
        
        losses = []
        
        for epoch in range(epochs):
            # 清零梯度
            optimizer.zero_grad()
            
            # 前向传播
            output = self(x)
            loss = criterion(output, y)
            
            # 反向传播
            loss.backward()
            
            # 更新参数
            optimizer.step()
            
            # 记录损失
            losses.append(loss.item())
            
            if epoch % 100 == 0:
                print(f"Epoch {epoch}/{epochs}, Loss: {loss.item():.6f}")
        
        self._plot_loss(losses)
        return losses
    
    @staticmethod
    def _plot_loss(losses: List[float]) -> None:
        """绘制损失曲线"""
        plt.figure(figsize=(10, 6))
        plt.plot(losses)
        plt.title('Loss Curve')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.grid(True)
        plt.yscale('log')
        plt.show()

def main():
    # 设置随机种子
    torch.manual_seed(42)
    
    # 准备数据
    x = torch.tensor([[5.0, 10.0]], dtype=torch.float32)
    y = torch.tensor([[0.01, 0.99]], dtype=torch.float32)
    
    # 创建模型
    model = BPNetwork(
        input_size=2,
        hidden_size=3,
        output_size=2
    )
    
    # 训练模型
    losses = model.train_model(x, y)
    
    # 评估结果
    model.eval()  # 设置为评估模式
    with torch.no_grad():
        final_output = model(x)
        print("\n最终结果：")
        print(f"预测值：{final_output}")
        print(f"目标值：{y}")
        print(f"最终损失：{nn.MSELoss()(final_output, y):.6f}")

if __name__ == "__main__":
    main()
