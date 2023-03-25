function getInfo() {

  const uniprot_id = document.getElementById('protein_id').value.trim();

  console.log(uniprot_id);

  let sql = "select * from charge_info where uniprotID = '" + uniprot_id + "'";

  connection.query(sql, function (err, results, fields) {
      if (err) {
          console.log(err);
      }
      console.log(results);
  });

  drawChart();
};


// connection.end(); // DB 접속 종료

function drawChart() {
    const ctx = document.getElementById("line-chart")
    new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['C-terminus','Domain1', 'Domain2', 'Domain3', 'Domain4', 'N-terminus'],
      datasets: [{ 
          data: [-3.4, -10.1, 1.1, -0.7, -4.7, -6.7],
          label: "Charge",
          borderColor: "#3e95cd",
          fill: false
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Charge value of each sequences'
      }
    }
  });
}

// window.addEventListener('click', drawChart, false); 
const searchBtn = document.getElementById('search');
searchBtn.addEventListener('click', drawChart);