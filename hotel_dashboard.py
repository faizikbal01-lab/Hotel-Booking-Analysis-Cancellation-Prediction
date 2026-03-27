import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch
import warnings
warnings.filterwarnings('ignore')

# ── Load & clean ─────────────────────────────────────────────────────────────
df = pd.read_csv('/mnt/user-data/uploads/hotel_booking.csv')

MONTH_ORDER = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']
MONTH_SHORT = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec']

df['arrival_date_month'] = pd.Categorical(
    df['arrival_date_month'], categories=MONTH_ORDER, ordered=True)
df['total_stays'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
df['revenue']     = df['adr'] * df['total_stays']

# ── Palette ──────────────────────────────────────────────────────────────────
BG        = '#0B0F1A'
CARD      = '#131929'
BORDER    = '#1E2740'
GRID_CLR  = '#1A2035'
TEXT_PRI  = '#E2E8F0'
TEXT_SEC  = '#7A8FA6'

C_RESORT  = '#38BDF8'   # sky blue  – Resort Hotel
C_CITY    = '#818CF8'   # indigo    – City Hotel
C_CANCEL  = '#F87171'   # red       – cancelled
C_OK      = '#34D399'   # green     – not cancelled
C_AMBER   = '#FCD34D'   # amber     – highlights
C_PURPLE  = '#C084FC'   # purple

# ── Helpers ──────────────────────────────────────────────────────────────────
def style_ax(ax, title='', xlabel='', ylabel='', xgrid=False):
    ax.set_facecolor(CARD)
    ax.tick_params(colors=TEXT_SEC, labelsize=8.5)
    ax.xaxis.label.set_color(TEXT_SEC)
    ax.yaxis.label.set_color(TEXT_SEC)
    for sp in ['top', 'right']:
        ax.spines[sp].set_visible(False)
    for sp in ['bottom', 'left']:
        ax.spines[sp].set_color(BORDER)
    ax.yaxis.grid(True, color=GRID_CLR, linewidth=0.5, linestyle='--', alpha=0.8)
    if xgrid:
        ax.xaxis.grid(True, color=GRID_CLR, linewidth=0.5, linestyle='--', alpha=0.8)
    ax.set_axisbelow(True)
    if title:
        ax.set_title(title, color=TEXT_PRI, fontsize=10.5,
                     fontweight='bold', pad=10, loc='left')
    if xlabel: ax.set_xlabel(xlabel, color=TEXT_SEC, fontsize=8.5)
    if ylabel: ax.set_ylabel(ylabel, color=TEXT_SEC, fontsize=8.5)

def metric_card(ax, value, label, sub='', color=C_RESORT):
    ax.set_facecolor(CARD)
    for sp in ax.spines.values():
        sp.set_color(BORDER); sp.set_linewidth(0.7)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.text(0.5, 0.60, value, ha='center', va='center',
            fontsize=26, fontweight='bold', color=color)
    ax.text(0.5, 0.30, label, ha='center', va='center',
            fontsize=10, color=TEXT_PRI)
    if sub:
        ax.text(0.5, 0.13, sub, ha='center', va='center',
                fontsize=8.5, color=TEXT_SEC)

def leg(labels, colors):
    return [mpatches.Patch(color=c, label=l) for l, c in zip(labels, colors)]

# ── Figure ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(22, 28), facecolor=BG)
gs  = gridspec.GridSpec(5, 3, figure=fig,
                        hspace=0.50, wspace=0.33,
                        top=0.95, bottom=0.03,
                        left=0.06, right=0.97)

# ── Title ─────────────────────────────────────────────────────────────────────
fig.text(0.06, 0.972, '🏨  Hotel Booking Analytics Dashboard',
         fontsize=22, fontweight='bold', color=TEXT_PRI, va='top')
fig.text(0.06, 0.957,
         f'{len(df):,} bookings  ·  2015–2017  ·  City Hotel & Resort Hotel  ·  32 features',
         fontsize=11, color=TEXT_SEC, va='top')

# ═══════════════════════════════════════════════════════════════════════════
# ROW 0 – Metric cards
# ═══════════════════════════════════════════════════════════════════════════
cancel_rate = df['is_canceled'].mean()
avg_adr     = df['adr'].median()
avg_lead    = df['lead_time'].mean()

ax_m1 = fig.add_subplot(gs[0, 0])
metric_card(ax_m1, f'{cancel_rate*100:.1f}%',
            'Overall cancellation rate',
            f'{df["is_canceled"].sum():,} of {len(df):,} bookings', C_CANCEL)

ax_m2 = fig.add_subplot(gs[0, 1])
metric_card(ax_m2, f'€{avg_adr:.0f}',
            'Median daily rate (ADR)',
            'City €105  ·  Resort €80', C_AMBER)

ax_m3 = fig.add_subplot(gs[0, 2])
metric_card(ax_m3, f'{avg_lead:.0f} days',
            'Avg booking lead time',
            'Cancelled: 106d  ·  Checked-out: 70d', C_PURPLE)

# ═══════════════════════════════════════════════════════════════════════════
# ROW 1 – Monthly bookings trend (full width)
# ═══════════════════════════════════════════════════════════════════════════
ax1 = fig.add_subplot(gs[1, :])
monthly = df.groupby('arrival_date_month', observed=True).agg(
    bookings=('is_canceled', 'count'),
    cancellations=('is_canceled', 'sum'),
    avg_adr=('adr', 'mean')
).reset_index()
monthly['checked_in'] = monthly['bookings'] - monthly['cancellations']
x = np.arange(12)

ax1.bar(x, monthly['checked_in'],    color=C_OK,     edgecolor='none', label='Checked-out / No-show', width=0.6)
ax1.bar(x, monthly['cancellations'], color=C_CANCEL,  edgecolor='none',
        bottom=monthly['checked_in'], label='Cancelled', width=0.6)

ax1_r = ax1.twinx()
ax1_r.plot(x, monthly['avg_adr'], color=C_AMBER, linewidth=2.2,
           marker='o', markersize=5, label='Avg ADR (€)', zorder=5)
ax1_r.tick_params(colors=TEXT_SEC, labelsize=8.5)
ax1_r.set_ylabel('Average Daily Rate (€)', color=TEXT_SEC, fontsize=8.5)
ax1_r.yaxis.label.set_color(TEXT_SEC)
for sp in ['top', 'right']:
    ax1_r.spines[sp].set_visible(False)
ax1_r.spines['right'].set_color(BORDER)
ax1_r.set_facecolor(CARD)

ax1.set_xticks(x)
ax1.set_xticklabels(MONTH_SHORT, color=TEXT_PRI, fontsize=9.5)
style_ax(ax1, 'Monthly bookings volume & average daily rate', ylabel='Number of bookings')
handles1 = leg(['Checked-out','Cancelled'], [C_OK, C_CANCEL])
handles2 = [plt.Line2D([0],[0], color=C_AMBER, linewidth=2, marker='o', markersize=5, label='Avg ADR (€)')]
ax1.legend(handles=handles1 + handles2, frameon=False,
           labelcolor=TEXT_SEC, fontsize=9, loc='upper left')

# ═══════════════════════════════════════════════════════════════════════════
# ROW 2 – ADR by hotel/month + Cancellation by market segment
# ═══════════════════════════════════════════════════════════════════════════
ax2 = fig.add_subplot(gs[2, :2])
adr_hotel = df.groupby(['arrival_date_month','hotel'], observed=True)['adr'].mean().unstack()
x = np.arange(12)
ax2.plot(x, adr_hotel['City Hotel'],   color=C_CITY,   linewidth=2.2,
         marker='o', markersize=5, label='City Hotel')
ax2.plot(x, adr_hotel['Resort Hotel'], color=C_RESORT, linewidth=2.2,
         marker='s', markersize=5, label='Resort Hotel')
ax2.fill_between(x, adr_hotel['City Hotel'],   alpha=0.10, color=C_CITY)
ax2.fill_between(x, adr_hotel['Resort Hotel'], alpha=0.10, color=C_RESORT)
ax2.set_xticks(x)
ax2.set_xticklabels(MONTH_SHORT, color=TEXT_PRI, fontsize=9)
style_ax(ax2, 'Average daily rate by hotel type (monthly)', ylabel='ADR (€)')
ax2.legend(frameon=False, labelcolor=TEXT_SEC, fontsize=9)

ax3 = fig.add_subplot(gs[2, 2])
seg = df.groupby('market_segment')['is_canceled'].agg(['mean','count'])
seg = seg[seg['count'] > 100].sort_values('mean', ascending=True)
seg_labels = seg.index.tolist()
seg_vals   = seg['mean'].values * 100
bar_colors = [C_CANCEL if v > 30 else C_OK if v < 15 else C_AMBER for v in seg_vals]
bars = ax3.barh(range(len(seg_labels)), seg_vals,
                color=bar_colors, edgecolor='none', height=0.6)
ax3.set_yticks(range(len(seg_labels)))
ax3.set_yticklabels(seg_labels, color=TEXT_PRI, fontsize=8.5)
for bar, v in zip(bars, seg_vals):
    ax3.text(v + 0.5, bar.get_y() + bar.get_height()/2,
             f'{v:.1f}%', va='center', fontsize=8, color=TEXT_SEC)
ax3.axvline(df['is_canceled'].mean()*100, color=C_AMBER,
            linewidth=1.2, linestyle='--', alpha=0.8)
ax3.text(df['is_canceled'].mean()*100 + 0.5, len(seg_labels)-0.2,
         'Avg', color=C_AMBER, fontsize=7.5)
style_ax(ax3, 'Cancellation rate\nby market segment', xlabel='Cancellation rate (%)')
ax3.yaxis.grid(False)
ax3.xaxis.grid(True, color=GRID_CLR, linewidth=0.5, linestyle='--')

# ═══════════════════════════════════════════════════════════════════════════
# ROW 3 – Lead time vs cancellation + Top guest countries + Stay length dist
# ═══════════════════════════════════════════════════════════════════════════
ax4 = fig.add_subplot(gs[3, 0])
bins_lt  = [0,7,30,90,180,365,700]
labels_lt= ['0-7d','8-30d','31-90d','91-180d','181-365d','365d+']
df['lead_bucket'] = pd.cut(df['lead_time'], bins=bins_lt, labels=labels_lt)
lt_stats = df.groupby('lead_bucket', observed=True)['is_canceled'].agg(['mean','count'])
lv = lt_stats['mean'].values * 100
bar_colors_lt = plt.cm.RdYlGn_r(np.linspace(0.1, 0.85, len(lv)))
bars_lt = ax4.bar(range(len(labels_lt)), lv, color=bar_colors_lt,
                  edgecolor='none', width=0.65)
for bar, v in zip(bars_lt, lv):
    ax4.text(bar.get_x() + bar.get_width()/2, v + 0.5,
             f'{v:.0f}%', ha='center', fontsize=8, color=TEXT_SEC)
ax4.set_xticks(range(len(labels_lt)))
ax4.set_xticklabels(labels_lt, color=TEXT_PRI, fontsize=8, rotation=25, ha='right')
style_ax(ax4, 'Cancellation rate\nby lead time', ylabel='Cancellation rate (%)')

ax5 = fig.add_subplot(gs[3, 1])
top_c = df['country'].value_counts().head(9)
country_colors = [C_RESORT, C_CITY, C_AMBER, C_OK, C_CANCEL,
                  C_PURPLE, '#38BDF8', '#FB923C', '#A3E635']
wedges, texts, autotexts = ax5.pie(
    top_c.values,
    labels=None,
    autopct='%1.1f%%',
    colors=country_colors,
    startangle=140,
    wedgeprops=dict(width=0.55, edgecolor=BG, linewidth=1.5),
    pctdistance=0.78
)
for at in autotexts:
    at.set_color(BG); at.set_fontsize(7.5); at.set_fontweight('bold')
ax5.set_facecolor(CARD)
ax5.set_title('Top guest countries', color=TEXT_PRI,
              fontsize=10.5, fontweight='bold', pad=10, loc='left')
legend_c = [mpatches.Patch(color=country_colors[i],
            label=f'{top_c.index[i]}  {top_c.values[i]:,}')
            for i in range(len(top_c))]
ax5.legend(handles=legend_c, loc='lower center',
           bbox_to_anchor=(0.5, -0.22), ncol=3,
           frameon=False, labelcolor=TEXT_SEC, fontsize=7.5)

ax6 = fig.add_subplot(gs[3, 2])
stay_data0 = df[(df['is_canceled']==0) & (df['total_stays']>0) & (df['total_stays']<=20)]['total_stays']
stay_data1 = df[(df['is_canceled']==1) & (df['total_stays']>0) & (df['total_stays']<=20)]['total_stays']
bins_stay = np.arange(0.5, 21.5, 1)
ax6.hist(stay_data0, bins=bins_stay, color=C_OK,     alpha=0.72, edgecolor='none', label='Not cancelled', density=True)
ax6.hist(stay_data1, bins=bins_stay, color=C_CANCEL, alpha=0.72, edgecolor='none', label='Cancelled',     density=True)
ax6.axvline(stay_data0.mean(), color=C_OK,     linewidth=1.5, linestyle='--')
ax6.axvline(stay_data1.mean(), color=C_CANCEL, linewidth=1.5, linestyle='--')
style_ax(ax6, 'Length of stay distribution', xlabel='Total nights', ylabel='Density')
ax6.legend(frameon=False, labelcolor=TEXT_SEC, fontsize=8)

# ═══════════════════════════════════════════════════════════════════════════
# ROW 4 – Hotel KPI comparison table + Revenue bar
# ═══════════════════════════════════════════════════════════════════════════
ax7 = fig.add_subplot(gs[4, :2])
ax7.set_facecolor(CARD)
ax7.axis('off')
ax7.set_title('Hotel performance comparison', color=TEXT_PRI,
              fontsize=10.5, fontweight='bold', pad=10, loc='left')

kpis = {
    'Total bookings':        [f'{df[df["hotel"]=="City Hotel"].shape[0]:,}',
                              f'{df[df["hotel"]=="Resort Hotel"].shape[0]:,}'],
    'Cancellation rate':     [f'{df[df["hotel"]=="City Hotel"]["is_canceled"].mean()*100:.1f}%',
                              f'{df[df["hotel"]=="Resort Hotel"]["is_canceled"].mean()*100:.1f}%'],
    'Median ADR (€)':        [f'€{df[df["hotel"]=="City Hotel"]["adr"].median():.0f}',
                              f'€{df[df["hotel"]=="Resort Hotel"]["adr"].median():.0f}'],
    'Avg lead time':         [f'{df[df["hotel"]=="City Hotel"]["lead_time"].mean():.0f}d',
                              f'{df[df["hotel"]=="Resort Hotel"]["lead_time"].mean():.0f}d'],
    'Avg stay length':       [f'{df[df["hotel"]=="City Hotel"]["total_stays"].mean():.1f} nights',
                              f'{df[df["hotel"]=="Resort Hotel"]["total_stays"].mean():.1f} nights'],
    'Repeat guest rate':     [f'{df[df["hotel"]=="City Hotel"]["is_repeated_guest"].mean()*100:.1f}%',
                              f'{df[df["hotel"]=="Resort Hotel"]["is_repeated_guest"].mean()*100:.1f}%'],
}

col_w = [0.36, 0.28, 0.28]
header_y = 0.90
row_h = 0.13

ax7.text(0.02, header_y, 'Metric',       color=TEXT_SEC, fontsize=9, fontweight='bold', transform=ax7.transAxes)
ax7.text(0.02+col_w[0], header_y, 'City Hotel',    color=C_CITY,   fontsize=9, fontweight='bold', transform=ax7.transAxes)
ax7.text(0.02+col_w[0]+col_w[1], header_y, 'Resort Hotel', color=C_RESORT, fontsize=9, fontweight='bold', transform=ax7.transAxes)
ax7.plot([0.02, 0.98], [header_y-0.07, header_y-0.07],
         color=BORDER, linewidth=0.8, transform=ax7.transAxes)

row_bgs = ['#161E30', CARD]
for i, (label, vals) in enumerate(kpis.items()):
    y = header_y - 0.10 - i * row_h
    rect = FancyBboxPatch((0.01, y-0.055), 0.97, row_h-0.01,
                          boxstyle='round,pad=0.005', linewidth=0,
                          facecolor=row_bgs[i%2], transform=ax7.transAxes, clip_on=False)
    ax7.add_patch(rect)
    ax7.text(0.02, y, label, color=TEXT_SEC, fontsize=9, va='center', transform=ax7.transAxes)
    ax7.text(0.02+col_w[0], y, vals[0], color=TEXT_PRI, fontsize=9.5, fontweight='bold',
             va='center', transform=ax7.transAxes)
    ax7.text(0.02+col_w[0]+col_w[1], y, vals[1], color=TEXT_PRI, fontsize=9.5, fontweight='bold',
             va='center', transform=ax7.transAxes)

ax8 = fig.add_subplot(gs[4, 2])
rev_data = (df[df['is_canceled']==0]
            .groupby(['arrival_date_month', 'hotel'], observed=True)['revenue']
            .sum().unstack().fillna(0))
x = np.arange(12)
w = 0.38
ax8.bar(x - w/2, rev_data['City Hotel']   / 1e6, w, color=C_CITY,   edgecolor='none', label='City Hotel')
ax8.bar(x + w/2, rev_data['Resort Hotel'] / 1e6, w, color=C_RESORT, edgecolor='none', label='Resort Hotel')
ax8.set_xticks(x)
ax8.set_xticklabels(MONTH_SHORT, color=TEXT_PRI, fontsize=7.5, rotation=35, ha='right')
style_ax(ax8, 'Monthly revenue\n(completed stays)', ylabel='Revenue (€M)')
ax8.legend(frameon=False, labelcolor=TEXT_SEC, fontsize=8)
ax8.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'€{v:.1f}M'))

plt.savefig('/mnt/user-data/outputs/hotel_dashboard.png',
            dpi=160, bbox_inches='tight', facecolor=BG)
print("Hotel dashboard saved!")
