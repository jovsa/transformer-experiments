import torch
from transformer.model import make_model
from transformer.training_utils import (
    LabelSmoothing,
    NoamOpt,
    run_epoch,
    SimpleLossCompute,
    data_gen,
    greedy_decode,
)

# from pdb import set_trace


## setup / initialize
V = 11
num_epoches = 1
criterion = LabelSmoothing(size=V, padding_idx=0, smoothing=0.0)
model = make_model(V, V, N=2)
model_opt = NoamOpt(
    model.src_embed[0].d_model,
    1,
    400,
    torch.optim.Adam(model.parameters(), lr=0, betas=(0.9, 0.98), eps=1e-9),
)

## training loop
for epoch in range(num_epoches):
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

## evaluate
model.eval()
print(greedy_decode(model, max_len=10, start_symbol=1))
print('lol')