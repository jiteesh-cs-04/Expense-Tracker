const filterToggle = document.getElementById("filter-toggle");
const filterOptions = document.getElementById("filter-options");
const filterArrow = document.getElementById("filter-arrow");

filterToggle.addEventListener("click", function() {

    filterOptions.classList.toggle("hidden");
    filterArrow.classList.toggle("rotated");
    

});
//---------------------------------------------------------<><><><>--------------------------------------------------------------
const tabButtons = document.querySelectorAll(".tab-button");
const tabContents = document.querySelectorAll(".tab-content");
const indicator = document.querySelector(".tab-indicator");

tabButtons.forEach((button, index) => {

    button.addEventListener("click", function() {

        // Remove active class from all buttons
        tabButtons.forEach(btn => {
            btn.classList.remove("active");
        });

        // Remove active class from all panels
        tabContents.forEach(panel => {
            panel.classList.remove("active");
        });

        // Activate clicked button
        button.classList.add("active");

        // Display corresponding panel
        const selectedTab = button.dataset.tab;
        document.getElementById(selectedTab + "-panel").classList.add("active");

        // Move sliding indicator
        indicator.style.transform = `translateX(${index * 100}%)`;

    });

});




// --------------------------------------------------
// LOAD AND DISPLAY EXPENSES
// --------------------------------------------------

const recentExpensesList = document.getElementById("recent-expenses-list");
const showMoreButton = document.getElementById("show-more");
const pagination = document.getElementById("pagination");
const previousPage = document.getElementById("previous-page");
const nextPage = document.getElementById("next-page");
const pageNumber = document.getElementById("page-number");

let allExpenses = [];
let currentPage = 1;
let expanded = false;

const pageSize = 20;
const initialSize = 5;


// Fetch expenses from Flask
async function loadExpenses() {

    try {

        const response = await fetch("/api/expenses");

        if (!response.ok) {
            throw new Error("Could not retrieve expenses");
        }

        allExpenses = await response.json();

        // Sort expenses by date (newest first)
        allExpenses.sort((a, b) =>
            new Date(b.date) - new Date(a.date)
        );

        displayExpenses();
        await loadCategoryChart();
        await loadMonthlyChart();

    }

    catch (error) {

        console.error("Error loading expenses:", error);
        recentExpensesList.textContent = "Unable to load expenses.";

    }

}


// Display expenses on the dashboard
function displayExpenses() {

    recentExpensesList.replaceChildren();

    const startIndex = expanded
        ? (currentPage - 1) * pageSize
        : 0;

    const endIndex = expanded
        ? startIndex + pageSize
        : initialSize;

    const visibleExpenses = allExpenses.slice(startIndex, endIndex);

    const table = document.createElement("table");
    const headerRow = document.createElement("tr");

    ["ID", "Description", "Category", "Date", "Amount"].forEach(title => {

        const heading = document.createElement("th");
        heading.textContent = title;
        headerRow.appendChild(heading);

    });

    table.appendChild(headerRow);

    visibleExpenses.forEach(expense => {

        const row = document.createElement("tr");

        const values = [
            expense.id,
            expense.description,
            expense.category,
            expense.date,
            `₹${Number(expense.amount).toFixed(2)}`
        ];

        values.forEach(value => {

            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);

        });

        table.appendChild(row);

    });

    recentExpensesList.appendChild(table);

    // Show More button
    showMoreButton.hidden = expanded || allExpenses.length <= initialSize;

    // Pagination
    pagination.classList.toggle(
        "hidden",
        !expanded || allExpenses.length <= pageSize
    );

    if (expanded) {

        const totalPages = Math.ceil(allExpenses.length / pageSize);

        pageNumber.textContent = `Page ${currentPage} of ${totalPages}`;

        previousPage.disabled = currentPage === 1;
        nextPage.disabled = currentPage === totalPages;

    }
    updateSummary();

}


// Show the first 20 expenses
showMoreButton.addEventListener("click", function() {

    expanded = true;
    currentPage = 1;

    displayExpenses();

});


