document.addEventListener('DOMContentLoaded', function() {
    // Besin arama fonksiyonu
    function searchFoods(input, select) {
        const searchTerm = input.value.toLowerCase();
        const options = select.options;
        
        for (let i = 0; i < options.length; i++) {
            const option = options[i];
            const text = option.text.toLowerCase();
            if (text.includes(searchTerm)) {
                option.style.display = '';
            } else {
                option.style.display = 'none';
            }
        }
    }

    // Besin ekleme fonksiyonu
    function addFoodForm(containerId) {
        const container = document.querySelector(`#${containerId}`);
        const totalForms = container.querySelector('#id_meal_food_set-TOTAL_FORMS');
        const formCount = parseInt(totalForms.value);
        
        // Yeni form oluştur
        const formTemplate = document.createElement('div');
        formTemplate.className = 'row meal-food-form mb-3';
        formTemplate.innerHTML = `
            <div class="col-md-6">
                <div class="input-group">
                    <span class="input-group-text">
                        <i class="fas fa-search"></i>
                    </span>
                    <input type="text" class="form-control food-search" placeholder="Besin ara...">
                </div>
                <select name="meal_food_set-${formCount}-food" id="id_meal_food_set-${formCount}-food" class="form-select mt-2">
                    <option value="">---------</option>
                    {% for food in foods %}
                    <option value="{{ food.id }}" 
                        data-calories="{{ food.calories }}"
                        data-protein="{{ food.protein }}"
                        data-carbs="{{ food.carbs }}"
                        data-fat="{{ food.fat }}">
                        {{ food.name }}
                    </option>
                    {% endfor %}
                </select>
            </div>
            <div class="col-md-4">
                <div class="input-group">
                    <input type="number" name="meal_food_set-${formCount}-amount" 
                        id="id_meal_food_set-${formCount}-amount" 
                        class="form-control" 
                        step="0.01" 
                        min="0" 
                        placeholder="Miktar (g)">
                    <span class="input-group-text">g</span>
                </div>
            </div>
            <div class="col-md-2">
                <button type="button" class="btn btn-danger btn-sm remove-food">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
        
        container.appendChild(formTemplate);
        totalForms.value = formCount + 1;

        // Yeni eklenen form için event listener'ları ekle
        const newForm = container.lastElementChild;
        const searchInput = newForm.querySelector('.food-search');
        const foodSelect = newForm.querySelector('select');
        const amountInput = newForm.querySelector('input[type="number"]');

        // Arama fonksiyonunu ekle
        searchInput.addEventListener('input', () => {
            searchFoods(searchInput, foodSelect);
        });

        // Besin seçildiğinde miktar alanına odaklan
        foodSelect.addEventListener('change', () => {
            if (foodSelect.value) {
                amountInput.focus();
                calculateNutritionValues(container.closest('.modal'));
            }
        });

        // Miktar değiştiğinde besin değerlerini güncelle
        amountInput.addEventListener('input', () => {
            calculateNutritionValues(container.closest('.modal'));
        });
    }

    // Besin silme fonksiyonu
    document.addEventListener('click', function(e) {
        if (e.target.closest('.remove-food')) {
            const form = e.target.closest('.meal-food-form');
            const container = form.closest('#meal-foods, #meal-foods-edit');
            if (container.querySelectorAll('.meal-food-form').length > 1) {
                form.remove();
                calculateNutritionValues(container.closest('.modal'));
            }
        }
    });

    // Yeni besin ekleme butonu
    document.querySelector('#add-food').addEventListener('click', () => addFoodForm('meal-foods'));
    document.querySelector('#add-food-edit').addEventListener('click', () => addFoodForm('meal-foods-edit'));

    // Düzenleme modalı için event listener
    document.querySelectorAll('.edit-meal').forEach(button => {
        button.addEventListener('click', function() {
            const mealId = this.dataset.mealId;
            const mealType = this.dataset.mealType;
            const mealName = this.dataset.mealName;
            const mealDescription = this.dataset.mealDescription;
            const mealTime = this.dataset.mealTime;
            const mealDay = this.dataset.mealDay;

            // Form alanlarını doldur
            document.querySelector('#edit-meal-id').value = mealId;
            document.querySelector('#edit-meal-type').value = mealType;
            document.querySelector('#edit-meal-name').value = mealName;
            document.querySelector('#edit-meal-description').value = mealDescription;
            document.querySelector('#edit-meal-time').value = mealTime;
            document.querySelector('#edit-meal-day').value = mealDay;

            // Besinleri yükle
            fetch(`/plans/get-meal-foods/${mealId}/`)
                .then(response => response.json())
                .then(data => {
                    const container = document.querySelector('#meal-foods-edit');
                    container.innerHTML = ''; // Mevcut besinleri temizle
                    
                    if (data.foods.length > 0) {
                        data.foods.forEach((food, index) => {
                            const formTemplate = document.createElement('div');
                            formTemplate.className = 'row meal-food-form mb-3';
                            formTemplate.innerHTML = `
                                <div class="col-md-6">
                                    <div class="input-group">
                                        <span class="input-group-text">
                                            <i class="fas fa-search"></i>
                                        </span>
                                        <input type="text" class="form-control food-search" placeholder="Besin ara...">
                                    </div>
                                    <select name="meal_food_set-${index}-food" id="id_meal_food_set-${index}-food" class="form-select mt-2">
                                        <option value="">---------</option>
                                        {% for food in foods %}
                                        <option value="{{ food.id }}" 
                                            data-calories="{{ food.calories }}"
                                            data-protein="{{ food.protein }}"
                                            data-carbs="{{ food.carbs }}"
                                            data-fat="{{ food.fat }}"
                                            {% if food.id == food.id %}selected{% endif %}>
                                            {{ food.name }}
                                        </option>
                                        {% endfor %}
                                    </select>
                                </div>
                                <div class="col-md-4">
                                    <div class="input-group">
                                        <input type="number" name="meal_food_set-${index}-amount" 
                                            id="id_meal_food_set-${index}-amount" 
                                            class="form-control" 
                                            step="0.01" 
                                            min="0" 
                                            value="${food.amount}"
                                            placeholder="Miktar (g)">
                                        <span class="input-group-text">g</span>
                                    </div>
                                </div>
                                <div class="col-md-2">
                                    <button type="button" class="btn btn-danger btn-sm remove-food">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </div>
                            `;
                            container.appendChild(formTemplate);

                            // Yeni eklenen form için event listener'ları ekle
                            const newForm = container.lastElementChild;
                            const searchInput = newForm.querySelector('.food-search');
                            const foodSelect = newForm.querySelector('select');
                            const amountInput = newForm.querySelector('input[type="number"]');

                            // Arama fonksiyonunu ekle
                            searchInput.addEventListener('input', () => {
                                searchFoods(searchInput, foodSelect);
                            });

                            // Besin seçildiğinde miktar alanına odaklan
                            foodSelect.addEventListener('change', () => {
                                if (foodSelect.value) {
                                    amountInput.focus();
                                    calculateNutritionValues(container.closest('.modal'));
                                }
                            });

                            // Miktar değiştiğinde besin değerlerini güncelle
                            amountInput.addEventListener('input', () => {
                                calculateNutritionValues(container.closest('.modal'));
                            });
                        });
                    } else {
                        // Hiç besin yoksa boş bir form ekle
                        addFoodForm('meal-foods-edit');
                    }
                    
                    // TOTAL_FORMS değerini güncelle
                    document.querySelector('#meal-foods-edit #id_meal_food_set-TOTAL_FORMS').value = Math.max(1, data.foods.length);
                    
                    // Besin değerlerini hesapla
                    calculateNutritionValues(document.querySelector('#editMealModal'));
                });
        });
    });

    // Besin değerlerini hesaplayan fonksiyon
    function calculateNutritionValues(container) {
        let totalCalories = 0;
        let totalProtein = 0;
        let totalCarbs = 0;
        let totalFat = 0;

        // Tüm besin formlarını seç
        const foodForms = container.querySelectorAll('.meal-food-form');
        
        foodForms.forEach(form => {
            const foodSelect = form.querySelector('select[name$="-food"]');
            const amountInput = form.querySelector('input[name$="-amount"]');
            
            if (foodSelect && amountInput) {
                const selectedOption = foodSelect.options[foodSelect.selectedIndex];
                const amount = parseFloat(amountInput.value) || 0;
                
                // Besin değerlerini data attribute'lerinden al
                const calories = parseFloat(selectedOption.dataset.calories) || 0;
                const protein = parseFloat(selectedOption.dataset.protein) || 0;
                const carbs = parseFloat(selectedOption.dataset.carbs) || 0;
                const fat = parseFloat(selectedOption.dataset.fat) || 0;
                
                // Toplam değerleri hesapla
                totalCalories += (calories * amount) / 100;
                totalProtein += (protein * amount) / 100;
                totalCarbs += (carbs * amount) / 100;
                totalFat += (fat * amount) / 100;
            }
        });

        // Değerleri güncelle
        const nutritionValues = container.querySelector('.nutrition-values');
        if (nutritionValues) {
            nutritionValues.innerHTML = `
                <div class="nutrition-value">
                    <span class="nutrition-label">Kalori:</span>
                    <span class="nutrition-amount">${totalCalories.toFixed(1)} kcal</span>
                </div>
                <div class="nutrition-value">
                    <span class="nutrition-label">Protein:</span>
                    <span class="nutrition-amount">${totalProtein.toFixed(1)} g</span>
                </div>
                <div class="nutrition-value">
                    <span class="nutrition-label">Karbonhidrat:</span>
                    <span class="nutrition-amount">${totalCarbs.toFixed(1)} g</span>
                </div>
                <div class="nutrition-value">
                    <span class="nutrition-label">Yağ:</span>
                    <span class="nutrition-amount">${totalFat.toFixed(1)} g</span>
                </div>
            `;
        }
    }

    // Sayfa yüklendiğinde mevcut formlar için event listener'ları ekle
    document.querySelectorAll('.modal').forEach(modal => {
        const container = modal.querySelector('#meal-foods, #meal-foods-edit');
        if (container) {
            container.querySelectorAll('.meal-food-form').forEach(form => {
                const foodSelect = form.querySelector('select');
                const amountInput = form.querySelector('input[type="number"]');
                
                if (foodSelect) foodSelect.addEventListener('change', () => calculateNutritionValues(modal));
                if (amountInput) amountInput.addEventListener('input', () => calculateNutritionValues(modal));
            });
        }
    });
}); 