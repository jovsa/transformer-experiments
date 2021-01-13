import torch
from transformer.model import make_model
from transformer.training_utils import (
    LabelSmoothing,
    NoamOpt,
    run_epoch,
    SimpleLossCompute,
    data_gen,
)

# from pdb import set_trace


# training loop
V = 11
criterion = LabelSmoothing(size=V, padding_idx=0, smoothing=0.0)
model = make_model(V, V, N=2)
model_opt = NoamOpt(
    model.src_embed[0].d_model,
    1,
    400,
    torch.optim.Adam(model.parameters(), lr=0, betas=(0.9, 0.98), eps=1e-9),
)

for epoch in range(10):
    model.train()
    run_epoch(
        data_gen(V, 30, 20),
        model,
        SimpleLossCompute(model.generator, criterion, model_opt),
    )
    model.eval()
    tot_loss = run_epoch(
        data_gen(V, 30, 5), model, SimpleLossCompute(model.generator, criterion, None)
    )
    print("total loss:", tot_loss.item())
