document.addEventListener("DOMContentLoaded", function () {
    let selectedPlayerId = null;
    const scoreId = document.getElementById("table").getAttribute("data-score-id");

    const socket = new WebSocket(`ws://${window.location.host}/ws/score/${scoreId}/`);

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        updateScoreboard(data.entries);
    };

    function updateScoreboard(entries) {
        const tableBody = document.querySelector("tbody");
        tableBody.innerHTML = ""; // Clear current table

        entries.forEach((entry, index) => {
            const row = document.createElement("tr");
            row.classList.add("player-row");
            row.setAttribute("data-player-id", entry.player__id);

            row.innerHTML = `
                <td>${entry.rank}</td>
                <td><a href="/p/${entry.player__name}/" class="text-decoration-none">${entry.player__name}</a></td>
                <td>${entry.value}</td>
            `;

            tableBody.appendChild(row);
        });
    }

    // **Event Delegation**: Listen for row clicks on <tbody>
    document.querySelector("tbody").addEventListener("click", function (event) {
        let row = event.target.closest("tr");
        if (!row || !row.classList.contains("player-row")) return;

        document.querySelectorAll(".player-row").forEach(r => r.classList.remove("table-primary"));
        row.classList.add("table-primary");

        selectedPlayerId = row.getAttribute("data-player-id");
        document.getElementById("selected-player-id").value = selectedPlayerId;
    });



    function modifyScore(action) {
        if (!selectedPlayerId) {
            alert("Please select a player first.");
            return;
        }

        const value = parseInt(document.getElementById("score-change").value, 10);
        if (isNaN(value)) {
            alert("Please enter a valid number.");
            return;
        }

        const requestData = {
            player_id: selectedPlayerId,
            score_id: scoreId,
            value: action === "add" ? value : -value
        };
    
        fetch("/modify_score/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            },
            body: JSON.stringify(requestData)
        });
    }

    // Event listeners for buttons
    document.getElementById("add-score").addEventListener("click", function () {
        modifyScore("add");
    });

    document.getElementById("remove-score").addEventListener("click", function () {
        modifyScore("remove");
    });
});