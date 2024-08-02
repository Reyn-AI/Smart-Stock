from typing import Union
from neuralforecast.losses.pytorch import BasePointLoss, _weighted_mean
from neuralforecast.common._scalers import TemporalNorm
import torch


class MixLoss(BasePointLoss):
    """涨跌幅约束"""

    def __init__(self, horizon_weight=None, delta=0.1, r=1):
        super(MixLoss, self).__init__(
            horizon_weight=horizon_weight, outputsize_multiplier=1, output_names=[""]
        )
        self.delta = delta #涨跌幅限制
        self.r = r #权重
        self.scalar = TemporalNorm(scaler_type='standard')
        
    def __call__(
        self,
        y: torch.Tensor,
        y_hat: torch.Tensor,
        mask: Union[torch.Tensor, None] = None,
    ):
        """
        **Parameters:**<br>
        `y`: tensor, Actual values.<br>
        `y_hat`: tensor, Predicted values.<br>
        `mask`: tensor, Specifies datapoints to consider in loss.<br>

        **Returns:**<br>
        `mae`: tensor (single value).
        """
        abs_losses = torch.abs(y - y_hat)
        diff = torch.abs(self.cal_change(y)) - self.delta
        diff = torch.where(diff<0, torch.zeros_like(diff), diff)
        weights = self._compute_weights(y=y, mask=mask)
        delta_loss = self.r * diff
        losses = abs_losses + delta_loss
        return _weighted_mean(losses=losses, weights=weights)
    
    def cal_change(self, y: torch.Tensor):
        #todo解决正则化的干扰
        y_shift = torch.roll(y, shifts=1, dims=1)
        y_shift[:, 0] = y_shift[:, 1]
        y_change = (y-y_shift)/(y_shift+1e-7)
        y_change[torch.isnan(y_change)] = 0
        y_change = self.min_max_normalization(y_change)
        return y_change
    
    def min_max_normalization(self, tensor):
    # 如果未提供最小值和最大值，先计算它们
        min_val = tensor.min()
        max_val = tensor.max()

        normalized_tensor = (tensor - min_val) / (max_val - min_val)
        
        return normalized_tensor
        