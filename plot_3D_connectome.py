# Plotly 3D scatter with top-5% connections as edges
import numpy as np
import plotly.graph_objects as go
from plotly.colors import sample_colorscale
import plotly.express as px

connectivity_data = 'data/connectivity_76'  # adjust path as needed
weights = np.loadtxt(f'{connectivity_data}/weights.txt')
centres = np.loadtxt(f'{connectivity_data}/centres.txt', dtype=str)
regions = centres[:, 0]

# coordinates and labels
x = centres[:, 1].astype(float)
y = centres[:, 2].astype(float)
z = centres[:, 3].astype(float)
labels = list(regions)

# node colours (hemisphere heuristic) and strengths
node_colors = ['red' if lab.startswith('r') else 'blue' if lab.startswith('l') else 'gray' for lab in labels]
strengths = weights.sum(axis=1)

# pick top 5% edges (from upper triangle)
n = weights.shape[0]
tri_idx = np.triu_indices(n, k=1)
tri_weights = weights[tri_idx]
pct = 95  # keep edges >= 95th percentile -> top 5%
threshold = np.percentile(tri_weights, pct)
mask = tri_weights >= threshold
edge_i = tri_idx[0][mask]
edge_j = tri_idx[1][mask]
edge_w = tri_weights[mask]
num_edges = len(edge_w)
print(f"Selected {num_edges} edges (weights >= {threshold:.4g})")

# normalize edge weights to [0,1] for width/color mapping
if num_edges > 0:
    wmin, wmax = edge_w.min(), edge_w.max()
    denom = (wmax - wmin) if (wmax - wmin) != 0 else 1.0
    w_norm = (edge_w - wmin) / denom
else:
    w_norm = np.array([])

# colorscale for edges
colorscale = px.colors.sequential.Viridis

# create traces: one line-trace per edge (keeps per-edge color and hover)
edge_traces = []
for (i, j, wn, w) in zip(edge_i, edge_j, w_norm, edge_w):
    color = sample_colorscale(colorscale, [wn])[0]  # returns list -> take first
    width = 1 + wn * 6                              # widths in [1,7]
    hover = f"{labels[i]} — {labels[j]}<br>weight={w:.4g}"
    edge_traces.append(
        go.Scatter3d(
            x=[x[i], x[j]],
            y=[y[i], y[j]],
            z=[z[i], z[j]],
            mode='lines',
            line=dict(color=color, width=width),
            hoverinfo='text',
            text=[hover],
            opacity=0.7,
            showlegend=False
        )
    )

# node trace (draw on top)
node_trace = go.Scatter3d(
    x=x, y=y, z=z,
    mode='markers+text',
    marker=dict(size=5, color=node_colors, line=dict(width=0.5, color='black')),
    text=labels,
    hovertemplate="%{text}<br>x=%{x:.2f}<br>y=%{y:.2f}<br>z=%{z:.2f}<extra></extra>",
    textposition='top center',
    showlegend=False
)

# compose and show figure (edges first so nodes are drawn on top)
fig = go.Figure(data=edge_traces + [node_trace])
fig.update_layout(
    scene=dict(
        xaxis=dict(title='X'),
        yaxis=dict(title='Y'),
        zaxis=dict(title='Z')
    ),
    title=f"3D Brain Regions with top {100-pct}% connections ({num_edges} edges)"
)
fig.show()