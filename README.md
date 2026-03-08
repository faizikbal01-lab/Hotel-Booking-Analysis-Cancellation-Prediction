#  Hotel Booking Analysis — Cancellation Prediction & Market Intelligence

A Python-based **Exploratory Data Analysis (EDA)** project built in Jupyter Notebook, examining hotel booking data to uncover cancellation patterns, revenue drivers, guest behaviour, and market segment insights. Structured across 10 sections with 4 multi-chart dashboard pages.

---

##  Key KPIs

| Metric | Value |
|---|---|
| City Hotel Cancel Rate | ~37% |
| Resort Hotel Cancel Rate | ~27% |
| Average Daily Rate (ADR) | Tracked over time (EUR) |
| Peak Booking Month | July – August |
| Top Booking Country | Portugal (PRT) |
| Repeat Guest Avg Stay | ~30% longer than new guests |

---

##  Notebook Structure

The notebook is organized into **10 clearly labeled sections**:

```
Hotel_Booking_Analysis___Cancellation_Prediction.ipynb
│
├── Section 1  — Setup & Configuration         (libraries, theme config)
├── Section 2  — Load Dataset                  (CSV upload / GitHub mirror)
├── Section 3  — Data Cleaning & Engineering   (deduplication, feature creation)
├── Section 4  — KPI Summary                   (printed metrics block)
├── Section 5  — Dashboard Page 1              (Hotel & Booking Overview)
├── Section 6  — Dashboard Page 2              (Revenue & ADR Analysis)
├── Section 7  — Dashboard Page 3              (Market Segments & Cancellation Drivers)
├── Section 8  — Dashboard Page 4              (Advanced Analytics & Heatmaps)
├── Section 9  — Detailed EDA Questions        (15 analytical deep-dives)
└── Section 10 — Key Insights & Recommendations
```

---

##  Tech Stack

| Tool | Purpose |
|---|---|
| Python 3 | Core language |
| Pandas | Data manipulation & aggregation |
| NumPy | Numerical computations |
| Matplotlib | Multi-panel dashboard charts |
| Seaborn | Statistical visualizations & heatmaps |
| Plotly | Interactive charts |
| Jupyter Notebook | Development & presentation environment |

---

##  Key Findings

**Cancellation by Hotel Type** — City hotels cancel at ~37%, significantly higher than resort hotels at ~27%, reflecting different guest intent and booking behaviour between property types.

**Lead Time Risk** — Bookings made 365+ days in advance carry the highest cancellation rates. The longer the lead time, the less committed the guest tends to be at point of booking.

**Deposit Type as the Strongest Lever** — Non-refundable deposits nearly eliminate cancellations entirely, making deposit policy one of the most powerful tools for protecting revenue.

**OTA Volume vs Quality Trade-off** — Online Travel Agents drive the highest booking volume but also carry elevated cancellation rates, reflecting the low-friction, easy-cancel nature of third-party platforms.

**Special Requests as Commitment Signal** — Guests who submit 3 or more special requests show a drastically lower cancellation rate, indicating higher personal investment in the stay.

**Seasonality** — July and August represent peak ADR and revenue across both hotel types, with significant variation throughout the year.

**Guest Loyalty Value** — Repeat guests stay approximately 30% longer than new guests, making loyalty programmes a meaningful revenue multiplier beyond just acquisition.

**Geographic Concentration** — Portugal (PRT) dominates booking origin data, with strong implications for targeted localised marketing.

---

##  Dashboard Pages

The notebook generates **4 multi-panel dark-theme dashboard figures**:

| Output File | Contents |
|---|---|
| `hotel_dashboard_p1.png` | Hotel type split, booking trends, stay duration, arrival month patterns |
| `hotel_dashboard_p2.png` | ADR over time, revenue distribution, rate comparisons |
| `hotel_dashboard_p3.png` | Market segments, country breakdown, cancellation drivers |
| `hotel_dashboard_p4.png` | Heatmaps, room type analysis, advanced correlation patterns |

---

##  Business Recommendations

1. **Enforce stricter deposit policies for city hotels** — With ~37% cancellation, offer non-refundable rate tiers with a 5–10% discount to shift guests away from high-cancel flexible bookings.

2. **Require deposits on long lead-time bookings** — Any booking made 6+ months in advance should trigger a partial or full non-refundable deposit requirement to protect against late cancellations.

3. **Incentivise direct bookings to reduce OTA dependency** — Offer direct-booking perks (room upgrades, free breakfast, early check-in) to reduce reliance on OTAs and their elevated churn rates.

4. **Proactively collect special requests at the booking step** — Since 3+ special requests dramatically lower cancellation likelihood, build a guided special-request step into the booking flow to increase guest commitment.

5. **Apply dynamic pricing in July–August** — Peak season is the maximum yield window. Revenue management tools and advance staffing plans should align tightly with this demand curve.

6. **Build a loyalty programme targeting repeat guests** — Given repeat guests stay ~30% longer, post-stay email sequences with exclusive return offers would generate strong occupancy and ADR returns.

7. **Localise marketing for Portugal** — PRT dominates bookings; Portuguese-language customer support, regional ad targeting, and local partnerships would strengthen conversion in this core market.

8. **Use lead time + deposit type as an early cancellation risk flag** — Combining these two variables into a risk score could enable revenue teams to intervene proactively (e.g., targeted upsell or deposit prompt) before a high-risk booking is lost.


## Author

**[Mohd Faiz]**

- **Role:** Business and Data Analyst
- **GitHub:** [https://github.com/faizikbal01-lab](https://github.com/your-github-handle)





---
