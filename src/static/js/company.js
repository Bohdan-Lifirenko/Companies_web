document.addEventListener("DOMContentLoaded", async () => {
    const companyId = window.COMPANY_ID;

    await loadCompanyProfile(companyId);
    await loadRevenueChart(companyId);
    await loadBalanceWaterfall(companyId);
});


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
                <div class="col-md-6">
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

                <div class="col-md-6">
                    <div class="info-label">Адреса</div>
                    <div>${company.address ?? "-"}</div>
                </div>

                <div class="col-md-3">
                    <div class="info-label">Статус</div>
                    <span class="badge bg-success">
                        ${company.status ?? "N/A"}
                    </span>
                </div>
            </div>
        `;

    } catch (error) {
        container.innerHTML = `
            <div class="alert alert-danger">
                ❌ Не вдалося завантажити профіль компанії
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
        if (!response.ok) {
            throw new Error("Failed to load revenue data");
        }

        const data = await response.json();

        const dates = data.map(item => new Date(item.date));
        const values = data.map(item => item.value);

        const trace = {
            x: dates,
            y: values,
            type: "scatter",
            mode: "lines+markers",
            name: "Дохід",
            line: { width: 3 }
        };

        const layout = {
            title: "Динаміка доходу",
            xaxis: { title: "Дата" },
            yaxis: { title: "Значення", tickformat: ",.0f" }
        };

        Plotly.newPlot(chartDiv, [trace], layout, { responsive: true });

    } catch (error) {
        chartDiv.innerHTML = `
            <div class="alert alert-danger text-center">
                ❌ Помилка завантаження даних
            </div>
        `;
        console.error(error);
    }
}

async function loadBalanceWaterfall(companyId) {
    const select = document.getElementById("balance-date-select");
    const chartDiv = document.getElementById("balance-waterfall-chart");

    try {
        const response = await fetch(`/companies/${companyId}/balance`);
        if (!response.ok) {
            throw new Error("Failed to load balance data");
        }

        const balances = await response.json();

        if (!balances.length) {
            chartDiv.innerHTML = "Немає даних";
            return;
        }

        // заповнюємо dropdown
        select.innerHTML = "";
        balances.forEach((b, index) => {
            const option = document.createElement("option");
            option.value = index;
            option.textContent = b.date;
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
        chartDiv.innerHTML = `
            <div class="alert alert-danger text-center">
                ❌ Помилка завантаження балансу
            </div>
        `;
        console.error(error);
    }
}

function renderBalanceWaterfall(balance) {
    const chartDiv = document.getElementById("balance-waterfall-chart");

    const equity = balance.equity;
    const liabilities = balance.liabilities;
    const assets = equity + liabilities; // контрольна сума

    const positiveColor = "#2ecc71";   // зелений
    const negativeColor = "#e74c3c";   // червоний
    const assetsColor   = "#3498db";   // синій

    const data = [{
        type: "waterfall",
        orientation: "v",
        x: ["Equity", "Liabilities", "Assets"],
        measure: ["relative", "relative", "total"],
        y: [equity, liabilities, assets],
        text: [equity, liabilities, assets],
        textposition: "outside",

        increasing: {
            marker: { color: positiveColor }
        },
        decreasing: {
            marker: { color: negativeColor }
        },
        totals: {
            marker: { color: assetsColor }
        },

        connector: {
            line: { width: 2 }
        }
    }];

    const layout = {
        title: `Balance structure (${formatDate(balance.date)})`,
        yaxis: {
            title: "Value",
            zeroline: true,
            tickformat: ",.0f"
        },
        showlegend: false
    };

    Plotly.newPlot(chartDiv, data, layout, { responsive: true });
}


function formatDate(dateString) {
    return new Date(dateString).toISOString().split("T")[0];
}



