#!/usr/bin/env python3
"""
Generate comprehensive CRR framework diagrams for LaTeX document.
Creates PNG images explaining Coherence-Rupture-Regeneration dynamics.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib import patheffects
import matplotlib.gridspec as gridspec

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.dpi'] = 150

# Color scheme
COLOR_COHERENCE = '#059669'  # Green
COLOR_RUPTURE = '#dc2626'    # Red
COLOR_REGENERATION = '#7c3aed'  # Purple
COLOR_FEP = '#2563eb'  # Blue


def create_crr_cycle_diagram():
    """Create the complete CRR cycle showing C -> delta -> R"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(5, 9.5, 'The Coherence-Rupture-Regeneration Cycle',
            fontsize=18, fontweight='bold', ha='center')

    # Coherence box
    coherence_box = FancyBboxPatch((0.5, 5.5), 2.5, 2.5,
                                   boxstyle="round,pad=0.1",
                                   edgecolor=COLOR_COHERENCE,
                                   facecolor=COLOR_COHERENCE,
                                   alpha=0.2, linewidth=3)
    ax.add_patch(coherence_box)
    ax.text(1.75, 7.5, 'COHERENCE', fontsize=14, fontweight='bold',
            ha='center', color=COLOR_COHERENCE)
    ax.text(1.75, 7.0, r'$C(x,t) = \int_0^t L(x,\tau) d\tau$',
            fontsize=11, ha='center')
    ax.text(1.75, 6.5, 'Memory accumulation', fontsize=10, ha='center', style='italic')
    ax.text(1.75, 6.1, 'Integration of experience', fontsize=9, ha='center')

    # Rupture box
    rupture_box = FancyBboxPatch((7, 5.5), 2.5, 2.5,
                                 boxstyle="round,pad=0.1",
                                 edgecolor=COLOR_RUPTURE,
                                 facecolor=COLOR_RUPTURE,
                                 alpha=0.2, linewidth=3)
    ax.add_patch(rupture_box)
    ax.text(8.25, 7.5, 'RUPTURE', fontsize=14, fontweight='bold',
            ha='center', color=COLOR_RUPTURE)
    ax.text(8.25, 7.0, r'$\delta(t-t_0)$', fontsize=11, ha='center')
    ax.text(8.25, 6.5, 'Discontinuous transition', fontsize=10, ha='center', style='italic')
    ax.text(8.25, 6.1, 'When $C \geq C_{crit}$', fontsize=9, ha='center')

    # Regeneration box
    regen_box = FancyBboxPatch((3.5, 1.5), 3, 2.5,
                               boxstyle="round,pad=0.1",
                               edgecolor=COLOR_REGENERATION,
                               facecolor=COLOR_REGENERATION,
                               alpha=0.2, linewidth=3)
    ax.add_patch(regen_box)
    ax.text(5, 3.5, 'REGENERATION', fontsize=14, fontweight='bold',
            ha='center', color=COLOR_REGENERATION)
    ax.text(5, 3.0, r'$R[\chi] = \int_0^t \phi(\tau) e^{C(\tau)/\Omega} \Theta(t-\tau) d\tau$',
            fontsize=10, ha='center')
    ax.text(5, 2.5, 'Exponentially-weighted memory reconstruction', fontsize=10,
            ha='center', style='italic')
    ax.text(5, 2.0, 'Past states weighted by prediction success', fontsize=9, ha='center')

    # Arrows
    # C -> delta
    arrow1 = FancyArrowPatch((3, 6.75), (7, 6.75),
                            arrowstyle='->,head_width=0.6,head_length=0.6',
                            color='black', lw=2.5,
                            path_effects=[patheffects.withStroke(linewidth=4, foreground='white')])
    ax.add_patch(arrow1)
    ax.text(5, 7.2, 'Threshold\ncrossing', fontsize=9, ha='center',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # delta -> R
    arrow2 = FancyArrowPatch((8.25, 5.5), (6.5, 4),
                            arrowstyle='->,head_width=0.6,head_length=0.6',
                            color='black', lw=2.5,
                            path_effects=[patheffects.withStroke(linewidth=4, foreground='white')])
    ax.add_patch(arrow2)
    ax.text(7.8, 4.6, 'System\nrebuilds', fontsize=9, ha='center',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # R -> C
    arrow3 = FancyArrowPatch((3.5, 2.5), (1.75, 5.5),
                            arrowstyle='->,head_width=0.6,head_length=0.6',
                            color='black', lw=2.5,
                            path_effects=[patheffects.withStroke(linewidth=4, foreground='white')])
    ax.add_patch(arrow3)
    ax.text(2.2, 3.8, 'New\ncoherence\nbuilds', fontsize=9, ha='center',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Add central label
    ax.text(5, 5.2, 'CONTINUOUS CYCLE', fontsize=12, ha='center',
            fontweight='bold', style='italic',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3, edgecolor='black', linewidth=2))

    # Bottom explanation
    ax.text(5, 0.7, 'Systems maintain identity through discontinuous change via memory-weighted reconstruction',
            fontsize=11, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))

    plt.tight_layout()
    plt.savefig('crr-cycle-diagram.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Created crr-cycle-diagram.png")
    plt.close()


def create_coherence_accumulation_graph():
    """Show coherence building over time with rupture events"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Time series
    t = np.linspace(0, 100, 1000)

    # Memory density L(t) with fluctuations
    L = 0.05 + 0.02*np.sin(2*np.pi*t/20) + 0.01*np.random.randn(len(t)).cumsum()/50

    # Coherence C(t) = integral of L
    C = np.cumsum(L) * (t[1]-t[0])

    # Rupture events when C crosses threshold
    C_crit = 2.5
    rupture_times = []
    rupture_coherence = []
    C_with_ruptures = C.copy()

    for i in range(1, len(t)):
        if C_with_ruptures[i] > C_crit and C_with_ruptures[i-1] <= C_crit:
            rupture_times.append(t[i])
            rupture_coherence.append(C_with_ruptures[i])
            # Reset coherence after rupture (40% reduction)
            C_with_ruptures[i:] -= 0.6 * C_with_ruptures[i]

    # Plot memory density
    ax1.plot(t, L, color=COLOR_COHERENCE, linewidth=2, label='Memory Density $L(x,t)$')
    ax1.axhline(y=0, color='black', linestyle='--', alpha=0.3)
    ax1.fill_between(t, 0, L, where=(L>0), alpha=0.2, color=COLOR_COHERENCE, label='Coherence building')
    ax1.fill_between(t, 0, L, where=(L<0), alpha=0.2, color='red', label='Decoherence')
    ax1.set_ylabel('Memory Density $L(x,t)$', fontsize=12)
    ax1.set_title('Coherence-Rupture-Regeneration Dynamics', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)

    # Plot coherence with ruptures
    ax2.plot(t, C_with_ruptures, color=COLOR_COHERENCE, linewidth=2.5, label='Coherence $C(x,t)$')
    ax2.axhline(y=C_crit, color=COLOR_RUPTURE, linestyle='--', linewidth=2,
                label=f'Critical threshold $C_{{crit}}$ = {C_crit}')

    # Mark rupture events
    for rt, rc in zip(rupture_times, rupture_coherence):
        ax2.axvline(x=rt, color=COLOR_RUPTURE, linestyle=':', alpha=0.5)
        ax2.scatter([rt], [rc], color=COLOR_RUPTURE, s=200, marker='X',
                   edgecolors='black', linewidth=1.5, zorder=5,
                   label='Rupture $\delta(t-t_0)$' if rt == rupture_times[0] else '')

    # Shade rupture regions
    for i, rt in enumerate(rupture_times):
        ax2.axvspan(rt-0.5, rt+0.5, alpha=0.15, color=COLOR_RUPTURE)
        # Add rupture annotation
        ax2.annotate(f'Rupture {i+1}', xy=(rt, C_crit), xytext=(rt, C_crit+0.8),
                    arrowprops=dict(arrowstyle='->', color=COLOR_RUPTURE, lw=1.5),
                    fontsize=9, ha='center',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor=COLOR_RUPTURE))

    ax2.fill_between(t, 0, C_with_ruptures, alpha=0.2, color=COLOR_COHERENCE)
    ax2.set_xlabel('Time $t$', fontsize=12)
    ax2.set_ylabel('Coherence $C(x,t)$', fontsize=12)
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)

    # Add explanation
    fig.text(0.5, 0.02,
            r'$C(x,t) = \int_0^t L(x,\tau) d\tau$ accumulates until rupture at $C_{crit}$, then resets and regenerates',
            ha='center', fontsize=11, style='italic',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig('coherence-accumulation-graph.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Created coherence-accumulation-graph.png")
    plt.close()


def create_regeneration_visualization():
    """Visualize exponential weighting of historical states"""
    fig = plt.figure(figsize=(14, 8))
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

    # Historical coherence
    ax1 = fig.add_subplot(gs[0, :])
    t_hist = np.linspace(0, 10, 100)
    C_hist = 0.5 + 0.3*np.sin(2*np.pi*t_hist/3) + 0.1*np.random.randn(len(t_hist))
    C_hist = np.cumsum(C_hist * 0.1)

    ax1.plot(t_hist, C_hist, color=COLOR_COHERENCE, linewidth=2, label='Historical Coherence $C(\\tau)$')
    ax1.fill_between(t_hist, 0, C_hist, alpha=0.2, color=COLOR_COHERENCE)
    ax1.axvline(x=10, color=COLOR_RUPTURE, linestyle='--', linewidth=2, label='Rupture event $t_0$')
    ax1.set_xlabel('Past Time $\\tau$', fontsize=12)
    ax1.set_ylabel('Coherence $C(\\tau)$', fontsize=12)
    ax1.set_title('Historical Coherence Profile', fontsize=13, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Exponential weighting for different Omega
    ax2 = fig.add_subplot(gs[1, 0])
    Omega_values = [0.5, 1.0, 2.0]
    colors = ['red', 'orange', 'blue']

    for Omega, color in zip(Omega_values, colors):
        weights = np.exp(C_hist / Omega)
        weights_norm = weights / np.max(weights)
        ax2.plot(t_hist, weights_norm, linewidth=2, label=f'$\\Omega = {Omega}$', color=color)

    ax2.set_xlabel('Past Time $\\tau$', fontsize=12)
    ax2.set_ylabel('Relative Weight $e^{C(\\tau)/\\Omega}$', fontsize=12)
    ax2.set_title('Exponential Coherence Weighting', fontsize=13, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.text(0.5, 0.5, 'Small $\\Omega$: Recent states dominate\nLarge $\\Omega$: All history contributes',
            transform=ax2.transAxes, fontsize=9, verticalalignment='center',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

    # Regeneration contribution
    ax3 = fig.add_subplot(gs[1, 1])
    phi_hist = np.sin(2*np.pi*t_hist/2) + 0.5  # Historical field signal
    Omega = 1.5
    weights = np.exp(C_hist / Omega)
    contribution = phi_hist * weights

    ax3.fill_between(t_hist, 0, contribution, alpha=0.3, color=COLOR_REGENERATION, label='Weighted contribution')
    ax3.plot(t_hist, contribution, color=COLOR_REGENERATION, linewidth=2)
    ax3.set_xlabel('Past Time $\\tau$', fontsize=12)
    ax3.set_ylabel('$\\phi(\\tau) \\cdot e^{C(\\tau)/\\Omega}$', fontsize=12)
    ax3.set_title('Regeneration Integral Contribution', fontsize=13, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Calculate regeneration value
    R_value = np.trapz(contribution, t_hist)
    ax3.text(0.5, 0.9, f'$R[\\chi] = {R_value:.2f}$',
            transform=ax3.transAxes, fontsize=12, ha='center', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor=COLOR_REGENERATION, alpha=0.3, edgecolor='black', linewidth=2))

    fig.suptitle('Regeneration Operator: Memory-Weighted Reconstruction', fontsize=16, fontweight='bold', y=0.98)

    plt.savefig('regeneration-visualization.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Created regeneration-visualization.png")
    plt.close()


def create_fep_crr_connection():
    """Diagram showing connection between FEP and CRR"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # Left: Free Energy vs Coherence
    t = np.linspace(0, 10, 200)
    C_t = 3 * (1 - np.exp(-t/2)) + 0.2*np.sin(2*np.pi*t/3)
    F_t = 5 * np.exp(-t/2) + 0.3*np.sin(2*np.pi*t/3) + 1

    ax1_twin = ax1.twinx()

    line1 = ax1.plot(t, C_t, color=COLOR_COHERENCE, linewidth=3, label='Coherence $C(t)$')
    ax1.fill_between(t, 0, C_t, alpha=0.2, color=COLOR_COHERENCE)
    ax1.set_xlabel('Time $t$', fontsize=12)
    ax1.set_ylabel('Coherence $C(t)$', fontsize=12, color=COLOR_COHERENCE)
    ax1.tick_params(axis='y', labelcolor=COLOR_COHERENCE)

    line2 = ax1_twin.plot(t, F_t, color=COLOR_FEP, linewidth=3, linestyle='--', label='Free Energy $F(t)$')
    ax1_twin.fill_between(t, F_t, 6, alpha=0.2, color=COLOR_FEP)
    ax1_twin.set_ylabel('Free Energy $F(t)$', fontsize=12, color=COLOR_FEP)
    ax1_twin.tick_params(axis='y', labelcolor=COLOR_FEP)

    # Add inverse relationship annotation
    ax1.annotate('', xy=(5, 2.5), xytext=(5, 0.5),
                arrowprops=dict(arrowstyle='<->', color=COLOR_COHERENCE, lw=2.5))
    ax1.text(5.5, 1.5, 'C increases', fontsize=10, color=COLOR_COHERENCE, fontweight='bold')

    ax1_twin.annotate('', xy=(5, 2), xytext=(5, 5),
                     arrowprops=dict(arrowstyle='<->', color=COLOR_FEP, lw=2.5))
    ax1_twin.text(5.5, 3.5, 'F decreases', fontsize=10, color=COLOR_FEP, fontweight='bold')

    ax1.set_title('Coherence-Free Energy Duality\n$C(t) \\propto -F(t)$', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='center right')

    # Right: FEP Active Inference Cycle mapped to CRR
    ax2.axis('off')
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)

    ax2.text(5, 9.5, 'FEP ↔ CRR Correspondence', fontsize=14, fontweight='bold', ha='center')

    # FEP column
    ax2.text(2.5, 8.5, 'Free Energy Principle', fontsize=12, ha='center', fontweight='bold',
            color=COLOR_FEP)

    fep_items = [
        (8.0, 'Minimize $F$'),
        (7.2, 'Prediction accuracy'),
        (6.4, 'Model inadequacy'),
        (5.6, 'Model switching'),
        (4.8, 'Bayesian inference'),
        (4.0, 'Active inference')
    ]

    for y, text in fep_items:
        ax2.text(2.5, y, text, fontsize=10, ha='center',
                bbox=dict(boxstyle='round', facecolor=COLOR_FEP, alpha=0.2, edgecolor=COLOR_FEP, linewidth=2))

    # CRR column
    ax2.text(7.5, 8.5, 'CRR Framework', fontsize=12, ha='center', fontweight='bold',
            color=COLOR_COHERENCE)

    crr_items = [
        (8.0, 'Maximize $C$', COLOR_COHERENCE),
        (7.2, '$L = -dF/dt$', COLOR_COHERENCE),
        (6.4, '$C \\geq C_{crit}$', COLOR_RUPTURE),
        (5.6, 'Rupture $\\delta(t-t_0)$', COLOR_RUPTURE),
        (4.8, '$R[\\chi] = \\int \\phi e^{C/\\Omega}$', COLOR_REGENERATION),
        (4.0, 'Maximize $E[L]$', COLOR_REGENERATION)
    ]

    for y, text, color in crr_items:
        ax2.text(7.5, y, text, fontsize=10, ha='center',
                bbox=dict(boxstyle='round', facecolor=color, alpha=0.2, edgecolor=color, linewidth=2))

    # Arrows showing correspondence
    arrow_ys = [8.0, 7.2, 6.4, 5.6, 4.8, 4.0]
    for y in arrow_ys:
        ax2.annotate('', xy=(6.5, y), xytext=(3.5, y),
                    arrowprops=dict(arrowstyle='<->', color='black', lw=2))

    # Bottom explanation
    ax2.text(5, 2.5, 'Coherence accumulation = Free energy minimization', fontsize=11, ha='center',
            fontweight='bold', style='italic',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7, edgecolor='black', linewidth=2))

    ax2.text(5, 1.5, 'Rupture = Generative model switching when $F$ cannot be minimized', fontsize=10, ha='center',
            style='italic')
    ax2.text(5, 0.8, 'Regeneration = Bayesian model averaging weighted by evidence', fontsize=10, ha='center',
            style='italic')

    plt.tight_layout()
    plt.savefig('fep-crr-connection.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Created fep-crr-connection.png")
    plt.close()


def create_scale_invariance_diagram():
    """Show CRR operating across multiple scales"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(5, 9.5, 'CRR Scale Invariance: Universal Coarse-Grain Active Inference',
            fontsize=16, fontweight='bold', ha='center')

    # Scales (logarithmic spacing)
    scales = [
        (8.5, 'Quantum\n(nm, ps)', '• Decoherence\n• Quantum jumps\n• Measurement', '#e74c3c'),
        (7.2, 'Molecular\n(μm, ms)', '• Protein folding\n• Enzyme catalysis\n• Conformational changes', '#e67e22'),
        (6.0, 'Cellular\n(mm, s)', '• Synaptic plasticity\n• Action potentials\n• Mitosis', '#f39c12'),
        (4.8, 'Organismal\n(m, h)', '• Learning\n• Development\n• Behavior', '#2ecc71'),
        (3.6, 'Ecological\n(km, y)', '• Population cycles\n• Succession\n• Disturbance', '#3498db'),
        (2.4, 'Cultural\n(global, decades)', '• Paradigm shifts\n• Institutions\n• Traditions', '#9b59b6'),
        (1.2, 'Cosmological\n(Mpc, Gy)', '• Structure formation\n• Dark energy\n• Phase transitions', '#34495e')
    ]

    for y, scale_label, examples, color in scales:
        # Scale box
        box = FancyBboxPatch((0.5, y-0.4), 3, 0.7,
                            boxstyle="round,pad=0.05",
                            edgecolor=color,
                            facecolor=color,
                            alpha=0.2, linewidth=2)
        ax.add_patch(box)
        ax.text(2, y, scale_label, fontsize=11, ha='center', va='center', fontweight='bold')

        # Examples
        ax.text(5.5, y, examples, fontsize=9, va='center',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.7, edgecolor=color, linewidth=1.5))

    # Connecting line showing continuity
    y_values = [s[0] for s in scales]
    ax.plot([0.3]*len(y_values), y_values, 'k--', linewidth=2, alpha=0.3)

    # CRR operators apply at all scales
    ax.text(8.5, 5, 'Same CRR Structure:', fontsize=13, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='black', linewidth=2))

    crr_formulas = [
        (4.3, f'$C(x,t) = \\int_0^t L(x,\\tau) d\\tau$', COLOR_COHERENCE),
        (3.8, f'$\\delta(t-t_0)$ when $C \\geq C_{{crit}}$', COLOR_RUPTURE),
        (3.3, f'$R[\\chi] = \\int \\phi(\\tau) e^{{C(\\tau)/\\Omega}} d\\tau$', COLOR_REGENERATION)
    ]

    for y, formula, color in crr_formulas:
        ax.text(8.5, y, formula, fontsize=11, ha='center',
                bbox=dict(boxstyle='round', facecolor=color, alpha=0.2, edgecolor=color, linewidth=2))

    # Key insight
    ax.text(5, 0.5, 'Universal Pattern: Memory accumulation → Critical transition → Weighted reconstruction',
            fontsize=11, ha='center', fontweight='bold', style='italic',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5, edgecolor='black', linewidth=2))

    plt.tight_layout()
    plt.savefig('scale-invariance-diagram.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Created scale-invariance-diagram.png")
    plt.close()


def create_memory_signatures_diagram():
    """Visualize the 5 memory signature types"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.delaxes(axes[1, 2])  # Remove last subplot

    t = np.linspace(0, 100, 1000)

    signatures = [
        # (ax, title, coherence_func, color, description)
        (axes[0, 0], 'Fragile', lambda t: t*0.05 + 0.01*np.random.randn(len(t)).cumsum()/10,
         '#e74c3c', 'Monotonic buildup\n→ Catastrophic collapse'),
        (axes[0, 1], 'Resilient', lambda t: 2 + 0.5*np.sin(2*np.pi*t/25) + 0.1*np.random.randn(len(t)),
         '#2ecc71', 'Balanced cycles\n→ Adaptive stability'),
        (axes[0, 2], 'Oscillatory', lambda t: 2 + np.sin(2*np.pi*t/15),
         '#3498db', 'Rhythmic renewal\n→ Limit cycles'),
        (axes[1, 0], 'Chaotic', lambda t: 0.5 + 0.05*np.random.randn(len(t)).cumsum()/3,
         '#9b59b6', 'Perpetual fragmentation\n→ No coherence buildup'),
        (axes[1, 1], 'Dialectical', lambda t: 2 + 0.3*np.sin(2*np.pi*t/20) + 0.2*np.sin(2*np.pi*t/8),
         '#f39c12', 'Interfering fields\n→ Emergent patterns')
    ]

    for ax, title, func, color, desc in signatures:
        C = func(t)
        C = np.clip(C, 0, None)  # Ensure non-negative

        # Add ruptures for non-chaotic signatures
        if 'Chaotic' not in title:
            C_crit = np.mean(C) + np.std(C)
            for i in range(1, len(t)):
                if C[i] > C_crit and C[i-1] <= C_crit:
                    ax.axvline(x=t[i], color=COLOR_RUPTURE, linestyle=':', alpha=0.5, linewidth=1.5)
                    C[i:] *= 0.7  # Partial reset

        ax.plot(t, C, color=color, linewidth=2)
        ax.fill_between(t, 0, C, alpha=0.3, color=color)

        if 'Chaotic' not in title:
            ax.axhline(y=C_crit, color=COLOR_RUPTURE, linestyle='--', linewidth=1.5, alpha=0.7,
                      label='$C_{crit}$')

        ax.set_title(f'{title} Signature', fontsize=12, fontweight='bold', color=color)
        ax.set_xlabel('Time', fontsize=10)
        ax.set_ylabel('Coherence $C(t)$', fontsize=10)
        ax.text(0.5, 0.95, desc, transform=ax.transAxes, fontsize=9, ha='center', va='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor=color, linewidth=2))
        ax.grid(True, alpha=0.3)

    fig.suptitle('Memory Signatures: Five Dynamical Regimes', fontsize=16, fontweight='bold')

    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.savefig('memory-signatures-diagram.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Created memory-signatures-diagram.png")
    plt.close()


def main():
    """Generate all CRR diagrams"""
    print("Generating CRR framework diagrams...")
    print("=" * 60)

    create_crr_cycle_diagram()
    create_coherence_accumulation_graph()
    create_regeneration_visualization()
    create_fep_crr_connection()
    create_scale_invariance_diagram()
    create_memory_signatures_diagram()

    print("=" * 60)
    print("✓ All diagrams generated successfully!")
    print("\nGenerated files:")
    print("  1. crr-cycle-diagram.png")
    print("  2. coherence-accumulation-graph.png")
    print("  3. regeneration-visualization.png")
    print("  4. fep-crr-connection.png")
    print("  5. scale-invariance-diagram.png")
    print("  6. memory-signatures-diagram.png")
    print("\nThese images can now be included in the LaTeX document.")


if __name__ == '__main__':
    main()
