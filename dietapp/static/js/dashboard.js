// Dashboard için gerekli JavaScript fonksiyonları
document.addEventListener('DOMContentLoaded', function() {
    // Tarih formatı
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    document.getElementById('current-date').textContent = new Date().toLocaleDateString('tr-TR', options);

    // Grafikleri başlat
    initializeCharts();
});

// Grafikleri başlatma fonksiyonu
function initializeCharts() {
    // Kilo grafiği
    const weightCtx = document.getElementById('weightChart');
    if (weightCtx) {
        new Chart(weightCtx, {
            type: 'line',
            data: {
                labels: ['1. Hafta', '2. Hafta', '3. Hafta', '4. Hafta'],
                datasets: [{
                    label: 'Kilo Değişimi (kg)',
                    data: [75, 74.5, 74, 73.5],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Kilo Takibi'
                    }
                }
            }
        });
    }

    // Beslenme grafiği
    const nutritionCtx = document.getElementById('nutritionChart');
    if (nutritionCtx) {
        new Chart(nutritionCtx, {
            type: 'doughnut',
            data: {
                labels: ['Protein', 'Karbonhidrat', 'Yağ'],
                datasets: [{
                    data: [30, 50, 20],
                    backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                        'rgb(255, 205, 86)'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Makro Besin Dağılımı'
                    }
                }
            }
        });
    }
} 