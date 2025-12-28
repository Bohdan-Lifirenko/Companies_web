document.addEventListener("DOMContentLoaded", async () => {
    const companyId = window.COMPANY_ID;

    await loadCompanyProfile(companyId);
    await loadRevenueChart(companyId);
    await loadBalanceWaterfall(companyId);
});


/* ==============================
   CHART CONFIGURATION
============================== */
const CHART_COLORS = {
    primary: "#3498db",
    positive: "#2ecc71",
    negative: "#e74c3c",
    gradient: {
        start: "rgba(52, 152, 219, 0.4)",
        end: "rgba(52, 152, 219, 0.05)"
    }
};

const CHART_DEFAULTS = {
    font: { family: "Inter, system-ui, sans-serif", size: 12 },
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    margin: { t: 50, r: 30, b: 50, l: 70 },
    hovermode: "x unified"
};

function formatNumber(value) {
    return new Intl.NumberFormat("uk-UA", {
        maximumFractionDigits: 0
    }).format(value);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString("uk-UA", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit"
    });
}

function showChartError(container, message = "Помилка завантаження даних") {
    container.innerHTML = `
        <div class="alert alert-danger text-center">
             ${message}
        </div>
    `;
}

function showChartLoading(container) {
    container.innerHTML = `
        <div class="d-flex justify-content-center align-items-center h-100">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Завантаження...</span>
            </div>
        </div>
    `;
}


/* ==============================
   COMPANY PROFILE
============================== */
async function loadCompanyProfile(companyId) {
    const container = document.getElementById("company-profile");

    try {
        const response = await fetch(`/companies/${companyId}`);
        if (!response.ok) {
            throw new Error("Failed to load company profile");
        }

        const company = await response.json();

        container.innerHTML = `
            <div class="row g-3">
                <div class="col-md-12">
                    <div class="info-label">Назва</div>
                    <div class="fw-semibold">${company.name ?? "-"}</div>
                </div>

                <div class="col-md-3">
                    <div class="info-label">ЄДРПОУ</div>
                    <div>${company.tax_id ?? companyId}</div>
                </div>

                <div class="col-md-3">
                    <div class="info-label">КВЕД</div>
                    <div>${company.kved ?? "-"}</div>
                </div>

                <div class="col-md-3">
                    <div class="info-label">Код ОПФ</div>
                    <div>${company.opf_code ?? "-"}</div>
                </div>

                <div class="col-md-3">
                    <div class="info-label">Код регіону</div>
                    <div>${company.region_code ?? "-"}</div>
                </div>

                <div class="col-md-6">
                    <div class="info-label">КАТОТТГ</div>
                    <div>${company.katottg ?? "-"}</div>
                </div>

                <div class="col-md-6">
                    <div class="info-label">Код населеного пункту</div>
                    <div>${company.local_code ?? "-"}</div>
                </div>
            </div>
        `;

    } catch (error) {
        container.innerHTML = `
            <div class="alert alert-danger">
                Не вдалося завантажити профіль компанії
            </div>
        `;
        console.error(error);
    }
}

/* ==============================
   REVENUE CHART
============================== */
async function loadRevenueChart(companyId) {
    const chartDiv = document.getElementById("revenue-chart");

    try {
        const response = await fetch(`/companies/${companyId}/revenue`);
        const data = await response.json();

        // Обробка помилки від API або порожніх даних
        if (!response.ok || data.error || !Array.isArray(data) || !data.length) {
            chartDiv.innerHTML = `<div class="text-muted text-center py-4">Немає даних про дохід</div>`;
            return;
        }

        const dates = data.map(item => new Date(item.date));
        const values = data.map(item => item.value);

        const trace = {
            x: dates,
            y: values,
            type: "scatter",
            mode: "lines+markers",
            name: "Дохід",
            line: {
                width: 3,
                color: CHART_COLORS.primary,
                shape: "spline"
            },
            marker: {
                size: 8,
                color: CHART_COLORS.primary,
                line: { width: 2, color: "#fff" }
            },
            fill: "tozeroy",
            fillcolor: CHART_COLORS.gradient.start,
            hovertemplate: "<b>%{x|%d.%m.%Y}</b><br>Дохід: %{y:,.0f} грн<extra></extra>"
        };

        const layout = {
            ...CHART_DEFAULTS,
            title: {
                text: "Графік динаміки виручки за всі доступні дати",
                font: { size: 16, color: "#333" }
            },
            xaxis: {
                title: "Дата",
                showgrid: true,
                gridcolor: "rgba(0,0,0,0.05)",
                tickformat: "%b %Y"
            },
            yaxis: {
                title: "Значення (грн)",
                tickformat: ",.0f",
                showgrid: true,
                gridcolor: "rgba(0,0,0,0.08)",
                zeroline: true,
                zerolinecolor: "rgba(0,0,0,0.1)"
            }
        };

        const config = {
            responsive: true,
            displayModeBar: true,
            modeBarButtonsToRemove: ["lasso2d", "select2d"],
            displaylogo: false
        };

        Plotly.newPlot(chartDiv, [trace], layout, config);

    } catch (error) {
        chartDiv.innerHTML = `<div class="text-muted text-center py-4">Немає даних про дохід</div>`;
        console.error(error);
    }
}

