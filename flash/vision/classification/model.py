# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Any, Callable, Mapping, Sequence, Type, Union

import torch
from pytorch_lightning.metrics import Accuracy
from torch import nn
from torch.nn import functional as F

from flash.core.classification import ClassificationTask
from flash.vision.backbones import torchvision_backbone_and_num_features
from flash.vision.classification.data import ImageClassificationData, ImageClassificationDataPipeline


class ImageClassifier(ClassificationTask):
    """Task that classifies images.

    Args:
        num_classes: Number of classes to classify.
        backbone: A model to use to compute image features.
        pretrained: Use a pretrained backbone.
        loss_fn: Loss function for training, defaults to cross entropy.
        optimizer: Optimizer to use for training, defaults to `torch.optim.SGD`.
        metrics: Metrics to compute for training and evaluation.
        learning_rate: Learning rate to use for training, defaults to `1e-3`
    """

    def __init__(
        self,
        num_classes,
        backbone="resnet18",
        num_features: int = None,
        pretrained=True,
        loss_fn: Callable = F.cross_entropy,
        optimizer: Type[torch.optim.Optimizer] = torch.optim.SGD,
        metrics: Union[Callable, Mapping, Sequence, None] = (Accuracy()),
        learning_rate: float = 1e-3,
    ):
        super().__init__(
            model=None,
            loss_fn=loss_fn,
            optimizer=optimizer,
            metrics=metrics,
            learning_rate=learning_rate,
        )

        self.save_hyperparameters()

        self.backbone, num_features = torchvision_backbone_and_num_features(backbone, pretrained)

        self.head = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(num_features, num_classes),
        )

    def forward(self, x) -> Any:
        x = self.backbone(x)
        return self.head(x)

    @staticmethod
    def default_pipeline() -> ImageClassificationDataPipeline:
        return ImageClassificationData.default_pipeline()
