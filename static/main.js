const socket = io();

/* LOAD SLOT STATUS */
function loadStatus(){
    fetch("/api/status")
    .then(res => res.json())
    .then(data => {

        const grid = document.getElementById("grid");
        grid.innerHTML = "";

        for(let i=1;i<=50;i++){
            let slot = i.toString(16).toUpperCase();
            let div = document.createElement("div");

            div.className = "slot " + (data[slot] || "available");
            div.innerText = "Slot " + slot;

            grid.appendChild(div);
        }
    });
}

/* LOAD ACTIVITY LOGS */
function loadLogs(){
    fetch("/api/logs")
    .then(res => res.json())
    .then(data => {

        let table = document.getElementById("logTable");

        table.innerHTML = `
        <tr>
            <th>Plate</th>
            <th>Slot</th>
            <th>Entry Time</th>
            <th>Exit Time</th>
            <th>Bill (₹)</th>
        </tr>`;

        data.forEach(row => {
            table.innerHTML += `
            <tr>
                <td>${row.plate}</td>
                <td>${row.slot}</td>
                <td>${row.entry}</td>
                <td>${row.exit}</td>
                <td>${row.fee}</td>
            </tr>`;
        });
    });
}

/* INITIAL LOAD */
loadStatus();
loadLogs();

/* REAL-TIME UPDATE */
socket.on("update", () => {
    loadStatus();
    loadLogs();
});