async function loadBalanceWaterfall(companyId) {
    const select = document.getElementById("balance-date-select");
    const chartDiv = document.getElementById("balance-waterfall-chart");

    try {
        const response = await fetch(`/companies/${companyId}/balance`);
        const balances = await response.json();

        // Обробка помилки від API або порожніх даних
        if (!response.ok || balances.error || !Array.isArray(balances) || !balances.length) {
            chartDiv.innerHTML = `<div class="text-muted text-center py-4">Немає даних про баланс</div>`;
            select.innerHTML = `<option>Немає даних</option>`;
            return;
        }

        // заповнюємо dropdown
        select.innerHTML = "";
        balances.forEach((b, index) => {
            const option = document.createElement("option");
            option.value = index;
            option.textContent = formatDate(b.date);
            select.appendChild(option);
        });

        // обираємо ОСТАННЮ дату
        select.value = balances.length - 1;

        // будуємо графік
        renderBalanceWaterfall(balances[select.value]);

        // onchange
        select.addEventListener("change", () => {
            renderBalanceWaterfall(balances[select.value]);
        });

    } catch (error) {
        showChartError(chartDiv, "Не вдалося завантажити дані балансу");
        console.error(error);
    }
}

function renderBalanceWaterfall(balance) {
    const chartDiv = document.getElementById("balance-waterfall-chart");

    const equity = balance.equity ?? 0;
    const liabilities = balance.liabilities ?? 0;
    const assets = equity + liabilities;

    const data = [{
        type: "waterfall",
        orientation: "v",
        x: ["Власний капітал", "Зобов'язання", "Активи"],
        measure: ["relative", "relative", "total"],
        y: [equity, liabilities, assets],
        text: [formatNumber(equity), formatNumber(liabilities), formatNumber(assets)],
        textposition: "outside",
        textfont: { size: 13, color: "#333" },

        increasing: {
            marker: {
                color: CHART_COLORS.positive,
                line: { color: CHART_COLORS.positive, width: 1 }
            }
        },
        decreasing: {
            marker: {
                color: CHART_COLORS.negative,
                line: { color: CHART_COLORS.negative, width: 1 }
            }
        },
        totals: {
            marker: {
                color: CHART_COLORS.primary,
                line: { color: CHART_COLORS.primary, width: 1 }
            }
        },

        connector: {
            line: { width: 2, color: "rgba(0,0,0,0.2)", dash: "dot" }
        },

        hovertemplate: "<b>%{x}</b><br>Сума: %{y:,.0f} грн<extra></extra>"
    }];

    const layout = {
        ...CHART_DEFAULTS,
        title: {
            text: `Графік балансу (Assets = Liabilities + Equity)`,
            font: { size: 16, color: "#333" }
        },
        yaxis: {
            title: "Сума (грн)",
            zeroline: true,
            zerolinecolor: "rgba(0,0,0,0.2)",
            tickformat: ",.0f",
            showgrid: true,
            gridcolor: "rgba(0,0,0,0.08)"
        },
        showlegend: false,
        bargap: 0.3
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ["lasso2d", "select2d"],
        displaylogo: false
    };

    Plotly.newPlot(chartDiv, data, layout, config);
}



