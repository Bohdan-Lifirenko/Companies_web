document.addEventListener("DOMContentLoaded", async () => {
    const companyId = window.COMPANY_ID;

    await loadCompanyProfile(companyId);
    await loadRevenueChart(companyId);
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
