"""自定义网络结构"""
import torch
import torch.nn as nn
import pytorch_lightning as pl


class SmartStockNetwork(pl.LightningModule):
    
    def __init__(self,num_factors=3, windows_size=32, in_channels=1, in_out_channels=64, num_class=1):
        """输入：[b, 1, windows_size, num_factors]"""
        super().__init__()
        self.conv_in = nn.Conv2d(in_channels=in_channels, out_channels=in_out_channels, kernel_size=num_factors)

    def min_max_normalization(self, tensor):
    # 如果未提供最小值和最大值，先计算它们
        min_val = tensor.min()
        max_val = tensor.max()
        normalized_tensor = (tensor - min_val) / (max_val - min_val)
        return normalized_tensor
    
    def normalization(self, seriers):
        seriers[torch.isnan(seriers)] = 0
        seriers = self.min_max_normalization(seriers)
        return seriers