// Previous page
previousPage.addEventListener("click", function() {

    if (currentPage > 1) {

        currentPage--;
        displayExpenses();

    }

});


// Next page
nextPage.addEventListener("click", function() {

    const totalPages = Math.ceil(allExpenses.length / pageSize);

    if (currentPage < totalPages) {

        currentPage++;
        displayExpenses();

    }

});


// Load expenses when the page opens
loadExpenses();

// --------------------------------------------------
// ADD EXPENSE
// --------------------------------------------------

const addExpenseButton = document.getElementById("add-expense-btn");

addExpenseButton.addEventListener("click", async function() {

    const description = document.getElementById("add-description").value;
    const amount = document.getElementById("add-amount").value;
    const category = document.getElementById("add-category").value;
    const date = document.getElementById("add-date").value;

    const expenseData = {
        description: description,
        amount: Number(amount),
        category: category,
        date: date
    };
    try {
        const response = await fetch("/api/expenses", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(expenseData)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.message || "Failed to add expense");
        }

        console.log(result.message);

        // Clear the input fields
        document.getElementById("add-description").value = "";
        document.getElementById("add-amount").value = "";
        document.getElementById("add-category").value = "";
        document.getElementById("add-date").value = "";

        // Reload expenses from database
        await loadExpenses();

    } catch (error) {
        console.error("Error adding expense:", error);
    }
});

// --------------------------------------------------
// EDIT EXPENSE
// --------------------------------------------------

const editExpenseButton = document.getElementById("edit-expense-btn");

editExpenseButton.addEventListener("click", async function() {

    const expenseData = {
        id: document.getElementById("edit-id").value,
        description: document.getElementById("edit-description").value,
        amount: document.getElementById("edit-amount").value,
        category: document.getElementById("edit-category").value,
        date: document.getElementById("edit-date").value
    };

    try {
        const response = await fetch("/api/expenses/edit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(expenseData)
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.message);
            return;
        }

        console.log(result.message);

        // Clear the fields
        document.getElementById("edit-id").value = "";
        document.getElementById("edit-description").value = "";
        document.getElementById("edit-amount").value = "";
        document.getElementById("edit-category").value = "";
        document.getElementById("edit-date").value = "";

        // Refresh the dashboard
        await loadExpenses();

    } catch (error) {
        console.error("Error editing expense:", error);
    }
});
// --------------------------------------------------
// DELETE EXPENSE
// --------------------------------------------------

const deleteExpenseButton = document.getElementById("delete-expense-btn");

deleteExpenseButton.addEventListener("click", async function() {

    const expenseId = document.getElementById("delete-id").value;

    if (!expenseId) {
        alert("Please enter an Expense ID");
        return;
    }

    // Ask for confirmation
    if (!confirm("Are you sure you want to delete this expense?")) {
        return;
    }

    try {
        const response = await fetch("/api/expenses/delete", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id: expenseId
            })
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.message);
            return;
        }

        alert(result.message);

        document.getElementById("delete-id").value = "";

        await loadExpenses();

    } catch (error) {
        console.error("Error deleting expense:", error);
    }
});


// --------------------------------------------------
// SEARCH EXPENSES
// --------------------------------------------------

const searchExpenseButton = document.getElementById("search-expense-btn");

searchExpenseButton.addEventListener("click", async function() {

    const description = document.getElementById("search-description").value.trim();
    const category = document.getElementById("search-category").value;

    try {
        const response = await fetch("/api/expenses/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                description: description,
                category: category
            })
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.message);
            return;
        }

        allExpenses = result;
        expanded = true;
        currentPage = 1;

        displayExpenses();

        // Clear search fields
        document.getElementById("search-description").value = "";
        document.getElementById("search-category").value = "";

    } catch (error) {
        console.error("Error searching expenses:", error);
    }
});


// --------------------------------------------------
// APPLY FILTERS
// --------------------------------------------------

