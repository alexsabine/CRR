"""Small decoder-only Transformer (pre-LN, learned positions, GELU MLP x4, tied output), byte vocabulary 256."""
import math, torch, torch.nn as nn, torch.nn.functional as F
class Block(nn.Module):
    def __init__(self, d, h):
        super().__init__(); self.ln1 = nn.LayerNorm(d); self.attn = nn.MultiheadAttention(d, h, batch_first=True); self.ln2 = nn.LayerNorm(d); self.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d))
    def forward(self, x, mask):
        a = self.ln1(x); x = x + self.attn(a, a, a, attn_mask=mask, need_weights=False)[0]; return x + self.mlp(self.ln2(x))
class GPT(nn.Module):
    def __init__(self, d=128, layers=4, heads=4, ctx=128, vocab=256):
        super().__init__(); self.tok = nn.Embedding(vocab, d); self.pos = nn.Embedding(ctx, d); self.blocks = nn.ModuleList([Block(d, heads) for _ in range(layers)]); self.ln = nn.LayerNorm(d); self.ctx = ctx
        self.register_buffer('mask', torch.triu(torch.ones(ctx, ctx, dtype=torch.bool), 1))
        for p in self.parameters():
            if p.dim() > 1: nn.init.normal_(p, 0, 0.02)
    def forward(self, x):
        T = x.shape[1]; h = self.tok(x) + self.pos(torch.arange(T, device=x.device)); m = self.mask[:T, :T]
        for b in self.blocks: h = b(h, m)
        return self.ln(h) @ self.tok.weight.T
    def loss(self, x, y): return F.cross_entropy(self.forward(x).reshape(-1, 256), y.reshape(-1))
def n_params(m): return sum(p.numel() for p in m.parameters())
