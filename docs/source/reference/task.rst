############
General Task
############

A majority of data science problems that involve machine learning can be tackled using Task. With Task you can:

- Pass an arbitrary model
- Pass an arbitrary loss
- Pass an arbitrary optimizer

*****************************
Example: Image Classification
*****************************

.. code-block:: python

    from flash import Task
    from torch import nn, optim
    from torch.utils.data import DataLoader, random_split
    from torchvision import transforms, datasets
    import pytorch_lightning as pl

    # model
    model = nn.Sequential(
        nn.Flatten(),
        nn.Linear(28 * 28, 128),
        nn.ReLU(),
        nn.Linear(128, 10)
    )

    # data
    dataset = datasets.MNIST('./data_folder', download=True, transform=transforms.ToTensor())
    train, val = random_split(dataset, [55000, 5000])

    # task
    classifier = Task(model, loss_fn=nn.functional.cross_entropy, optimizer=optim.Adam)

    # train
    pl.Trainer().fit(classifier, DataLoader(train), DataLoader(val))

-----

*************
API reference
*************

.. _task:

Task
----

.. autoclass:: flash.core.Task
    :members:
    :noindex:
    :exclude-members: forward