const applyFiltersButton = document.getElementById("apply-filters");

applyFiltersButton.addEventListener("click", async function() {

    const category = document.getElementById("category-filter").value;
    const minAmount = document.getElementById("amount-min").value;
    const maxAmount = document.getElementById("amount-max").value;
    const minDate = document.getElementById("date-from").value;
    const maxDate = document.getElementById("date-to").value;

    if (minAmount && maxAmount && Number(minAmount) > Number(maxAmount)) {
        alert("Minimum amount cannot be greater than maximum amount.");
        return;
    }

    if (minDate && maxDate && minDate > maxDate) {
        alert("From date cannot be later than To date.");
        return;
    }

    try {
        const response = await fetch("/api/expenses/filter", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                category: category,
                min_amount: minAmount,
                max_amount: maxAmount,
                min_date: minDate,
                max_date: maxDate
            })
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.message);
            return;
        }

        allExpenses = result;
        expanded = true;
        currentPage = 1;

        displayExpenses();

    } catch (error) {
        console.error("Error applying filters:", error);
    }
});

// --------------------------------------------------
// CLEAR FILTERS
// --------------------------------------------------

const clearFiltersButton = document.getElementById("clear-filters");

clearFiltersButton.addEventListener("click", async function() {

    document.getElementById("category-filter").value = "All";
    document.getElementById("amount-min").value = "";
    document.getElementById("amount-max").value = "";
    document.getElementById("date-from").value = "";
    document.getElementById("date-to").value = "";

    await loadExpenses();
});

// --------------------------------------------------
// UPDATE SUMMARY
// --------------------------------------------------

function updateSummary() {
    const totalExpenses = allExpenses.reduce(
        (total, expense) => total + Number(expense.amount),
        0
    );

    const totalTransactions = allExpenses.length;

    document.getElementById("total-expenses").textContent =
        `₹${totalExpenses.toFixed(2)}`;

    document.getElementById("total-transactions").textContent =
        totalTransactions;
}

let categoryChart;

async function loadCategoryChart() {
    try {
        const response = await fetch("/api/expenses/chart/category");

        if (!response.ok) {
            throw new Error("Could not load category chart data");
        }

        const data = await response.json();

        const categories = data.map(item => item[0]);
        const amounts = data.map(item => Number(item[1]));

        const canvas = document.getElementById("category-chart");
        const ctx = canvas.getContext("2d");

        console.log(canvas);
        

        if (categoryChart) {
            categoryChart.destroy();
        }

        categoryChart = new Chart(ctx, {
            type: "doughnut",

            data: {
                labels: categories,

                datasets: [{
                    data: amounts
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins:{legend:{labels:{color:'rgb(252, 249, 203)'}}}
                    }
        });

    } catch (error) {
        console.error("Error loading category chart:", error);
    }
}

let monthlyChart;

async function loadMonthlyChart() {
    try {
        const response = await fetch("/api/expenses/chart/monthly");

        if (!response.ok) {
            throw new Error("Could not load monthly chart data");
        }

        const data = await response.json();

        const months = data.map(item => {
            const [year, month] = item[0].split("-");

            return new Date(Number(year), Number(month) - 1)
                .toLocaleDateString("en-IN", {
                    month: "short",
                    year: "numeric"
                });
        });

        const amounts = data.map(item => Number(item[1]));

        const ctx = document.getElementById("monthly-expense-chart");

        if (monthlyChart) {
            monthlyChart.destroy();
        }

        monthlyChart = new Chart(ctx, {
            type: "bar",

            data: {
                labels: months,

                datasets: [{
                    label: "Monthly Spending (₹)",
                    data: amounts
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        labels: {
                            color: "#ffffff"
                        }
                    }
                },

                scales: {
                    x: {
                        ticks: {
                            color: "#ffffff"
                        }
                    },

                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: "#ffffff"
                        }
                    }
                }
            }
        });

    } catch (error) {
        console.error("Error loading monthly chart:", error);
    }
}
