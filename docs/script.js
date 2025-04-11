async function fetchData() {
  const res = await fetch('data.json');
  const data = await res.json();
  renderChart(data);
  renderTable(data);
}

function renderChart(data) {
  const labels = data.map(item => item.name);
  const values = data.map(item => item.status === 'success' ? 1 : 0);

  new Chart(document.getElementById('chart'), {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: '是否成功 (1=成功, 0=失败)',
        data: values,
        backgroundColor: values.map(v => v ? 'green' : 'red')
      }]
    }
  });
}

function renderTable(data) {
  const container = document.getElementById('interface-list');
  container.innerHTML = data.map(item => `
    <div class="card mb-2 ${item.status === 'success' ? 'border-success' : 'border-danger'}">
      <div class="card-body">
        <h5 class="card-title">${item.name}</h5>
        <p class="card-text">状态: <strong>${item.status}</strong></p>
        <p class="card-text"><small class="text-muted">最后测试时间: ${item.last_test_time}</small></p>
      </div>
    </div>
  `).join('');
}

fetchData();
